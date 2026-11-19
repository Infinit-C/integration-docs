#!/usr/bin/env python3
"""Google OAuth 심사용 스크린캐스트 (GOOGLE_REVIEW_HANDOFF_20261119.md 장면 1~7·9).

  python record_google_review.py record dv360       # 장면 1·2·6·7. 실제 Chrome + 화면 녹화(screencapture) 자동
  python record_google_review.py record google_ads  # 장면 3·4·5·9 (Google Ads 계정 권한이 생긴 뒤)
  python record_google_review.py record_tail   # 수집 뒤 5·7번(대시보드 수치)만 다시 녹화
  python record_google_review.py cleanup       # 촬영이 남긴 Google Ads·DV360 연동 해제 (Product 팀)

- Google 로그인·동의 화면과 9번의 Google 계정 보안 페이지는 사용자가 직접 조작한다. 터미널 안내를 따를 것.
- 주소창이 찍혀야 하므로 Playwright 내장 녹화 대신 macOS screencapture로 Chrome 창 영역을 녹화한다.
- Google 화면은 블러하지 않는다. Claire 화면은 광고주명·ID 자동 블러 + 계정/캠페인 선택 목록 전체 블러.
- 출력: out/google-review.mp4 (tail: out/google-review-part2.mp4)
"""
import re
import signal
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from capture import BASE, PROFILE, SENSITIVE, _wide_range
from record_test import AUTO_BLUR_JS, CURSOR_JS, Recorder

HERE = Path(__file__).parent
OUT = HERE / "out"
REVIEW_PROFILE = HERE / ".profile-google-review"  # 로그인 화면부터 담기 위해 기존 세션과 분리
MANUAL = 10 * 60 * 1000
ORG = "Product"

# 선택 목록(광고 계정·광고주·캠페인)은 고객사 이름이 섞여 있으니 체크박스 빼고 전부 흐린다
BLUR_ROWS_JS = r"""() => {
  for (const td of document.querySelectorAll('main tbody td')) {
    if (td.querySelector('[role=checkbox], input[type=checkbox]')) continue;
    td.style.filter = 'blur(7px)';
  }
  for (const b of document.querySelectorAll('main button'))  // 광고주 탭 "1.이름 (n)"
    if (/^\d+\./.test(b.textContent.trim())) b.style.filter = 'blur(7px)';
}"""


class ReviewRecorder(Recorder):
    def prep(self, wait=1800):
        self.page.wait_for_timeout(wait)
        if self.page.url.startswith(BASE):  # Google 화면은 그대로
            self.page.evaluate(AUTO_BLUR_JS, SENSITIVE)
            self.page.evaluate(CURSOR_JS)

    def hold(self, note, ms=3000):
        print("  ·", note)
        self.page.wait_for_timeout(ms)


def _ctx(p, headed):
    kw = dict(headless=not headed, locale="en-US", timezone_id="Asia/Seoul")
    if headed:  # 실제 Chrome: Google이 자동화 Chromium 로그인을 막는 문제 회피. 주소창 포함 창 크기 고정
        _chrome_prefs()
        kw.update(channel="chrome", no_viewport=True, ignore_default_args=["--enable-automation", "--no-sandbox"],
                  args=["--window-size=1440,960", "--window-position=0,0", "--disable-sync",
                        "--disable-features=TranslateUI"])
    else:
        kw.update(viewport={"width": 1440, "height": 900})
    ctx = p.chromium.launch_persistent_context(REVIEW_PROFILE if headed else PROFILE, **kw)
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.on("dialog", lambda d: d.accept())
    return ctx, page


def _chrome_prefs():
    """Google 계정 로그인 시 Chrome이 '직장 프로필 만들기' 창을 띄우고 녹화 창을 닫아 버린다 → 브라우저 로그인·번역 끔."""
    import json
    f = REVIEW_PROFILE / "Default" / "Preferences"
    f.parent.mkdir(parents=True, exist_ok=True)
    prefs = json.loads(f.read_text()) if f.exists() else {}
    prefs.setdefault("signin", {}).update({"allowed": False, "allowed_on_next_startup": False})
    prefs.setdefault("translate", {})["enabled"] = False
    prefs.setdefault("profile", {})["password_manager_enabled"] = False
    f.write_text(json.dumps(prefs))


