#!/usr/bin/env python3
"""Meta 앱 심사용 스크린캐스트: 로그인 → Meta 연동(OAuth) → 계정·캠페인 선택 → 대시보드 → 연동 해제.

사용법:
  python record_meta_review.py prep     # (촬영 전) 데모 조직의 Meta 연동을 헤드리스로 끊는다
  python record_meta_review.py cleanup  # 실패한 녹화가 남긴 캠페인·그룹 삭제 + Meta 해제
  python record_meta_review.py record   # 헤드 브라우저 녹화. Claire 로그인과 Facebook 로그인·동의만 직접 입력
  python record_meta_review.py restore  # (촬영 후) Meta를 다시 연결해 데모 조직을 복구

- Claire 로그인은 이메일/비밀번호로 (Google OAuth는 자동화 브라우저를 막을 수 있음).
- Facebook 화면은 블러하지 않는다 (심사 영상). Claire 화면의 광고주명·ID만 가린다.
- 출력: out/meta-review.mp4
"""
import re
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from capture import BASE, PROFILE, SENSITIVE, _wide_range
from record_test import AUTO_BLUR_JS, CAPTION_JS, CURSOR_JS, Recorder

HERE = Path(__file__).parent
OUT = HERE / "out"
# 로그인 화면부터 담아야 하므로 기존 세션(.profile)과 분리된 프로필을 쓴다
REVIEW_PROFILE = HERE / ".profile-meta-review"
MANUAL = 10 * 60 * 1000  # 사용자가 직접 입력하는 단계의 대기 한도


def _ctx(p, headed, record=False):
    kw = dict(headless=not headed, viewport={"width": 1440, "height": 900},
              locale="ko-KR", timezone_id="Asia/Seoul")
    if record:
        kw.update(record_video_dir=str(OUT), record_video_size={"width": 1440, "height": 900})
    ctx = p.chromium.launch_persistent_context(REVIEW_PROFILE if headed else PROFILE, **kw)
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.on("dialog", lambda d: d.accept())  # Disconnect의 window.confirm
    return ctx, page


class ReviewRecorder(Recorder):
    def prep(self, wait=1800):
        self.page.wait_for_timeout(wait)
        if self.page.url.startswith(BASE):  # Facebook 페이지는 그대로 보여준다
            self.page.evaluate(AUTO_BLUR_JS, SENSITIVE)
            self.page.evaluate(CURSOR_JS)


class Silent:
    """restore 모드: 자막·커서 없이 같은 흐름을 돈다."""
    def __init__(self, page):
        self.page = page

    def prep(self, wait=1200):
        self.page.wait_for_timeout(wait)

    def caption(self, text, hold=0):
        print("  ·", text)

    def click(self, locator, settle=500):
        locator.scroll_into_view_if_needed()
        locator.click()
        self.page.wait_for_timeout(settle)


# 데모 조직에 원래 붙어 있던 광고 계정만 고른다 — 전체 선택하면 실제 광고주 계정이 다 들어온다 (실사고)
DEMO_ACCOUNTS = ["택산가든", "키세카츠"]


def _check_rows(page, r, names=None):
    """표의 체크박스를 켠다. names가 있으면 그 이름이 들어간 행만."""
    rows = page.locator("tr").filter(has=page.get_by_role("checkbox"))
    n = 0
    for i in range(rows.count()):
        row = rows.nth(i)
        if names and not any(nm in row.inner_text() for nm in names):
            continue
        box = row.get_by_role("checkbox")
        if box.get_attribute("aria-checked") != "true":
            r.click(box, settle=250)
            _accept_restore(page, r)
        n += 1
    return n


def _accept_restore(page, r):
    """'Restore existing campaigns?' 모달이 뜨면 Restore. 모달이 떠 있는 동안은 뒤 화면이 role 조회에서 빠진다."""
    btn = page.get_by_role("button", name=re.compile(r"Restore campaigns"))
    try:
        btn.wait_for(timeout=1500)
        r.click(btn)
        page.wait_for_timeout(800)
    except Exception:
        pass


