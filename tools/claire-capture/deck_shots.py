#!/usr/bin/env python3
"""내부 회의 덱용 콘솔 캡처 (ops/DECK_SCREENSHOT_PROMPT_20261021_KO.md).

사용법: python deck_shots.py [번호...]   # 기본: 1 2 (3~5는 10/20 배포 후)
- 로그인은 사용자가 헤드 브라우저에서 직접 한다. 화면은 읽기만 하고 메뉴는 열어 보여준 뒤 닫는다.
- 뷰포트 1600×1180, 한국어 UI로 찍고 끝나면 원래 언어로 되돌린다.
- 출력: ~/Downloads/claire-deck-shots/0N-*.png
"""
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from capture import BASE, BLUR_JS, PROFILE, SENSITIVE

OUT = Path.home() / "Downloads" / "claire-deck-shots"
MANUAL = 10 * 60 * 1000


EMAIL_BLUR_JS = """
(keep) => {
  const re = /[\\w.+-]+@[\\w-]+\\.[\\w.-]+/;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n, hits = 0;
  while ((n = walker.nextNode())) {
    const t = n.textContent || '';
    if (re.test(t) && !keep.some((k) => t.includes(k)) && n.parentElement) { n.parentElement.style.filter = 'blur(7px)'; hits++; }
  }
  return hits;
}
"""
KEEP_EMAILS = ["jh.yoon@infinit-c.com"]  # 우리 수신 주소는 그대로 둔다


def _shot(page, name):
    page.wait_for_timeout(800)
    page.evaluate(BLUR_JS, SENSITIVE)
    page.evaluate(EMAIL_BLUR_JS, KEEP_EMAILS)
    page.screenshot(path=str(OUT / name))
    print("✓", name)


def _open_row_menu(page, row):
    """행 오른쪽 ⋮ 메뉴를 연다. 메뉴 항목 목록을 돌려준다."""
    row.get_by_role("button").last.click()
    page.wait_for_timeout(600)
    return page.get_by_role("menuitem").all_inner_texts()


def _set_language(page, want):
    """헤더 언어 메뉴에서 want(한국어/영어)를 고른다. 바꿨으면 이전 언어 이름을 돌려준다."""
    btn = page.get_by_role("button", name=re.compile("언어 변경|Change language"))
    if not btn.count():
        return None
    btn.first.click()
    page.wait_for_timeout(500)
    items = page.get_by_role("menuitem")
    names = items.all_inner_texts()
    current_ko = any(n in ("한국어", "영어") for n in names)  # 메뉴가 한국어면 현재 UI가 한국어
    target = {"ko": ("한국어", "Korean"), "en": ("영어", "English")}[want]
    if (want == "ko") == current_ko:
        page.keyboard.press("Escape")
        return None
    items.filter(has_text=re.compile("|".join(target))).first.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1500)
    return "en" if want == "ko" else "ko"


def shot_alerts(page):
    page.goto(BASE + "/alerts", wait_until="networkidle")
    page.wait_for_timeout(2000)
    rows = page.locator("tbody tr")
    note = None
    if rows.count() and rows.first.get_by_role("button").count():
        items = _open_row_menu(page, rows.first)
        if not any(("끄기" in i or "켜기" in i) for i in items):
            note = f"행 메뉴에 끄기/켜기 없음: {items}"
    else:
        note = "알림이 없어 빈 목록으로 캡처"
    _shot(page, "01-alerts.png")
    page.keyboard.press("Escape")
    return note


def shot_users(page):
    page.goto(BASE + "/org/users", wait_until="networkidle")
    page.wait_for_timeout(2000)
    note = None
    invited = page.locator("tbody tr", has_text=re.compile("초대됨|Invited"))
    row = invited.first if invited.count() else page.locator("tbody tr").first
    if not invited.count():
        note = "초대됨 상태 사용자가 없어 첫 행 메뉴로 대체"
    if row.count() and row.get_by_role("button").count():
        items = _open_row_menu(page, row)
        if invited.count() and not any("초대 취소" in i for i in items):
            note = f"행 메뉴에 초대 취소 없음: {items}"
    _shot(page, "02-users.png")
    page.keyboard.press("Escape")
    return note