def _window_rect(page):
    cdp = page.context.new_cdp_session(page)
    b = cdp.send("Browser.getWindowBounds", {"windowId": cdp.send("Browser.getWindowForTarget")["windowId"]})["bounds"]
    return b["left"], b["top"], b["width"], b["height"]


class ScreenRec:
    """screencapture -v 로 Chrome 창 영역을 녹화. stop()에서 mp4로 변환."""
    def __init__(self, name, rect):
        OUT.mkdir(exist_ok=True)
        self.mov, self.mp4 = OUT / f"{name}.mov", OUT / f"{name}.mp4"
        self.mov.unlink(missing_ok=True)
        x, y, w, h = rect
        self.proc = subprocess.Popen(["screencapture", "-v", "-x", "-R", f"{x},{y},{w},{h}", str(self.mov)])

    def stop(self):
        self.proc.send_signal(signal.SIGINT)
        self.proc.wait(timeout=600)  # 긴 녹화는 마무리에 1분 이상 걸린다
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(self.mov), "-c:v", "libx264",
                        "-pix_fmt", "yuv420p", "-crf", "20", "-an", str(self.mp4)], check=True)
        print("saved:", self.mp4)


def _manual(page, note, until):
    print(f">> {note}  (최대 10분)")
    page.wait_for_url(until, timeout=MANUAL)
    page.wait_for_load_state("networkidle")


def _english_ui(page, r):
    lang = page.get_by_role("button", name=re.compile("언어 변경|Change language"))
    if lang.count():
        r.click(lang)
        r.click(page.get_by_role("menuitem", name=re.compile("^(영어|English)$")))
        page.wait_for_load_state("networkidle"); r.prep(1200)


def _ensure_org(page, r):
    btn = page.get_by_role("button", name=re.compile("팀 전환|Switch team"))
    if btn.count() and ORG not in btn.inner_text():
        r.click(btn)
        r.click(page.get_by_role("menuitem", name=ORG))
        page.wait_for_load_state("networkidle"); r.prep(1500)


def _check_first(page, r, name=""):
    """선택 목록: 전부 블러하고 name이 들어간 행(없으면 첫 행)만 체크."""
    page.get_by_role("checkbox").first.wait_for(timeout=120_000)
    page.wait_for_timeout(800)
    page.evaluate(BLUR_ROWS_JS)
    rows = page.locator("tr").filter(has=page.get_by_role("checkbox"))
    if name and rows.filter(has_text=re.compile(name, re.I)).count():
        rows = rows.filter(has_text=re.compile(name, re.I))
    box = rows.first.get_by_role("checkbox")
    if box.get_attribute("aria-checked") != "true":
        r.click(box, settle=300)
    page.evaluate(BLUR_ROWS_JS)
    r.hold("목록 (블러)", 2500)


def connect(page, r, platform, scope_note, account="", campaign=""):
    """Platform Integrations → Connect → platform → OAuth(수동) → 첫 계정 → 첫 캠페인 → Finish setup."""
    r.click(page.get_by_role("link", name="Platform Integrations"))
    r.prep()
    r.click(page.get_by_role("link", name="Connect").first)
    r.prep()
    r.click(page.get_by_role("radio", name=re.compile(platform)))
    page.wait_for_timeout(500)
    r.click(page.get_by_role("button", name="Continue"))
    r.prep(1200)
    r.click(page.get_by_role("button", name=re.compile(r"^Authorize")))
    _manual(page, f"Google 동의 화면: 주소창을 클릭해 client_id 가 3초 보이게 한 뒤 허용 ({scope_note})",
            re.compile(re.escape(BASE) + r"/platform-integrations/new\?.*step=accounts"))
    r.prep(2500)
    # 계정/광고주는 사용자가 고른다 (캠페인이 있는 회사 계정 하나). 고객사 이름은 YouTube 편집기에서 흐림 처리
    page.get_by_role("checkbox").first.wait_for(timeout=120_000)
    page.wait_for_timeout(800)
    row = page.locator("tr", has_text=re.compile(account, re.I)).first
    if row.count():
        r.click(row.get_by_role("checkbox"), settle=300)
        r.hold("계정 선택", 1500)
        r.click(page.get_by_role("button", name=re.compile(r"Import accounts|Continue")))
        page.wait_for_url(re.compile(r"step=campaigns"), timeout=120_000)
    else:
        _manual(page, f"'{account}' 행이 없음 — 캠페인이 있는 계정 하나를 체크하고 [Import accounts]를 누르세요", re.compile(r"step=campaigns"))
    r.prep(2500)
    _check_first(page, r, campaign)
    r.click(page.get_by_role("button", name=re.compile(r"Finish setup")))
    rb = page.get_by_role("button", name=re.compile(r"Restore"))
    try:
        rb.wait_for(timeout=2500); r.click(rb)
    except Exception:
        pass
    page.wait_for_url(lambda u: "/platform-integrations/new" not in u, timeout=120_000)
    r.prep(2000)
    r.hold("연동 완료", 2500)


