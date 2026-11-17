"""클릭 탐색 2차: 캠페인 목록(정렬·열 선택·작업 메뉴·행 메뉴), 캠페인 상세 ⋮ 메뉴/탭/사용자 지정, 내 채팅 행 메뉴, 헤더 메뉴(검색·알림·팀 전환·계정), 시각화 유형 전환, 영문 잔존 확인."""
import sys, re, json, time; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt
from deck_shots import _set_language
wt.OUT = "out/explore"
R = {}; ERR = []
DANGER = re.compile("삭제|비활성|활성화|발송|보내기|연결 끊기|연결 해제|재수집|수집|초대|재발급|폐기|실행|로그아웃")
def go(pg, path, wait=1500): pg.goto(BASE+path, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(wait)
def vshot(pg, name): pg.screenshot(path=f"{wt.OUT}/{name}.png")
def step(pg, name, fn):
    n = len(wt.log)
    try: r = fn(); R[name] = r if r is not None else "ok"
    except Exception as e: R[name] = "ERR " + str(e).split("\n")[0][:160]; vshot(pg, "err2-" + re.sub(r"[^\w]+", "_", name)[:60])
    new = [l for l in wt.log[n:] if l[0] in ("console", "http")]
    if new: ERR.append((name, new[:4]))
def campaigns(pg):
    go(pg, "/campaigns"); out = {}
    for name in ("이름", "캠페인 그룹", "플랫폼", "기간 (시작일)"):
        b = pg.locator("thead").get_by_role("button", name=re.compile(name)); 
        if b.count(): b.first.click(); pg.wait_for_timeout(800); b.first.click(); pg.wait_for_timeout(800); out.setdefault("sorted", []).append(name)
    out["rows after sort"] = pg.locator("tbody tr").count()
    pg.get_by_role("button", name="열 선택").click(); pg.wait_for_timeout(500); out["열 선택"] = pg.evaluate("()=>[...document.querySelectorAll('[role=menu],[role=dialog],[data-radix-popper-content-wrapper]')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,300))"); pg.keyboard.press("Escape")
    tr = pg.locator("tbody tr").first; tr.locator("button").last.click(); pg.wait_for_timeout(500); out["rowmenu"] = pg.get_by_role("menuitem").all_inner_texts(); pg.keyboard.press("Escape")
    pg.locator("tbody tr input[type=checkbox]").first.check(force=True); pg.wait_for_timeout(500)
    ab = pg.get_by_role("button", name=re.compile("작업 \\(1\\)")); out["actions btn"] = ab.count()
    if ab.count(): ab.first.click(); pg.wait_for_timeout(500); out["actions menu"] = pg.get_by_role("menuitem").all_inner_texts(); pg.keyboard.press("Escape")
    pg.locator("thead input[type=checkbox]").first.check(force=True); pg.wait_for_timeout(400); out["header check"] = pg.get_by_role("button", name=re.compile("작업 \\(\\d+\\)")).first.inner_text()
    # KPI·알림 열 셀 내용
    out["row1 cells"] = [c[:30] for c in pg.locator("tbody tr").first.locator("td").all_inner_texts()]
    return out
def camp_detail(pg):
    go(pg, "/campaigns/83901859", 2500); out = {"tabs": pg.get_by_role("tab").all_inner_texts()}
    for tab in out["tabs"]: pg.get_by_role("tab", name=tab, exact=True).click(); pg.wait_for_timeout(1500); out[f"tab {tab}"] = main_text(pg, 160); out[f"tab {tab} url"] = pg.url[len(BASE):][:60]
    pg.get_by_role("tab", name=out["tabs"][0], exact=True).click(); pg.wait_for_timeout(800)
    mbs = pg.locator("main button[aria-haspopup='menu'], main button[aria-haspopup='true']"); out["menu btns"] = mbs.count()
    if not mbs.count():
        cand = [b for b in pg.locator("main button").all() if not b.inner_text().strip() and b.locator("svg").count()]
        out["icon btns"] = len(cand); mb = cand[-1] if cand else None
    else: mb = mbs.last
    if mb:
        mb.click(); pg.wait_for_timeout(500); items = pg.get_by_role("menuitem").all_inner_texts(); out["menu"] = items; vshot(pg, "camp-menu"); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        for it in items:
            if DANGER.search(it): continue
            mb.click(); pg.wait_for_timeout(400); pg.get_by_role("menuitem", name=it, exact=True).click(); pg.wait_for_timeout(2000)
            out[f"menu:{it}"] = {"url": pg.url[len(BASE):][:80], "head": main_text(pg, 200), "dialog": (dlg(pg) or [None])[0]}; vshot(pg, "camp-" + re.sub(r"\W+", "_", it)[:20])
            c = pg.locator("[role=dialog] button, main button").filter(has_text=re.compile("^(취소|닫기|Close)$"))
            if c.count(): c.first.click(); pg.wait_for_timeout(800)
            if "/campaigns/83901859" != pg.url[len(BASE):].split("?")[0]: go(pg, "/campaigns/83901859", 2000)
            d = dlg(pg)
            if d: out[f"menu:{it} leave"] = d[0][:100]; confirm(pg, "나가기|확인|계속|취소")
    b = pg.get_by_role("button", name="대시보드 사용자 지정")
    if b.count():
        b.click(); pg.wait_for_timeout(2000); out["customize btns"] = [x for x in pg.locator("main button").all_inner_texts() if x.strip()][:12]; vshot(pg, "camp-customize")
        pg.get_by_role("button", name="시각화 추가").click(); pg.wait_for_timeout(600); out["add viz menu"] = pg.get_by_role("menuitem").all_inner_texts() or pg.evaluate("()=>[...document.querySelectorAll('[role=dialog],[role=menu]')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,200))"); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        pg.get_by_role("button", name="취소").click(); pg.wait_for_timeout(800); out["after cancel"] = main_text(pg, 120)
    b = pg.get_by_role("button", name="보고서 링크"); 
    if b.count(): b.click(); pg.wait_for_timeout(800); out["보고서 링크"] = (dlg(pg) or [None])[0] or toast(pg)[:1] or pg.evaluate("()=>[...document.querySelectorAll('[role=menu],[data-radix-popper-content-wrapper]')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,200))"); vshot(pg, "camp-report-link"); pg.keyboard.press("Escape")
    return out
def chats(pg):
    go(pg, "/my-chats"); out = {}
    tr = pg.locator("tbody tr").first; tr.locator("button").last.click(); pg.wait_for_timeout(500); out["rowmenu"] = pg.get_by_role("menuitem").all_inner_texts(); pg.keyboard.press("Escape")
    tr.locator("a, td").first.click(); pg.wait_for_timeout(1500); out["detail"] = {"url": pg.url[len(BASE):][:40], "btns": [b for b in pg.locator("main button").all_inner_texts() if b.strip()][:6]}
    pg.locator("tbody tr input[type=checkbox]").first.check(force=True) if pg.locator("tbody tr input[type=checkbox]").count() else None
    go(pg, "/my-chats"); pg.locator("tbody tr input[type=checkbox]").first.check(force=True); pg.wait_for_timeout(400); ab = pg.get_by_role("button", name=re.compile("작업 \\(1\\)"))
    if ab.count(): ab.click(); pg.wait_for_timeout(400); out["actions"] = pg.get_by_role("menuitem").all_inner_texts(); pg.keyboard.press("Escape")
    return out
def header(pg):
    go(pg, "/dashboards"); out = {}
    btns = pg.locator("header button").all(); out["header btns"] = [(b.get_attribute("aria-label") or b.inner_text().strip()[:20]) for b in btns]
    for b in btns:
        lab = (b.get_attribute("aria-label") or b.inner_text().strip()[:20])
        if re.search("검색|search", lab, re.I):
            b.click(); pg.wait_for_timeout(600); out["search"] = pg.evaluate("()=>[...document.querySelectorAll('[role=dialog],[cmdk-root]')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,200))")
            pg.keyboard.type("브랜드"); pg.wait_for_timeout(1500); out["search 브랜드"] = pg.evaluate("()=>[...document.querySelectorAll('[role=dialog],[cmdk-root]')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,400))"); vshot(pg, "search"); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        elif re.search("알림|notification", lab, re.I):
            b.click(); pg.wait_for_timeout(600); out["bell"] = pg.evaluate("()=>[...document.querySelectorAll('[role=dialog],[data-radix-popper-content-wrapper],[role=menu]')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,200))"); vshot(pg, "bell"); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    pg.locator("header button").filter(has_text="Guide Organization").first.click(); pg.wait_for_timeout(500); out["org menu"] = pg.get_by_role("menuitem").all_inner_texts(); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    pg.locator("header button").filter(has_text="Jaehyon Yoon").first.click(); pg.wait_for_timeout(500); out["user menu"] = pg.get_by_role("menuitem").all_inner_texts(); vshot(pg, "user-menu"); pg.keyboard.press("Escape")
    return out
def viz(pg):
    go(pg, "/visualizations/78949445", 3000); out = {}
    cb = pg.locator("main").get_by_role("combobox").filter(has_text=re.compile("히스토그램|원형|게이지|지표|표|히트맵")).first; out["cb"] = cb.count()
    cb.click(); pg.wait_for_timeout(400); opts = pg.get_by_role("option").all_inner_texts(); out["types"] = opts; pg.keyboard.press("Escape")
    for o in opts:
        cb = pg.locator("main").get_by_role("combobox").filter(has_text=re.compile("히스토그램|원형|게이지|지표|표|히트맵")).first; cb.click(); pg.wait_for_timeout(300); pg.get_by_role("option", name=o, exact=True).click(); pg.wait_for_timeout(600)
        ap = pg.get_by_role("button", name="미리보기 적용"); en = ap.count() and ap.first.is_enabled()
        if en: ap.first.click(); pg.wait_for_timeout(2500)
        out[f"type {o}"] = {"apply": bool(en), "canvas": pg.locator("main canvas").count(), "table": pg.locator("main table").count(), "msg": [t for t in main_text(pg, 1200).split(" | ") if re.search("오류|실패|없습니다|선택", t)][:2], "toast": toast(pg)[:1]}
        vshot(pg, "viz-type-" + re.sub(r"\W+", "_", o))
    return out
def english(pg):
    _set_language(pg, "en"); out = {}
    for p in ("/campaigns", "/campaigns/83901859", "/alerts/new", "/custom-summaries/new", "/profile", "/organization-settings", "/reports/new"):
        go(pg, p, 1500); txt = main_text(pg, 4000); out[p] = sorted(set(re.findall(r"[가-힣][가-힣 ·()]{1,30}", txt)))[:8]
    vshot(pg, "en-campaign"); _set_language(pg, "ko"); return out
def dark(pg):
    go(pg, "/campaigns/83901859", 2500); out = {}
    for b in pg.locator("header button").all():
        lab = (b.get_attribute("aria-label") or "") + (b.get_attribute("title") or "")
        if re.search("dark|light|테마|모드", lab, re.I): out["btn"] = lab; b.click(); pg.wait_for_timeout(1200); break
    out["class"] = pg.evaluate("()=>document.documentElement.className")
    out["main left"] = pg.evaluate("()=>{const m=document.querySelector('main');const s=document.querySelector('aside,nav');return {main:m&&m.getBoundingClientRect().left,side:s&&s.getBoundingClientRect().width}}")
    vshot(pg, "dark2-campaign"); pg.reload(wait_until="networkidle"); pg.wait_for_timeout(2000); out["after reload"] = pg.evaluate("()=>{const m=document.querySelector('main');return m&&m.getBoundingClientRect().left}"); vshot(pg, "dark2-reload")
    for b in pg.locator("header button").all():
        lab = (b.get_attribute("aria-label") or "") + (b.get_attribute("title") or "")
        if re.search("dark|light|테마|모드", lab, re.I): b.click(); pg.wait_for_timeout(800); break
    out["restored"] = pg.evaluate("()=>document.documentElement.className"); return out
def t(pg):
    for fn in (campaigns, camp_detail, chats, header, viz, dark, english):
        step(pg, fn.__name__, lambda fn=fn: fn(pg))
    print(json.dumps(R, ensure_ascii=False, indent=1)); print("ERRORS", json.dumps(ERR, ensure_ascii=False, indent=1))
run(t)
