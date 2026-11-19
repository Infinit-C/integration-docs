#!/usr/bin/env python3
"""Claire 대시보드 가이드 캡처 도구.

사용법:
  python capture.py login   # 헤드 브라우저가 뜬다 → 직접 로그인 (세션은 .profile/에 저장)
  python capture.py shoot [이름...]   # 가이드 캡처 일괄 생성 (기본: 전체)

- 출력: ../../static/img/claire/{이름}.png (뷰포트 1440x900, 2x 스케일)
- 민감 정보(광고주명·계정 ID·URN·사용자명)는 캡처 직전에 블러 CSS를 주입해 가린다.
  광고주/캠페인이 늘면 SENSITIVE 목록에 추가할 것.
"""
import os
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = os.environ.get("CLAIRE_BASE", "https://claire.infinit-c.com")  # 공개 도메인이 막히면 CLAIRE_BASE=http://100.93.154.57:13020
HERE = Path(__file__).parent
# gitignore 대상 — 절대 커밋 금지. 다른 계정은 CLAIRE_PROFILE=.profile-admin 처럼 바꿔 쓴다
PROFILE = HERE / os.environ.get("CLAIRE_PROFILE", ".profile")
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
  // 12자리 이상 숫자열 = 매체 계정·캠페인 ID로 간주해 무조건 블러
  // (개별 문자열 나열은 새 캠페인이 생기면 누락된다 — 실사고)
  const hit = (t) => words.some((w) => t.includes(w)) || /\\d{12,}/.test(t);
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walker.nextNode())) {
    const t = n.textContent || '';
    if (hit(t)) {
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
    page.get_by_role("tab", name=re.compile(name)).click()
    page.wait_for_timeout(1500)


def _open_chat(page):
    page.get_by_role("button", name=re.compile("Open chat|채팅 열기")).click()
    page.wait_for_timeout(2500)
    # 이전 대화가 있으면 '기존 채팅 이어가기 / 새로운 채팅' 선택 화면이 먼저 뜬다
    new_chat = page.get_by_role("button", name="새로운 채팅")
    if new_chat.count():
        new_chat.click()
        page.wait_for_timeout(2000)


def _wide_range(page):
    """대시보드 기간 기본값(최근 24시간)은 데모 데이터가 오래돼 빈 차트가 된다 → 기간 선택기에서 '최근 1년'을 골라 찍는다.
    (선택은 localStorage에 저장돼 캠페인·그룹·홈 대시보드에 함께 적용된다.)"""
    btn = page.locator("main button").filter(has_text=re.compile("최근|지난|Last|이전")).first
    if not btn.count():
        return
    btn.click()
    page.wait_for_timeout(700)
    tab = page.get_by_text(re.compile("^(최근 기간|Relative)$")).first
    if tab.count():
        tab.click()
        page.wait_for_timeout(300)
    opt = page.get_by_text(re.compile("^(최근 1년|Last 1 year|Last year|Past 1 year)$")).first
    if opt.count():
        opt.click()
        page.wait_for_timeout(300)
    apply = page.get_by_role("button", name=re.compile("^(적용|Apply)$"))
    if apply.count():
        apply.last.click()
    else:
        page.keyboard.press("Escape")
    page.wait_for_timeout(3500)


def _viz_range(page):
    """시각화 편집기는 프리셋이 최근 3개월까지라 데모 데이터(7~8월)가 안 보인다 → 날짜 입력칸에 직접 넣고 새로고침."""
    dates = page.locator("main input[type=date]")
    if dates.count() >= 2:
        dates.nth(0).fill("2026-07-01")
        dates.nth(1).fill("2026-08-31")
        page.get_by_role("button", name=re.compile("^(새로고침|Refresh)$")).first.click()
        page.wait_for_timeout(3500)


def _campaign_dashboard(page):
    _click_tab(page, "^(Dashboard|대시보드)$")
    _wide_range(page)


def _campaign_edit(page):
    page.get_by_text(re.compile("^4\\. 수집 일정|Collection schedule")).first.scroll_into_view_if_needed()
    page.mouse.wheel(0, -120)
    page.wait_for_timeout(500)


def _share_dialog(page, title="협력광고 7~8월 성과 보고서", per_campaign=False):
    """보고서 링크 대화상자를 열어 채운다 (만들지는 않음). AI 채팅 on, 함께 보기 CTR+클릭, 기간 지정 7/1~8/31."""
    page.get_by_role("button", name=re.compile("보고서 링크")).first.click(); page.wait_for_timeout(2000)
    d = page.locator("[role=dialog]").first
    d.get_by_placeholder("예: 월간 성과 보고서").fill(title)
    d.get_by_placeholder("리포트를 받는 분께 전할 내용을 입력하세요").fill("7~8월 캠페인 성과입니다. 8월 셋째 주부터 CTR이 개선됐습니다.")
    sw = d.get_by_label("리포트 관련 AI 채팅 활성화").first
    if sw.get_attribute("aria-checked") != "true": sw.click()
    if per_campaign:
        pc = d.get_by_label("캠페인별")
        if pc.count() and pc.first.get_attribute("aria-checked") != "true": pc.first.click()
    for m in ("CTR", "클릭"): d.locator("label", has_text=re.compile(f"^{m}$")).last.click()
    ads = d.get_by_label("소재 성과 포함")
    if ads.count() and ads.first.get_attribute("aria-checked") != "true": ads.first.click(); page.wait_for_timeout(300)
    d.get_by_role("combobox").filter(has_text=re.compile("최근 7일")).first.click(); page.wait_for_timeout(300); page.get_by_role("option", name="기간 지정").click(); page.wait_for_timeout(500)
    dates = d.locator("input[type=date]"); dates.nth(0).fill("2026-07-01"); dates.nth(1).fill("2026-08-31")
    page.wait_for_timeout(300)
    d.evaluate("e => { e.scrollTop = 0 }"); page.wait_for_timeout(400)  # 폼 위쪽이 보이게 (아래의 끊긴 테스트 링크 목록은 가린다)
    return d


def _collect_dialog(page):
    """상세 ⋮ → 지금 수집 대화상자 (캠페인 전체 기간 버튼 포함)."""
    page.get_by_role("button", name=re.compile("캠페인 대시보드 작업|^작업")).first.click(); page.wait_for_timeout(500)
    page.get_by_role("menuitem", name=re.compile("지금 수집")).click(); page.wait_for_timeout(1200)


def _google_hint(page):
    """연결 위저드에서 Google Ads 선택 → 인증 단계 (확인되지 않은 앱 안내)."""
    page.locator("main").get_by_text(re.compile("^Google Ads$")).first.click(); page.wait_for_timeout(500)
    page.get_by_role("button", name=re.compile("^계속$")).first.click(); page.wait_for_timeout(1500)


def _share_page(page):
    """링크를 실제로 만들어 공개 보고서 페이지를 찍고, 찍은 뒤 바로 끊는다 (끊긴 링크는 목록에 남는다)."""
    from admin_shots import _api
    d = _share_dialog(page)
    created = {}
    page.on("response", lambda r: created.update(r.json().get("data", {})) if "report-shares" in r.url and r.request.method == "POST" and r.status == 201 else None)
    d.get_by_role("button", name="링크 만들기").click(); page.wait_for_timeout(3500)
    if not created.get("token"):
        print("  !! 링크 생성 실패"); return False
    page.goto(BASE + "/share/" + created["token"], wait_until="networkidle"); page.wait_for_timeout(4000)
    page.evaluate(BLUR_JS, SENSITIVE); page.wait_for_timeout(500)
    page.screenshot(path=str(OUT / "report-share-page-full.png"), full_page=True)
    page.get_by_role("button", name="리포트에 대해 질문하기").click(); page.wait_for_timeout(1200)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)"); page.wait_for_timeout(800)
    page.screenshot(path=str(OUT / "report-share-page-chat.png"))
    page.get_by_role("button", name=re.compile("닫기|Close")).last.click(); page.wait_for_timeout(300)
    page.evaluate("window.scrollTo(0, 0)"); page.wait_for_timeout(500)
    status, _ = _api(page, "POST", f"/report-shares/{created['code']}/revoke")
    print("  revoke:", status)


def _creatives_tab(page):
    _click_tab(page, "^소재$")
    cb = page.locator("main").get_by_role("combobox").first
    if cb.count():
        cb.click(); page.wait_for_timeout(300)
        o = page.get_by_role("option", name="최근 90일")
        if o.count(): o.click(); page.wait_for_timeout(3000)


def _bulk_edit(page):
    page.locator("tbody tr").first.locator("[role=checkbox]").first.click(); page.wait_for_timeout(600)
    page.get_by_role("button", name=re.compile(r"^작업 \(")).click(); page.wait_for_timeout(500)
    page.get_by_role("menuitem", name=re.compile("일괄 편집")).click(); page.wait_for_timeout(1500)


def _team_history(page):
    page.get_by_text("팀 이력").first.scroll_into_view_if_needed(); page.wait_for_timeout(800)


def _first_detail(page):
    link = page.get_by_role("link", name=re.compile("View details|상세 보기|자세히")).first
    if not link.count():
        print("  (목록이 비어 있어 상세 캡처 생략)")
        return False
    link.click()
    page.wait_for_timeout(2500)


# (이름, 경로, 페이지 로드 후 액션)
SHOTS = [
    ("dashboard", "/", _wide_range),  # 홈은 기본 대시보드로 리다이렉트
    ("dashboards-list", "/dashboards", None),
    ("visualizations", "/visualizations", None),
    ("visualization-editor", "/visualizations/78949445", _viz_range),  # 데모 시각화 편집기
    ("campaign-groups", "/campaign-groups", None),
    ("campaign-group-detail", "/campaign-groups/82936400", _wide_range),
    ("campaign-group-campaigns", "/campaign-groups/82936400",
     lambda p: _click_tab(p, "^(Campaigns|캠페인)$")),
    ("campaign-detail", "/campaigns/83901859", lambda p: _click_tab(p, "^(Details|상세 정보)$")),
    # 2026-09 개편: KPI·Trends 탭 → Dashboard 탭 하나로 합쳐졌고 KPI 설정은 별도 화면
    ("campaign-trends", "/campaigns/83901859", _campaign_dashboard),
    ("campaign-kpi", "/campaigns/83901859/kpis/edit", None),
    ("campaign-edit", "/campaigns/83901859/edit", _campaign_edit),  # 수집 일정 섹션
    ("report-link-dialog", "/campaigns/83901859", _share_dialog),
    ("report-share-page", "/campaigns/83901859", _share_page),  # 공개 페이지 (full/chat 파일을 따로 저장)
    ("campaigns-bulk-edit", "/campaigns", _bulk_edit),
    ("collect-dialog", "/campaigns/83901859", _collect_dialog),
    ("platform-connect-google", "/platform-integrations/new", _google_hint),
    ("company-settings", "/company-settings", None),
    ("team-history", "/org/users", _team_history),
    ("chat-panel", "/campaigns/83901859", _open_chat),
    ("campaigns-list", "/campaigns", None),
    ("my-chats", "/my-chats", None),
    ("metric-categories", "/metric-categories", None),
    ("metric-formulas", "/metric-formulas", None),
    ("kpi-rules", "/kpis", None),
    ("alerts", "/alerts", None),
    ("custom-summaries", "/custom-summaries", None),
    ("custom-summary-new", "/custom-summaries/new", None),
    ("custom-summary-detail", "/custom-summaries", _first_detail),
    ("reports", "/reports", None),
    ("organization-settings", "/organization-settings", None),
        ("platform-integrations", "/platform-integrations", None),
    ("platform-accounts", "/platform-integrations/meta/accounts", None),
    ("platform-connect", "/platform-integrations/new", None),
    ("communication-groups", "/communication-groups", None),
    ("security-users", "/org/users", None),
    ("api-keys", "/api-keys", None),
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
        # 첫 진입 시 "/"가 /login으로 넘어가기 전에 조건을 통과하는 경합이 있어 사이드바 링크로 판단한다
        page.wait_for_selector("a[href^='/dashboards'], a[href='/my-chats']", timeout=600_000)
        page.wait_for_load_state("networkidle")
        # 토큰이 디스크에 내려가기 전에 닫으면 세션이 날아간다 — 한 번 더 열어 저장을 확인한 뒤 닫는다
        page.wait_for_timeout(4000)
        page.goto(BASE, wait_until="networkidle")
        page.wait_for_timeout(3000)
        if "/login" in page.url:
            print("!! 로그인 상태가 유지되지 않음 — 다시 시도"); ctx.close(); sys.exit(1)
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
            if action and action(page) is False:
                continue
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
