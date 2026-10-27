#!/usr/bin/env python3
"""클레어 프론트 읽기 전용 점검 크롤러.

사용법: CLAIRE_PROFILE=.profile-admin python audit.py
- 헤드 브라우저를 띄우고 사용자가 로그인할 때까지(최대 30분) 기다린다. 점검이 끝날 때까지 창을 닫지 않는다.
- 사이드바의 모든 메뉴 → 목록의 첫 상세 → '새로 만들기' 폼을 GET 이동으로만 순회한다. 버튼은 누르지 않는다.
- 페이지마다 콘솔 오류, 4xx/5xx 응답, 404, 번역 누락 의심 문자열, 가로 넘침, 중복 표 머리글, 빈 본문을 기록하고 캡처를 남긴다.
- 한국어 전체 순회 → 영어 사이드바 순회 → 1280 폭 사이드바 순회.
- 출력: out/audit/report.json, out/audit/*.png, 마지막에 요약 출력.
"""
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

from capture import BASE, PROFILE
from deck_shots import _set_language

OUT = Path(__file__).parent / "out" / "audit"
MANUAL = 30 * 60 * 1000
SKIP = re.compile(r"logout|sign-?out|oauth|/api/|mailto:|^https?://(?!claire\.infinit-c\.com)", re.I)
# 번역 누락·렌더 사고 의심 패턴
SUSPECT = re.compile(r"\b(undefined|null|NaN|\[object Object\]|Invalid Date)\b|\{\{|\}\}|^[a-z]+(\.[a-zA-Z0-9_]+){2,}$")

PAGE_CHECKS = """
() => {
  const main = document.querySelector('main') || document.body;
  const texts = [];
  const w = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
  let n; while ((n = w.nextNode())) { const t = n.textContent.trim(); if (t) texts.push(t); }
  const heads = [...main.querySelectorAll('table')].map(t => [...t.querySelectorAll('thead th')].map(th => th.innerText.trim()).filter(Boolean));
  const dupHeads = heads.filter(h => new Set(h).size !== h.length);
  const overflow = document.documentElement.scrollWidth > document.documentElement.clientWidth + 2
    || main.scrollWidth > main.clientWidth + 2;
  const imgsBroken = [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.src && !i.src.startsWith('data:')).map(i => i.src).slice(0, 5);
  const emptyMain = main.innerText.trim().length < 20;
  const notFound = /This page could not be found|404/.test(document.body.innerText) && document.body.innerText.length < 400;
  const h1 = (main.querySelector('h1') || {}).innerText || '';
  const btnNoName = [...main.querySelectorAll('button')].filter(b => b.offsetParent && !b.innerText.trim() && !b.getAttribute('aria-label') && !b.getAttribute('title')).length;
  const inputsNoLabel = [...main.querySelectorAll('input:not([type=hidden]),select,textarea')].filter(e => e.offsetParent && !e.labels?.length && !e.getAttribute('aria-label') && !e.getAttribute('aria-labelledby') && !e.getAttribute('placeholder')).length;
  return {texts, dupHeads, overflow, imgsBroken, emptyMain, notFound, h1, btnNoName, inputsNoLabel,
          title: document.title, mainLinks: [...main.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(Boolean)};
}
"""


def slug(url):
    p = urlparse(url).path.strip("/") or "home"
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", p)[:80]


class Audit:
    def __init__(self, page):
        self.page = page
        self.records = []
        self.cur = None
        page.on("console", lambda m: self._log("console", f"{m.type}: {m.text[:300]}") if m.type == "error" else None)
        page.on("pageerror", lambda e: self._log("pageerror", str(e)[:300]))
        page.on("response", self._resp)
        page.on("requestfailed", lambda r: self._log("requestfailed", f"{r.method} {r.url[:150]} {r.failure}")
                if "/api/" in r.url or r.resource_type in ("document", "script", "stylesheet") else None)

    def _resp(self, r):
        if r.status >= 400 and ("/api/" in r.url or r.resource_type in ("document", "script", "stylesheet", "image")):
            body = ""
            try:
                body = r.text()[:200] if "/api/" in r.url else ""
            except Exception:
                pass
            self._log("http", f"{r.status} {r.request.method} {r.url.replace(BASE, '')[:150]} {body}")

    def _log(self, kind, msg):
        if self.cur is not None:
            self.cur.setdefault(kind, []).append(msg)

    def visit(self, url, tag, shot=True):
        self.cur = {"url": url.replace(BASE, ""), "tag": tag}
        t0 = time.time()
        try:
            self.page.goto(url, wait_until="networkidle", timeout=30000)
        except Exception as e:
            self.cur["nav_error"] = str(e)[:200]
        self.page.wait_for_timeout(1200)
        self.cur["load_s"] = round(time.time() - t0, 1)
        self.cur["final_url"] = self.page.url.replace(BASE, "")
        try:
            c = self.page.evaluate(PAGE_CHECKS)
        except Exception as e:
            c = {"texts": [], "mainLinks": [], "evalError": str(e)[:200]}
        sus = sorted({t for t in c.get("texts", []) if SUSPECT.search(t)})[:15]
        self.cur.update({k: v for k, v in c.items() if k not in ("texts", "mainLinks")}, suspect=sus)
        if shot:
            name = f"{tag}-{slug(self.page.url)}.png"
            try:
                self.page.screenshot(path=str(OUT / name), full_page=True)
                self.cur["shot"] = name
            except Exception as e:
                self.cur["shot_error"] = str(e)[:100]
        self.records.append(self.cur)
        flags = [k for k in ("console", "pageerror", "http", "requestfailed", "nav_error") if self.cur.get(k)] \
            + [k for k in ("overflow", "emptyMain", "notFound") if self.cur.get(k)] + (["suspect"] if sus else []) \
            + (["dupHeads"] if self.cur.get("dupHeads") else [])
        print(f"  [{tag}] {self.cur['url']:<50} {self.cur['load_s']:>5}s  {' '.join(flags) or 'ok'}", flush=True)
        return c.get("mainLinks", [])


