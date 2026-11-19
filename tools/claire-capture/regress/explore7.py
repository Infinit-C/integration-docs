"""11/19 오후 추가 기능 점검 (PoC 3차). 읽기 위주 + AUDIT-TEST 보고서 링크 1개 생성/수정/끊기."""
import re, sys, json, time
sys.path.insert(0, "/Users/yoonjaehyon/dev/integration-docs/tools/claire-capture/regress")
import wt
from wt import run, toast, dlg, main_text, rows
from capture import BASE
wt.OUT = "out/explore7"
R = {}
CAMP = "83901859"

def sh(pg, n): pg.screenshot(path=f"{wt.OUT}/{n}.png", full_page=True)

def main(pg):
    if "/login" in pg.url:
        R["login"] = "EXPIRED"; print("SESSION EXPIRED"); return
    # 1. 캠페인 목록: 검색 placeholder, 플랫폼/계정 필터, 즉시 검색
    pg.goto(BASE + "/campaigns", wait_until="networkidle"); pg.wait_for_timeout(1500)
    R["campaigns_placeholder"] = pg.locator("main input").first.get_attribute("placeholder")
    sels = pg.locator("main select")
    R["campaigns_selects"] = [(s.get_attribute("aria-label"), s.locator("option").all_inner_texts()) for s in sels.all()]
    sh(pg, "campaigns-filters")
    before = len(rows(pg))
    pg.locator("main input").first.fill("AUDIT"); pg.wait_for_timeout(1500)
    R["campaigns_instant_search"] = (before, len(rows(pg)), main_text(pg, 400))
    pg.locator("main input").first.fill(""); pg.wait_for_timeout(1000)
    # 잘못된 조건식 → 오류 위치
    pg.locator("main input").first.fill("campaign.name:"); pg.get_by_role("button", name="적용").first.click(); pg.wait_for_timeout(1200)
    R["campaigns_query_error"] = main_text(pg, 500)
    sh(pg, "campaigns-query-error")
    pg.locator("main input").first.fill(""); pg.get_by_role("button", name="적용").first.click(); pg.wait_for_timeout(1000)
    if len(sels.all()) > 1:
        sels.nth(1).select_option(index=1); pg.wait_for_timeout(1500)
        R["campaigns_account_filter"] = (sels.nth(1).input_value(), len(rows(pg)))
        sh(pg, "campaigns-account-filter")
        sels.nth(1).select_option(index=0); pg.wait_for_timeout(800)
    # 2. 캠페인 그룹 목록 검색
    pg.goto(BASE + "/campaign-groups", wait_until="networkidle"); pg.wait_for_timeout(1200)
    R["groups_placeholder"] = pg.locator("main input").first.get_attribute("placeholder")
    b = len(rows(pg)); pg.locator("main input").first.fill("zzzz-none"); pg.wait_for_timeout(1500)
    R["groups_instant_search"] = (b, len(rows(pg)))
    # 3. 캠페인 상세: 지금 수집 → 전체 기간 버튼, 소재 탭
    pg.goto(BASE + f"/campaigns/{CAMP}", wait_until="networkidle"); pg.wait_for_timeout(1500)
    pg.get_by_role("button", name=re.compile("캠페인 대시보드 작업|작업")).first.click(); pg.wait_for_timeout(500)
    R["detail_menu"] = pg.get_by_role("menuitem").all_inner_texts()
    pg.get_by_role("menuitem", name=re.compile("지금 수집")).click(); pg.wait_for_timeout(1200)
    d = pg.locator("[role=dialog]").first
    R["collect_dialog_buttons"] = d.get_by_role("button").all_inner_texts()
    fb = d.get_by_role("button", name=re.compile("전체 기간"))
    if fb.count():
        inputs_before = [i.input_value() for i in d.locator("input").all()]
        fb.click(); pg.wait_for_timeout(600)
        R["collect_full_period"] = (inputs_before, [i.input_value() for i in d.locator("input").all()], d.inner_text()[:400].replace("\n"," | "))
        sh(pg, "collect-full-period")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
    tabs = pg.get_by_role("tab").all_inner_texts(); R["detail_tabs"] = tabs
    t = pg.get_by_role("tab", name=re.compile("소재"))
    if t.count():
        t.click(); pg.wait_for_timeout(2500)
        R["ads_tab_text"] = main_text(pg, 900)
        sh(pg, "ads-tab")
        hdr = pg.locator("main table thead th button, main table thead th [role=button]")
        R["ads_sortable_headers"] = hdr.all_inner_texts()
        if hdr.count():
            hdr.first.click(); pg.wait_for_timeout(600); a1 = pg.locator("main table thead th").all_inner_texts()
            hdr.first.click(); pg.wait_for_timeout(600); a2 = pg.locator("main table thead th").all_inner_texts()
            R["ads_sort_toggle"] = (a1, a2)
    # 4. 보고서 링크 dialog: 소재 성과, 토스트, 끊은 링크 접기
    pg.goto(BASE + f"/campaigns/{CAMP}", wait_until="networkidle"); pg.wait_for_timeout(1500)
    pg.locator("main button, main a").filter(has_text=re.compile("보고서 링크")).first.click(); pg.wait_for_timeout(1200)
    d = pg.locator("[role=dialog]").first
    R["share_dialog_text"] = d.inner_text()[:2500].replace("\n", " | ")
    R["share_dialog_buttons"] = d.get_by_role("button").all_inner_texts()
    sh(pg, "share-dialog-top")
    inc = d.get_by_label(re.compile("소재 성과"), exact=False)
    R["share_ads_include_found"] = inc.count()
    if inc.count():
        inc.first.check(); pg.wait_for_timeout(500)
        combos = d.get_by_role("combobox").all()
        R["share_ads_combos"] = [c.inner_text() for c in combos]
        sh(pg, "share-dialog-ads")
    d.get_by_placeholder(re.compile("월간 성과")).fill("AUDIT-TEST 소재 포함 링크")
    sw = d.get_by_label(re.compile("AI 채팅"), exact=False)
    if sw.count(): sw.first.click()
    d.get_by_role("button", name=re.compile("^링크 만들기")).click(); pg.wait_for_timeout(2500)
    R["share_create_toast"] = toast(pg)
    txt = d.inner_text(); m = re.search(r"https?://\S+/share/\S+", txt)
    url = m.group(0) if m else None; R["share_url"] = bool(url)
    R["share_links_section"] = txt[txt.find("만든 링크"):][:700].replace("\n", " | ")
    sh(pg, "share-dialog-after-create")
    hide = d.get_by_role("button", name=re.compile("끊김|끊은|만료"))
    R["share_inactive_toggle"] = hide.all_inner_texts()
    if hide.count():
        hide.first.click(); pg.wait_for_timeout(500); R["share_inactive_expanded"] = d.inner_text().count("끊김")
        hide.first.click(); pg.wait_for_timeout(300)
    # 수정 → 토스트
    ed = d.get_by_role("button", name=re.compile("^수정")).first
    ed.click(); pg.wait_for_timeout(600)
    d.get_by_placeholder(re.compile("월간 성과")).fill("AUDIT-TEST 소재 포함 링크 v2")
    d.get_by_role("button", name=re.compile("변경사항 저장")).click(); pg.wait_for_timeout(2000)
    R["share_update_toast"] = toast(pg)
    # 공개 페이지
    if url:
        ctx2 = pg.context.browser.new_context(viewport={"width":1280,"height":900}, locale="ko-KR") if pg.context.browser else None
        p2 = ctx2.new_page() if ctx2 else pg.context.new_page()
        p2.goto(url, wait_until="networkidle"); p2.wait_for_timeout(3000)
        R["share_page_title"] = p2.title()
        t2 = p2.locator("body").inner_text(); R["share_page_text"] = t2[:3000].replace("\n", " | ")
        R["share_page_svg_lines"] = (p2.locator("svg path.recharts-line-curve, svg .recharts-line").count(), p2.locator("svg .recharts-bar-rectangle, svg .recharts-bar").count())
        R["share_page_imgs"] = [i.get_attribute("src")[:80] for i in p2.locator("main img, img").all()][:10]
        p2.screenshot(path=f"{wt.OUT}/share-page.png", full_page=True)
        # AI 질문 (CTR)
        qb = p2.get_by_role("button", name=re.compile("질문하기"))
        if qb.count():
            qb.first.click(); p2.wait_for_timeout(800)
            p2.get_by_placeholder(re.compile("질문")).fill("이 기간 CTR 합계는 얼마야? 숫자만 답해줘"); p2.keyboard.press("Enter")
            for _ in range(30):
                p2.wait_for_timeout(1000)
                bt = p2.locator("body").inner_text()
                if re.search(r"남은 질문|남은 횟수|\d+개 남", bt) and "%" in bt.split("숫자만 답해줘")[-1]: break
            R["share_ai_answer"] = p2.locator("body").inner_text().split("숫자만 답해줘")[-1][:600].replace("\n"," | ")
            p2.screenshot(path=f"{wt.OUT}/share-page-ai.png", full_page=True)
        p2.close()
    # 링크 끊기 → 토스트
    rv = d.get_by_role("button", name=re.compile("^링크 끊기")).first
    rv.click(); pg.wait_for_timeout(600)
    ad = pg.locator("[role=alertdialog]").last
    if ad.count(): ad.get_by_role("button", name=re.compile("링크 끊기")).click(); pg.wait_for_timeout(2000)
    R["share_revoke_toast"] = toast(pg)
    R["share_after_revoke"] = d.inner_text()[d.inner_text().find("만든 링크"):][:400].replace("\n"," | ")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
    # 5. 플랫폼 연동 새로 만들기 → Google Ads 선택 → 미확인 앱 안내
    pg.goto(BASE + "/platform-integrations/new", wait_until="networkidle"); pg.wait_for_timeout(1500)
    R["pi_new_text0"] = main_text(pg, 600)
    g = pg.locator("main").get_by_text(re.compile("Google Ads")).first
    if g.count():
        g.click(); pg.wait_for_timeout(800)
        nxt = pg.get_by_role("button", name=re.compile("다음|계속"))
        if nxt.count(): nxt.first.click(); pg.wait_for_timeout(1200)
        R["pi_google_hint"] = main_text(pg, 1500)
        sh(pg, "pi-google-unverified-hint")
    # 6. 회사 설정: 최상위 관리자 목록
    pg.goto(BASE + "/company-settings", wait_until="networkidle"); pg.wait_for_timeout(1500)
    R["company_settings"] = main_text(pg, 1500); sh(pg, "company-settings")
    # 7. 사용자 그룹 설명·정책 라벨
    for path in ["/user-groups", "/org/user-groups", "/user-groups/new"]:
        pg.goto(BASE + path, wait_until="networkidle"); pg.wait_for_timeout(1200)
        R["ug_"+path] = main_text(pg, 700)
    sh(pg, "user-groups")
    pg.goto(BASE + "/policies", wait_until="networkidle"); pg.wait_for_timeout(1200)
    R["policies"] = main_text(pg, 1200); sh(pg, "policies")

try:
    run(main)
finally:
    json.dump(R, open(f"{wt.OUT}/result.json","w"), ensure_ascii=False, indent=1)
    for k, v in R.items(): print(k, "=>", str(v)[:700])