SUMMARY_NAME = "주간 성과 요약"
# DV360는 비용 지표가 spend가 아니라 media_cost (alert.service.ts 참고). 기본 템플릿의 spend는 DV360에서 미리보기가 실패한다.
SUMMARY_DOC = """@metric media_cost = raw("media_cost", period="last_7_days")
@metric impressions = raw("impressions", period="last_7_days")
@metric clicks = raw("clicks", period="last_7_days")

# {{summary.name}}
**{{campaign.name}}** · 최근 7일

- 미디어 비용: {{media_cost.current}} (전주 대비 {{media_cost.change}})
- 노출: {{impressions.current}} ({{impressions.change}})
- 클릭: {{clicks.current}} ({{clicks.change}})
"""
CHAT_Q = "이 캠페인 최근 7일 성과를 일별로 요약하고 눈에 띄는 점을 알려줘"


def shot_summary(page, group, campaign):
    """새 맞춤 요약 편집기: 대상 선택 → 마크다운 모드에 지표 3개 문서 → 미리보기 탭. 저장하지 않는다."""
    from admin_shots import _pick  # 순환 import 회피
    page.goto(BASE + "/custom-summaries/new", wait_until="networkidle")
    page.wait_for_timeout(2000)
    _pick(page, "customSummaryCampaignGroup", group); page.wait_for_timeout(800)
    _pick(page, "customSummaryCampaign", campaign); page.wait_for_timeout(800)
    page.locator("input#name").fill(SUMMARY_NAME)
    page.get_by_role("button", name="마크다운").click(); page.wait_for_timeout(1200)
    ta = page.locator("main textarea").first
    ta.click(); ta.fill(SUMMARY_DOC); page.wait_for_timeout(500)
    page.get_by_text("미리보기", exact=True).first.click()
    page.wait_for_timeout(5000)
    err = page.locator("[role=status], [role=alert]").all_inner_texts()
    page.get_by_text("2. 요약 문서").scroll_into_view_if_needed(); page.wait_for_timeout(500)
    page.evaluate("window.scrollBy(0, -16)")
    _shot(page, "05-summary.png")
    note = f"미리보기 오류: {err}" if any("could not" in e or "invalid" in e.lower() for e in err) else None
    page.goto(BASE + "/custom-summaries", wait_until="networkidle")  # 저장 없이 이탈
    return note


def shot_chat(page, campaign_path, question=CHAT_Q, wait_s=150):
    """캠페인 화면의 채팅 위젯에서 새 대화를 열고 질문을 보낸 뒤 답변이 멈추면 확장 상태로 캡처한다."""
    page.goto(BASE + campaign_path, wait_until="networkidle"); page.wait_for_timeout(2500)
    page.get_by_role("button", name="채팅 열기").click(); page.wait_for_timeout(1500)
    if page.get_by_role("button", name="새로운 채팅").count():
        page.get_by_role("button", name="새로운 채팅").click(); page.wait_for_timeout(2500)
    page.get_by_role("button", name="채팅 패널 확장").click(); page.wait_for_timeout(800)
    ta = page.get_by_role("textbox", name="채팅 메시지"); ta.click(); ta.fill(question)
    page.get_by_role("button", name="메시지 보내기").click()
    import time
    t0, last = time.time(), -1
    while time.time() - t0 < wait_s:
        page.wait_for_timeout(5000)
        n = len(page.evaluate("()=>document.body.innerText"))
        if n == last and not page.get_by_role("button", name="메시지 보내기").is_disabled() and time.time() - t0 > 20:
            break
        last = n
    page.evaluate("()=>{const m=document.querySelector('[class*=overflow-y-auto]'); if(m) m.scrollTop=0}")
    _shot(page, "03-chat.png")
    body = page.evaluate("()=>document.body.innerText")
    return "채팅 실패 문구가 보임" if "전송하지 못했습니다" in body else None


SHOTS = {"1": shot_alerts, "2": shot_users}


def main(nums):
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE, headless=False, viewport={"width": 1600, "height": 1180},
            device_scale_factor=2, locale="ko-KR", timezone_id="Asia/Seoul")
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(BASE, wait_until="networkidle")
        if "/login" in page.url:
            print(">> 브라우저에서 로그인해 주세요 (최대 10분)")
            page.wait_for_url(lambda u: "/login" not in u, timeout=MANUAL)
            page.wait_for_load_state("networkidle")
        prev = _set_language(page, "ko")
        notes = {}
        for n in nums:
            fn = SHOTS.get(n)
            if not fn:
                notes[n] = "10/20 배포 후 캡처 가능 — 이번엔 건너뜀"
                continue
            notes[n] = fn(page)
        if prev:
            _set_language(page, prev)
        ctx.close()
    print("\n저장 위치:", OUT)
    for n, note in notes.items():
        print(f"  {n}: {note or 'OK'}")


if __name__ == "__main__":
    main(sys.argv[1:] or ["1", "2"])