def nav_links(page):
    # 접힌 메뉴(캠페인 등)를 펼쳐야 하위 링크가 DOM에 생긴다
    for b in page.locator("nav button[aria-expanded='false'], aside button[aria-expanded='false']").all():
        try:
            b.click(); page.wait_for_timeout(300)
        except Exception:
            pass
    hrefs = page.locator("nav a[href], aside a[href]").evaluate_all("els=>els.map(e=>e.getAttribute('href'))")
    seen, out = set(), []
    for h in hrefs:
        if not h or SKIP.search(h) or not h.startswith("/"):
            continue
        if h not in seen:
            seen.add(h); out.append(h)
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE, headless=False, viewport={"width": 1600, "height": 1180},
            locale="ko-KR", timezone_id="Asia/Seoul")
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(BASE, wait_until="networkidle")
        if "/login" in page.url:
            print(">> 이 창에서 관리자 계정으로 로그인해 주세요. 점검이 끝날 때까지 창은 닫히지 않습니다.", flush=True)
            page.wait_for_selector("a[href='/campaigns'], a[href^='/dashboards']", timeout=MANUAL)
            page.wait_for_timeout(3000)
        print("로그인 확인:", page.url, flush=True)
        a = Audit(page)
        prev = _set_language(page, "ko")

        # 1) 한국어: 사이드바 → 첫 상세 → 새로 만들기
        links = nav_links(page)
        print(f"\n== 한국어 순회: 사이드바 {len(links)}개", flush=True)
        detail_seen = set()
        for h in links:
            main_links = a.visit(BASE + h, "ko")
            cands = [l for l in main_links if l.startswith(h + "/") and not SKIP.search(l)]
            new = next((l for l in cands if re.search(r"/(new|create)$", l)), None)
            first = next((l for l in cands if l != new and not re.search(r"/(new|create)$", l)), None)
            for d in (new, first):
                if d and d not in detail_seen:
                    detail_seen.add(d)
                    sub = a.visit(BASE + d, "ko")
                    # 상세 안의 탭/하위 링크 1단계
                    for t in [l for l in sub if l.startswith(d + "/") and not SKIP.search(l)][:4]:
                        if t not in detail_seen:
                            detail_seen.add(t); a.visit(BASE + t, "ko")
                    # 상세 화면의 탭(role=tab)도 한 번씩 열어 캡처
                    for tab in page.get_by_role("tab").all_inner_texts()[1:6]:
                        try:
                            page.get_by_role("tab", name=tab, exact=True).click(); page.wait_for_timeout(2500)
                            page.screenshot(path=str(OUT / f"ko-{slug(d)}-tab-{tab}.png"), full_page=True)
                        except Exception as e:
                            print("  tab fail", d, tab, str(e)[:80])

        # 2) 영어: 사이드바만 (번역 누락·레이아웃 깨짐 비교)
        _set_language(page, "en")
        print(f"\n== 영어 순회", flush=True)
        for h in nav_links(page):
            a.visit(BASE + h, "en")
        _set_language(page, "ko")

        # 3) 1280 폭: 사이드바만 (가로 넘침)
        page.set_viewport_size({"width": 1280, "height": 900})
        print(f"\n== 1280 폭 순회", flush=True)
        for h in links:
            a.visit(BASE + h, "w1280", shot=False)
        page.set_viewport_size({"width": 1600, "height": 1180})

        if prev:
            _set_language(page, prev)
        (OUT / "report.json").write_text(json.dumps(a.records, ensure_ascii=False, indent=1))
        ctx.close()

    # 요약
    bad = [r for r in a.records if any(r.get(k) for k in ("console", "pageerror", "http", "requestfailed", "nav_error", "overflow", "emptyMain", "notFound", "suspect", "dupHeads"))]
    print(f"\n페이지 {len(a.records)}개 점검, 이상 {len(bad)}개 → {OUT / 'report.json'}")


if __name__ == "__main__":
    main()