def _open_campaign(page, r, platform, name=""):
    r.click(page.get_by_role("button", name="Campaigns"))
    page.wait_for_timeout(500)
    r.click(page.get_by_role("link", name="Campaigns", exact=True).first)
    r.prep(1500)
    rows = page.locator("tbody tr", has_text=re.compile(platform))
    row = rows.filter(has_text=re.compile(name, re.I)).first if name else rows.first
    link = row.get_by_role("link").first
    link.scroll_into_view_if_needed(); b = link.bounding_box()
    r.move_to(b["x"] + 20, b["y"] + 10)  # 두 줄로 꺾이는 링크는 중앙 좌표가 빈 곳이라 Playwright 클릭으로
    link.click()
    page.wait_for_url(re.compile(r"/campaigns/\d+"), timeout=30_000)
    r.prep(1500)


def google_ads_usage(page, r):
    """5번: 캠페인 대시보드(추이·KPI) + Alerts 탭 + 알림 목록."""
    _open_campaign(page, r, "Google Ads")
    r.click(page.get_by_role("tab", name="Dashboard"))
    _wide_range(page); r.prep(1500)
    r.hold("Google Ads 캠페인 대시보드", 4000)
    r.click(page.get_by_role("tab", name="Alerts"))
    r.prep(); r.hold("Alerts 탭", 2500)
    r.click(page.get_by_role("link", name="Alerts", exact=True).first)
    r.prep(); r.hold("알림 규칙 목록", 2500)


def dv360_usage(page, r):
    """7번: Insertion orders 탭 → 대시보드."""
    _open_campaign(page, r, "DV360|Display")
    r.click(page.get_by_role("tab", name=re.compile("Insertion")))
    r.prep(); r.hold("Insertion orders", 4000)
    r.click(page.get_by_role("tab", name="Dashboard"))
    _wide_range(page); r.prep(1500)
    r.hold("DV360 일별 성과", 4000)


def disconnect(page, r, platform):
    r.click(page.get_by_role("link", name="Platform Integrations"))
    r.prep()
    r.click(page.locator("tr", has_text=re.compile(platform)).get_by_role("button").last)
    r.click(page.get_by_role("menuitem", name="Disconnect"))
    r.click(page.get_by_role("button", name=re.compile("^(Continue|계속)$")))  # 확인 모달
    page.wait_for_timeout(3500); r.prep(500)
    r.hold("연동 해제됨", 2000)


