"""클릭 탐색 3차: 다크모드 레이아웃 치수, 캠페인 목록 일괄 작업/행 메뉴(role=checkbox 대응), 캠페인 상세 ⋮ 메뉴, 내 채팅 행 메뉴, 검색·알림 팝업 캡처."""
import sys, re, json, time; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt
wt.OUT = "out/explore"
R = {}; ERR = []
DANGER = re.compile("삭제|비활성|활성화|발송|보내기|연결 끊기|연결 해제|재수집|수집|초대|재발급|폐기|실행|로그아웃")
def go(pg, path, wait=1500): pg.goto(BASE+path, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(wait)
def vshot(pg, name): pg.screenshot(path=f"{wt.OUT}/{name}.png")
def step(pg, name, fn):
    n = len(wt.log)
    try: r = fn(); R[name] = r if r is not None else "ok"
    except Exception as e: R[name] = "ERR " + str(e).split("\n")[0][:160]; vshot(pg, "err3-" + re.sub(r"[^\w]+", "_", name)[:60])
    new = [l for l in wt.log[n:] if l[0] in ("console", "http")]
    if new: ERR.append((name, new[:4]))
def geom(pg): return pg.evaluate("()=>{const m=document.querySelector('main');const a=document.querySelector('aside');const n=document.querySelector('nav');const r=e=>e&&{l:Math.round(e.getBoundingClientRect().left),w:Math.round(e.getBoundingClientRect().width)};return {html:document.documentElement.className,main:r(m),aside:r(a),nav:r(n),mainPad:m&&getComputedStyle(m).paddingLeft,mainML:m&&getComputedStyle(m).marginLeft}}")
def theme(pg): pg.get_by_role("button", name="색상 모드 변경").click(); pg.wait_for_timeout(1200)
def dark(pg):
    go(pg, "/campaigns/83901859", 2500); out = {"light": geom(pg)}; vshot(pg, "theme-light")
    theme(pg); out["dark"] = geom(pg); vshot(pg, "theme-dark")
    go(pg, "/campaigns", 2000); out["dark campaigns"] = geom(pg); vshot(pg, "theme-dark-campaigns")
    theme(pg); out["light again"] = geom(pg); vshot(pg, "theme-light-again")
    return out
def checkbox(pg, scope):
    cb = scope.locator("input[type=checkbox], [role=checkbox], button[role=checkbox]").first
    cb.click(force=True); pg.wait_for_timeout(500); return cb.count()
def campaigns(pg):
    go(pg, "/campaigns"); out = {}
    out["cb kinds"] = pg.locator("tbody tr").first.evaluate("tr=>[...tr.querySelectorAll('input,button,[role=checkbox]')].map(e=>e.tagName+':'+(e.getAttribute('role')||e.type||'')+':'+(e.getAttribute('aria-label')||''))")
    checkbox(pg, pg.locator("tbody tr").first); out["actions btn"] = pg.get_by_role("button", name=re.compile("작업")).first.inner_text()
    pg.get_by_role("button", name=re.compile("작업")).first.click(); pg.wait_for_timeout(500); out["actions menu"] = pg.get_by_role("menuitem").all_inner_texts(); vshot(pg, "campaign-actions"); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    tr = pg.locator("tbody tr").first; tr.locator("button").last.click(); pg.wait_for_timeout(500); out["rowmenu"] = pg.get_by_role("menuitem").all_inner_texts(); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    pg.get_by_role("button", name="열 선택").click(); pg.wait_for_timeout(600); vshot(pg, "campaign-columns"); out["columns popup"] = pg.evaluate("()=>[...document.querySelectorAll('[role=menu],[role=dialog],[role=listbox],[data-state=open]')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,300)).filter(t=>t.length>5).slice(-2)"); pg.keyboard.press("Escape")
    return out
def camp_detail(pg):
    go(pg, "/campaigns/83901859", 2500); out = {"tabs": pg.get_by_role("tab").all_inner_texts()}
    for tab in out["tabs"][1:]:
        pg.get_by_role("tab", name=tab, exact=True).click(); pg.wait_for_timeout(1200); out[f"tab {tab} url"] = pg.url[len(BASE):][:70]
    go(pg, "/campaigns/83901859", 2000)
    hb = pg.locator("main button[aria-haspopup]"); out["haspopup btns"] = [(b.get_attribute("aria-label") or b.inner_text().strip()[:12]) for b in hb.all()]
    mb = hb.last; mb.click(); pg.wait_for_timeout(500); items = pg.get_by_role("menuitem").all_inner_texts(); out["menu"] = items; vshot(pg, "camp-menu"); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    for it in items:
        if DANGER.search(it): continue
        hb.last.click(); pg.wait_for_timeout(400); pg.get_by_role("menuitem", name=it, exact=True).click(); pg.wait_for_timeout(2000)
        out[f"menu:{it}"] = {"url": pg.url[len(BASE):][:80], "head": main_text(pg, 160), "dialog": (dlg(pg) or [None])[0]}; vshot(pg, "camp-" + re.sub(r"\W+", "_", it)[:20])
        c = pg.locator("[role=dialog] button").filter(has_text=re.compile("^(취소|닫기|Close)$"))
        if c.count(): c.first.click(); pg.wait_for_timeout(500)
        go(pg, "/campaigns/83901859", 1500)
        d = dlg(pg)
        if d: out[f"menu:{it} leave"] = d[0][:100]; confirm(pg, "나가기|확인|계속|취소")
    pg.get_by_role("button", name="대시보드 사용자 지정").click(); pg.wait_for_timeout(2000); out["customize btns"] = [x for x in pg.locator("main button").all_inner_texts() if x.strip()][:12]; vshot(pg, "camp-customize")
    pg.get_by_role("button", name="시각화 추가").click(); pg.wait_for_timeout(700); vshot(pg, "camp-add-viz"); out["add viz"] = pg.get_by_role("menuitem").all_inner_texts() or (dlg(pg) or [None])[0]; pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    pg.get_by_role("button", name="취소").click(); pg.wait_for_timeout(800); out["after cancel"] = (dlg(pg) or [None])[0] or main_text(pg, 100); confirm(pg, "확인|계속|나가기|취소")
    go(pg, "/campaigns/83901859", 1500); pg.get_by_role("button", name="보고서 링크").click(); pg.wait_for_timeout(800); vshot(pg, "camp-report-link"); out["보고서 링크"] = (dlg(pg) or [None])[0] or toast(pg)[:1]; pg.keyboard.press("Escape")
    return out
def chats(pg):
    go(pg, "/my-chats"); out = {}
    tr = pg.locator("tbody tr").first; tr.locator("button").last.click(); pg.wait_for_timeout(500); out["rowmenu"] = pg.get_by_role("menuitem").all_inner_texts(); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    checkbox(pg, pg.locator("tbody tr").first); b = pg.get_by_role("button", name=re.compile("작업")).first; b.click(); pg.wait_for_timeout(500); out["actions"] = pg.get_by_role("menuitem").all_inner_texts(); pg.keyboard.press("Escape")
    tr.locator("td").nth(1).click(); pg.wait_for_timeout(1500); out["detail"] = {"url": pg.url[len(BASE):][:40], "btns": [x for x in pg.locator("main button").all_inner_texts() if x.strip()][:6]}
    return out
def header(pg):
    go(pg, "/dashboards"); out = {}
    pg.get_by_role("button", name="검색").click(); pg.wait_for_timeout(800); vshot(pg, "search-open"); pg.keyboard.type("브랜드"); pg.wait_for_timeout(1500); vshot(pg, "search-result"); out["search text"] = pg.evaluate("()=>document.body.innerText.replace(/\\s+/g,' ').slice(-500)"); pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    pg.get_by_role("button", name="알림").click(); pg.wait_for_timeout(800); vshot(pg, "bell-open"); out["bell text"] = pg.evaluate("()=>document.body.innerText.replace(/\\s+/g,' ').slice(-400)"); pg.keyboard.press("Escape")
    pg.get_by_role("button", name="사용자 메뉴 열기").click(); pg.wait_for_timeout(400); pg.get_by_role("menuitem", name="회사 설정").click(); pg.wait_for_timeout(2000); out["회사 설정"] = {"url": pg.url[len(BASE):][:60], "head": main_text(pg, 300), "tabs": pg.get_by_role("tab").all_inner_texts()}; vshot(pg, "company-settings")
    return out
def t(pg):
    for fn in (dark, campaigns, camp_detail, chats, header):
        step(pg, fn.__name__, lambda fn=fn: fn(pg))
    print(json.dumps(R, ensure_ascii=False, indent=1)); print("ERRORS", json.dumps(ERR, ensure_ascii=False, indent=1))
run(t)
