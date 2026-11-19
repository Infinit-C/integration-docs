"""정찰 6: 11/17 이후 추가된 화면의 실제 라벨 수집 (보고서 링크·내 데이터 전환·대시보드 탭·광고별 탭·팀 이력·약관·일괄 편집·알림 기준값·고정 기간)."""
import sys, re, json; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt
wt.OUT = "out/recon6"
R = {}
def go(pg, path, wait=1800): pg.goto(BASE+path, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(wait)
def vshot(pg, name): pg.screenshot(path=f"{wt.OUT}/{name}.png")
def btns(pg, scope="main"): return [b.strip() for b in pg.locator(f"{scope} button, {scope} a[role=button]").all_inner_texts() if b.strip()][:60]
def tabs(pg): return pg.get_by_role("tab").all_inner_texts()
def dialog(pg):
    d = pg.locator("[role=dialog]").last
    if not d.count(): return None
    return {"text": d.inner_text()[:1500].replace("\n"," | "), "buttons": d.get_by_role("button").all_inner_texts(),
            "labels": d.locator("label").all_inner_texts(), "inputs": [(i.get_attribute("type"), i.get_attribute("placeholder")) for i in d.locator("input,textarea").all()][:20],
            "switches": [(s.get_attribute("aria-label") or s.inner_text()[:30], s.get_attribute("aria-checked")) for s in d.locator("[role=switch],[role=checkbox]").all()][:20]}
def step(name, fn):
    n = len(wt.log)
    try: R[name] = fn()
    except Exception as e: R[name] = f"ERR {type(e).__name__}: {str(e)[:160]}"
    if len(wt.log) > n: R[name+" :log"] = wt.log[n:]
def t(pg):
    # 헤더 / 사용자 메뉴
    go(pg, "/", 2000)
    step("header buttons", lambda: [b.get_attribute("aria-label") or b.inner_text().strip() for b in pg.locator("header button").all()])
    step("header text", lambda: pg.locator("header").inner_text().replace("\n"," | ")[:300])
    def um():
        pg.get_by_role("button", name="사용자 메뉴 열기").click(); pg.wait_for_timeout(600)
        items = pg.get_by_role("menuitem").all_inner_texts(); vshot(pg, "user-menu"); pg.keyboard.press("Escape"); return items
    step("user menu", um)
    step("sidebar", lambda: [a.strip() for a in pg.locator("aside a, nav a").all_inner_texts() if a.strip()][:60])
    # 홈 대시보드 고정 기간 표시
    step("home dashboard main", lambda: main_text(pg, 600))
    vshot(pg, "home")
    # 보고서 링크 (캠페인)
    go(pg, "/campaigns/83901859", 2500)
    step("campaign tabs", lambda: tabs(pg))
    step("campaign buttons", lambda: btns(pg))
    def rl():
        pg.get_by_role("button", name=re.compile("보고서 링크")).first.click(); pg.wait_for_timeout(2500); vshot(pg, "report-link-campaign"); d = dialog(pg); return d
    step("report link dialog (campaign)", rl)
    def rl_more():
        d = pg.locator("[role=dialog]").last
        out = {}
        for s in d.locator("[role=switch]").all():
            lab = s.get_attribute("aria-label") or s.evaluate("e=>e.closest('label,div')?.innerText.slice(0,60)")
            out[lab] = s.get_attribute("aria-checked")
        out["comboboxes"] = [c.inner_text()[:40] for c in d.get_by_role("combobox").all()]
        out["radios"] = [r.get_attribute("aria-label") or r.evaluate("e=>e.closest('label,div')?.innerText.slice(0,60)") for r in d.get_by_role("radio").all()]
        return out
    step("report link dialog controls", rl_more)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
    # 광고별 탭
    def ads_tab():
        tb = pg.get_by_role("tab", name=re.compile("광고"))
        if not tb.count(): return "no ads tab: " + str(tabs(pg))
        tb.first.click(); pg.wait_for_timeout(3000); vshot(pg, "campaign-ads-tab"); return main_text(pg, 1200)
    step("ads tab", ads_tab)
    # 그룹 보고서 링크
    go(pg, "/campaign-groups/82936400", 2500)
    step("group tabs", lambda: tabs(pg)); step("group buttons", lambda: btns(pg))
    def grl():
        b = pg.get_by_role("button", name=re.compile("보고서 링크"))
        if not b.count(): return "no button"
        b.first.click(); pg.wait_for_timeout(2500); vshot(pg, "report-link-group"); return dialog(pg)
    step("report link dialog (group)", grl)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    # 대시보드 목록 탭
    go(pg, "/dashboards", 2000)
    step("dashboards tabs", lambda: tabs(pg)); step("dashboards main", lambda: main_text(pg, 500)); vshot(pg, "dashboards-tabs")
    # 캠페인 목록: 열 선택, 작업 → 일괄 편집
    go(pg, "/campaigns", 2500)
    step("campaign list headers", lambda: pg.locator("thead th").all_inner_texts())
    def colpick():
        pg.get_by_role("button", name=re.compile("열 선택")).click(); pg.wait_for_timeout(600)
        items = [x.strip() for x in pg.locator("[role=menu] *,[role=dialog] label,[data-radix-popper-content-wrapper] label").all_inner_texts() if x.strip()]
        items = pg.locator("[role=menuitemcheckbox],[role=menuitem],[data-radix-popper-content-wrapper] label").all_inner_texts()
        vshot(pg, "columns"); pg.keyboard.press("Escape"); return items
    step("column picker", colpick)
    def bulk():
        box = pg.locator("tbody tr").filter(has_text="협력광고").first.locator("[role=checkbox]").first
        box.click(); pg.wait_for_timeout(500)
        pg.get_by_role("button", name=re.compile("작업")).click(); pg.wait_for_timeout(500)
        items = pg.get_by_role("menuitem").all_inner_texts()
        pg.get_by_role("menuitem", name=re.compile("일괄 편집")).click(); pg.wait_for_timeout(1500); vshot(pg, "bulk-edit")
        d = dialog(pg); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        return {"menu": items, "dialog": d}
    step("bulk edit", bulk)
    # 알림 목록 헤더
    go(pg, "/alerts", 2000); step("alerts headers", lambda: pg.locator("thead th").all_inner_texts())
    # 플랫폼 연동: 팀원별 로그인
    go(pg, "/platform-integrations", 2000); step("platform main", lambda: main_text(pg, 800)); step("platform buttons", lambda: btns(pg)); vshot(pg, "platform")
    def prow():
        tr = pg.locator("tbody tr", has_text="Meta").first; tr.locator("button").last.click(); pg.wait_for_timeout(500)
        items = pg.get_by_role("menuitem").all_inner_texts(); pg.keyboard.press("Escape"); return items
    step("platform row menu", prow)
    # 팀 이력 / 구성원
    for path in ("/org/users", "/organization-settings", "/company-settings"):
        go(pg, path, 2000); step(f"{path} tabs", lambda: tabs(pg)); step(f"{path} main", lambda: main_text(pg, 500))
    def hist():
        tb = pg.get_by_role("tab", name=re.compile("이력|기록|History"))
        go(pg, "/org/users", 2000); tb = pg.get_by_role("tab", name=re.compile("이력|기록|History"))
        if not tb.count(): return "no history tab"
        tb.first.click(); pg.wait_for_timeout(2500); vshot(pg, "team-history"); return {"headers": pg.locator("thead th").all_inner_texts(), "main": main_text(pg, 800)}
    step("team history", hist)
    # 약관/개인정보
    for path in ("/terms?lang=ko", "/privacy?lang=ko"):
        go(pg, path, 1500); step(f"{path}", lambda: {"h1": pg.locator("h1").all_inner_texts(), "h2": pg.locator("h2").all_inner_texts()[:12]})
    go(pg, "/login", 1500); step("login links", lambda: [(a.inner_text(), a.get_attribute("href")) for a in pg.locator("a").all()])
    print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
run(t)
