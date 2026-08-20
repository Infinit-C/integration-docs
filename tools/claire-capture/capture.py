#!/usr/bin/env python3
"""Claire 대시보드 가이드 캡처 도구.

사용법:
  python capture.py login   # 헤드 브라우저가 뜬다 → 직접 로그인 (세션은 .profile/에 저장)
  python capture.py shoot [이름...]   # 가이드 캡처 일괄 생성 (기본: 전체)

- 출력: ../../static/img/claire/{이름}.png (뷰포트 1440x900, 2x 스케일)
- 민감 정보(광고주명·계정 ID·URN·사용자명)는 캡처 직전에 블러 CSS를 주입해 가린다.
  광고주/캠페인이 늘면 SENSITIVE 목록에 추가할 것.
"""
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://claire.infinit-c.com"
HERE = Path(__file__).parent
PROFILE = HERE / ".profile"  # gitignore 대상 — 절대 커밋 금지
OUT = HERE.parent.parent / "static" / "img" / "claire"

# 부분 문자열 매치로 블러 처리할 민감 텍스트
SENSITIVE = [
    # 광고주·캠페인
    "키세카츠", "택산가든",
    # 사용자
    "Jaehyon Yoon", "jh.yoon",
    # 계정·조직·캠페인 식별자
    "1396192822257338", "35056664", "745226954918", "120242560568860305",
    "50103304", "82936400", "24053310", "54622417", "54833101", "84974901",
]

BLUR_JS = """
(words) => {
  const hits = new Set();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walker.nextNode())) {
    const t = n.textContent || '';
    if (words.some((w) => t.includes(w))) {
      if (n.parentElement) hits.add(n.parentElement);
    }
  }
  // 아바타 이니셜
  document.querySelectorAll('*').forEach((el) => {
    if (el.children.length === 0 && (el.textContent || '').trim() === 'JY') hits.add(el);
  });
  hits.forEach((el) => { el.style.filter = 'blur(7px)'; });
  return hits.size;
}
"""


def _click_tab(page, name):
    page.get_by_role("tab", name=name).click()
    page.wait_for_timeout(1500)


def _open_chat(page):
    page.get_by_role("button", name="Open chat").click()
    page.wait_for_timeout(2500)


# (이름, 경로, 페이지 로드 후 액션)
SHOTS = [
    ("overview", "/", None),
    ("campaign-groups", "/campaign-groups", None),
    ("campaign-group-detail", "/campaign-groups/50103304", None),
    ("campaign-group-campaigns", "/campaign-groups/50103304",
     lambda p: _click_tab(p, "Campaigns")),
    ("campaign-detail", "/campaigns/24053310", None),
    ("campaign-trends", "/campaigns/24053310", lambda p: _click_tab(p, "Trends")),
    ("campaign-kpi", "/campaigns/24053310", lambda p: _click_tab(p, "KPI")),
    ("chat-panel", "/campaigns/24053310", _open_chat),
    ("my-chats", "/my-chats", None),
    ("metric-categories", "/metric-categories", None),
    ("metric-formulas", "/metric-formulas", None),
    ("kpi-rules", "/kpis", None),
    ("organization-settings", "/organization-settings", None),
    ("communication-groups", "/communication-groups", None),
]


def _context(p, headed):
    return p.chromium.launch_persistent_context(
        PROFILE,
        headless=not headed,
        viewport={"width": 1440, "height": 900},
        device_scale_factor=2,
        locale="ko-KR",
        timezone_id="Asia/Seoul",
    )


def login():
    with sync_playwright() as p:
        ctx = _context(p, headed=True)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(BASE)
        print("브라우저에서 로그인해 주세요 (이메일/비밀번호 권장 — Google OAuth는 자동화 브라우저를 차단할 수 있음)")
        # 사이드바 Overview 링크가 보이면 로그인 완료로 판단
        page.wait_for_selector("text=Overview", timeout=300_000)
        page.wait_for_timeout(2000)
        print("로그인 감지 — 세션 저장 완료. 창을 닫습니다.")
        ctx.close()


def shoot(only=None):
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        ctx = _context(p, headed=False)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for name, path, action in SHOTS:
            if only and name not in only:
                continue
            page.goto(BASE + path, wait_until="networkidle")
            page.wait_for_timeout(2500)
            if "로그인" in page.content() and "Sign in" in page.content():
                print("!! 세션 만료 — `python capture.py login` 먼저 실행")
                sys.exit(1)
            if action:
                action(page)
            blurred = page.evaluate(BLUR_JS, SENSITIVE)
            out = OUT / f"{name}.png"
            page.screenshot(path=str(out))
            print(f"✓ {name}.png (blur {blurred}곳)")
        ctx.close()


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "shoot"
    if mode == "login":
        login()
    elif mode == "shoot":
        shoot(set(sys.argv[2:]) or None)
    else:
        print(__doc__)