def connect_meta(page, r):
    """Platform Integrations → Connect → Meta → OAuth(수동) → 계정·캠페인 선택 → Finish setup."""
    r.caption("Settings → Platform Integrations", 900)
    r.click(page.get_by_role("link", name="Platform Integrations"))
    r.prep()
    r.caption("Click [Connect] to add an advertising platform", 1200)
    r.click(page.get_by_role("link", name="Connect").first)
    r.prep()
    r.caption("Step 1 — Select Meta", 800)
    r.click(page.get_by_role("radio", name="Meta"))
    page.wait_for_timeout(500)
    r.click(page.get_by_role("button", name="Continue"))
    r.prep(1200)
    r.caption("Step 2 — Authorize Meta (Facebook Login)", 1500)
    r.click(page.get_by_role("button", name=re.compile(r"^Authorize")))
    print(">> Facebook 로그인과 권한 동의를 브라우저에서 직접 진행하세요 (최대 10분)")
    page.wait_for_url(re.compile(re.escape(BASE) + r"/platform-integrations/new\?.*step=accounts"), timeout=MANUAL)
    r.prep(2500)
    r.caption("Step 3 — Select ad accounts to import", 800)
    page.get_by_role("checkbox").first.wait_for(timeout=60_000)
    assert _check_rows(page, r, DEMO_ACCOUNTS), "데모 계정이 목록에 없음"
    r.click(page.get_by_role("button", name=re.compile(r"Import accounts")))
    page.wait_for_url(re.compile(r"step=campaigns"), timeout=120_000)
    r.prep(2500)
    r.caption("Step 4 — Select campaigns", 800)
    page.get_by_role("checkbox").first.wait_for(timeout=120_000)
    # 계정이 여럿이면 계정 탭(Step i of n)을 돌며 각 계정의 캠페인을 모두 고른다
    tabs = page.locator("nav[aria-label='Select accounts'] button")
    for i in range(max(1, tabs.count())):
        if tabs.count() > 1:
            r.click(tabs.nth(i))
            page.wait_for_timeout(1500)
        _check_rows(page, r)
    r.click(page.get_by_role("button", name=re.compile(r"Finish setup")))
    _accept_restore(page, r)
    page.wait_for_url(lambda u: "/platform-integrations/new" not in u, timeout=120_000)
    r.prep(2000)


def prep_page(page):
    page.goto(BASE + "/platform-integrations", wait_until="networkidle")
    row = page.locator("tr", has_text="Meta")
    if not row.count():
        print("Meta가 연결돼 있지 않음 — 건너뜀"); return
    row.get_by_role("button").last.click()  # 행 ⋮ 메뉴
    page.get_by_role("menuitem", name="Disconnect").click()
    page.wait_for_timeout(4000)
    print("Meta 연동 해제 완료:", page.inner_text("main").replace("\n", " | ")[-80:])


def prep():
    with sync_playwright() as p:
        ctx, page = _ctx(p, headed=False)
        prep_page(page)
        ctx.close()


def _row_menu(page, want):
    """상세 화면 우상단 ⋮ 메뉴에서 want 항목을 누른다. 없으면 False."""
    page.locator("main button[aria-haspopup='menu']").first.click()
    page.wait_for_timeout(600)
    item = page.get_by_role("menuitem", name=re.compile(want))
    if not item.count():
        page.keyboard.press("Escape")
        return False
    item.first.click()
    page.wait_for_timeout(3000)
    return True


def cleanup():
    """실패한 녹화가 남긴 흔적 제거: 잘못 등록된 캠페인·그룹 삭제 후 Meta 해제(계정 전체 제거)."""
    with sync_playwright() as p:
        ctx, page = _ctx(p, headed=False)
        page.goto(BASE + "/campaigns", wait_until="networkidle"); page.wait_for_timeout(2000)
        row = page.locator("tr", has_text="260421")
        if row.count():
            row.get_by_role("link").first.click(); page.wait_for_timeout(2500)
            print("campaign delete:", _row_menu(page, "Delete"))
        page.goto(BASE + "/campaign-groups", wait_until="networkidle"); page.wait_for_timeout(2000)
        row = page.locator("tr", has_text="대한상공회의소")
        if row.count():
            row.get_by_role("link").first.click(); page.wait_for_timeout(2500)
            print("group disable:", _row_menu(page, "Disable"), "delete:", _row_menu(page, "Delete"))
        prep_page(page)
        ctx.close()


def restore():
    with sync_playwright() as p:
        ctx, page = _ctx(p, headed=True)
        page.goto(BASE, wait_until="networkidle")
        if "Overview" not in page.content():
            print(">> Claire에 로그인하세요"); page.wait_for_url(lambda u: "/login" not in u, timeout=MANUAL)
        connect_meta(page, Silent(page))
        print("복구 완료:", page.url)
        ctx.close()