def record(part="dv360"):
    """part: dv360 → 장면 1·2·6·7 (out/google-review-dv360).  google_ads → 장면 3·4·5·9 (out/google-review-ads)."""
    with sync_playwright() as p:
        ctx, page = _ctx(p, headed=True)
        r = ReviewRecorder(page)
        page.goto(BASE + "/login", wait_until="networkidle")
        rec = ScreenRec(f"google-review-{'ads' if part == 'google_ads' else part}", _window_rect(page))
        try:
            page.wait_for_timeout(1500)

            if part == "dv360":
                # 1. 로그인 화면 → Privacy Policy → Google APIs 절 (새 탭)
                with ctx.expect_page() as new:
                    r.click(page.get_by_role("link", name=re.compile("Privacy|개인정보")))
                pp = new.value
                pp.wait_for_load_state("networkidle"); pp.wait_for_timeout(1500)
                pp.get_by_text("Information received from Google APIs").first.scroll_into_view_if_needed()
                pp.mouse.wheel(0, -80)
                r.hold("Privacy — Google APIs 절", 6000)
                pp.close(); page.bring_to_front(); page.wait_for_timeout(1000)

            # 2. 로그인 — Google 로그인은 jh.yoon 계정이 다른 팀에 연결돼 있어 Claire가 거부(2026-11-19) → 이메일
            if "/login" in page.url:
                _manual(page, "Claire에 이메일/비밀번호로 로그인하세요",
                        lambda u: u.startswith(BASE) and "/login" not in u and "/oauth" not in u)
            r.prep(2000)
            _english_ui(page, r)
            _ensure_org(page, r)
            r.hold("로그인 후 대시보드", 2000)

            if part == "dv360":
                connect(page, r, "DV360|Display", "display-video, Bid Manager", account="gugus")   # 6
                dv360_usage(page, r)                                               # 7
            else:
                connect(page, r, "Google Ads", "adwords", account="GPN_BSN", campaign="pMax GMC")  # 3~4
                google_ads_usage(page, r)                                          # 5
                disconnect(page, r, "Google Ads")                                  # 9
                r.click(page.get_by_role("link", name="Campaigns", exact=True).first)
                r.prep(); r.hold("캠페인 Disconnected 상태", 3000)
                page.goto("https://myaccount.google.com/connections")
                _manual(page, "Google 계정 → 보안 → 타사 앱 목록에서 Claire가 없는 것을 보여 준 뒤, 주소창에 claire.infinit-c.com 을 쳐서 돌아오면 녹화가 끝납니다",
                        lambda u: u.startswith(BASE))
                page.wait_for_timeout(2000)
        finally:
            rec.stop()
            ctx.close()


def record_tail(part="dv360"):
    with sync_playwright() as p:
        ctx, page = _ctx(p, headed=True)
        r = ReviewRecorder(page)
        page.goto(BASE + "/", wait_until="networkidle")
        if "/login" in page.url:
            _manual(page, "Claire에 로그인하세요", lambda u: "/login" not in u and "/oauth" not in u)
        _english_ui(page, r); _ensure_org(page, r)
        rec = ScreenRec(f"google-review-{part}-tail", _window_rect(page))
        try:
            if part == "dv360":
                dv360_usage(page, r)
            else:  # 5 → 9
                google_ads_usage(page, r)
                disconnect(page, r, "Google Ads")
                r.click(page.get_by_role("link", name="Campaigns", exact=True).first)
                r.prep(); r.hold("캠페인 Disconnected 상태", 3000)
                page.goto("https://myaccount.google.com/connections")
                _manual(page, "Google 계정 → 보안 → 타사 앱 목록에서 Claire가 없는 것을 보여 준 뒤, 주소창에 claire.infinit-c.com 을 쳐서 돌아오면 녹화가 끝납니다",
                        lambda u: u.startswith(BASE))
                page.wait_for_timeout(2000)
        finally:
            rec.stop()
            ctx.close()


def cleanup():
    with sync_playwright() as p:
        ctx, page = _ctx(p, headed=False)
        for name in ("Google Ads", "DV360|Display"):
            page.goto(BASE + "/platform-integrations", wait_until="networkidle"); page.wait_for_timeout(1500)
            row = page.locator("tr", has_text=re.compile(name))
            if not row.count():
                print(name, "없음"); continue
            row.get_by_role("button").last.click()
            page.get_by_role("menuitem", name=re.compile("Disconnect|연결 끊기")).click()
            page.get_by_role("button", name=re.compile("^(Continue|계속)$")).click()
            page.wait_for_timeout(4000); print(name, "해제")
        ctx.close()


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    arg = sys.argv[2] if len(sys.argv) > 2 else "dv360"
    if mode == "record":
        record(arg)
    elif mode == "record_tail":
        record_tail(arg)
    elif mode == "cleanup":
        cleanup()
    else:
        print(__doc__)