def _finish_video(page, ctx, name):
    video = page.video
    ctx.close()
    webm = OUT / f"{name}.webm"
    webm.unlink(missing_ok=True)
    Path(video.path()).rename(webm)
    mp4 = OUT / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(webm),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", str(mp4)], check=True)
    print(f"saved: {mp4}")


def tail(page, r):
    """대시보드 이후: 캠페인 상세 → Platform Integrations → Disconnect."""
    r.click(page.get_by_role("button", name="Campaigns"))  # 사이드바 접힘 그룹 → 펼치기
    page.wait_for_timeout(500)
    r.click(page.get_by_role("link", name="Campaigns", exact=True).first)
    r.prep(1500)
    r.caption("Imported Meta campaigns", 1500)
    r.click(page.locator("tr", has_text="협력광고").get_by_role("link").first)
    r.prep(1500)
    r.caption("Campaign dashboard — KPI cards and trend", 3000)
    r.caption("Disconnecting Meta from the organization", 800)
    r.click(page.get_by_role("link", name="Platform Integrations"))
    r.prep()
    r.click(page.locator("tr", has_text="Meta").get_by_role("button").last)  # 행 ⋮ 메뉴
    r.click(page.get_by_role("menuitem", name="Disconnect"))
    page.wait_for_timeout(3500)
    r.prep(500)
    r.caption("Meta disconnected — campaigns stop syncing. Reconnect any time with [Connect]", 3000)
    page.evaluate(CAPTION_JS, None)
    page.wait_for_timeout(800)


def record_tail():
    """record가 대시보드까지 찍고 끊겼을 때: 로그인된 리뷰 프로필로 뒷부분만 헤드리스 녹화 (meta-review-part2)."""
    with sync_playwright() as p:
        kw = dict(headless=True, viewport={"width": 1440, "height": 900}, locale="ko-KR", timezone_id="Asia/Seoul",
                  record_video_dir=str(OUT), record_video_size={"width": 1440, "height": 900})
        ctx = p.chromium.launch_persistent_context(REVIEW_PROFILE, **kw)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.on("dialog", lambda d: d.accept())
        r = ReviewRecorder(page)
        page.goto(BASE + "/", wait_until="networkidle")
        _wide_range(page)
        r.prep(1500)
        r.caption("Impressions, clicks and media cost pulled via the Marketing API (ads_read)", 2500)
        tail(page, r)
        _finish_video(page, ctx, "meta-review-part2")


def record():
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        ctx, page = _ctx(p, headed=True, record=True)
        r = ReviewRecorder(page)

        # 1. 로그인 (사용자 직접)
        page.goto(BASE, wait_until="networkidle")
        page.evaluate(CAPTION_JS, "Log in to Claire")
        print(">> Claire에 이메일/비밀번호로 로그인하세요 — 그 뒤로는 아무것도 누르지 마세요")
        # 사이드바 문구는 계정 권한에 따라 다르다 — 로그인 화면을 벗어나는 것으로 판단
        page.wait_for_url(lambda u: u.startswith(BASE) and "/login" not in u and "/oauth" not in u, timeout=MANUAL)
        page.wait_for_load_state("networkidle")
        r.prep(2000)
        lang = page.get_by_role("button", name="언어 변경")  # 심사용이라 영어 UI로
        if lang.count():
            r.click(lang)
            r.click(page.get_by_role("menuitem", name="영어"))
            page.wait_for_load_state("networkidle")
            r.prep(1500)
        r.caption("Claire dashboard after login", 1500)

        # 2~3. 연동 (Facebook 로그인·동의만 사용자 직접)
        connect_meta(page, r)
        r.caption("Meta campaigns are now registered", 2000)

        # 4. 대시보드 성과
        r.caption("Dashboard — performance metrics from Meta campaigns", 800)
        page.goto(BASE + "/", wait_until="networkidle")
        _wide_range(page)  # 데모 데이터가 오래돼 기본 24시간은 비어 있다
        r.prep(2000)
        r.caption("Impressions, clicks and media cost pulled via the Marketing API (ads_read)", 3000)
        tail(page, r)
        _finish_video(page, ctx, "meta-review")


if __name__ == "__main__":
    {"prep": prep, "cleanup": cleanup, "record": record, "record_tail": record_tail, "restore": restore}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: print(__doc__))()
