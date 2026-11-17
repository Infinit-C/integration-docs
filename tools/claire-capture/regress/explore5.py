"""탐색 5: 사이드바 겹침 재현(1024→1440, 헤더 내비게이션 버튼), 검색·알림 팝업 캡처, 시각화 편집기 폭 좁힘."""
import sys, re, json, time; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt
wt.OUT = "out/explore"
R = {}
def go(pg, path, wait=1500): pg.goto(BASE+path, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(wait)
def vshot(pg, name): pg.screenshot(path=f"{wt.OUT}/{name}.png")
def geom(pg): return pg.evaluate("()=>{const m=document.querySelector('main');const a=document.querySelector('aside');const r=e=>e&&{l:Math.round(e.getBoundingClientRect().left),w:Math.round(e.getBoundingClientRect().width)};return {main:r(m),aside:r(a),ls:Object.entries(localStorage).filter(([k])=>/sidebarType|isCollapse/.test(k)).map(([k,v])=>k+'='+v)}}")
def t(pg):
    go(pg, "/campaigns", 2000); R["1440 start"] = geom(pg)
    for w in (1280, 1100, 1024, 900):
        pg.set_viewport_size({"width": w, "height": 900}); pg.wait_for_timeout(1200); R[f"at {w}"] = geom(pg)
        pg.set_viewport_size({"width": 1440, "height": 1000}); pg.wait_for_timeout(1200); R[f"back from {w}"] = geom(pg)
        if R[f"back from {w}"]["main"]["l"] != 260: vshot(pg, f"sidebar-back-from-{w}"); break
    pg.reload(wait_until="networkidle"); pg.wait_for_timeout(1500); R["after reload"] = geom(pg); vshot(pg, "sidebar-after-reload")
    # 헤더 버튼 조합
    for lab in ("내비게이션 접기", "내비게이션 펼치기", "내비게이션 열기"):
        b = pg.get_by_role("button", name=lab)
        if b.count(): b.first.click(); pg.wait_for_timeout(800); R[f"click {lab}"] = geom(pg); vshot(pg, f"sidebar-{lab}")
    pg.evaluate("()=>{localStorage.removeItem('sidebarType');localStorage.setItem('isCollapse','\"full-sidebar\"')}"); pg.reload(wait_until="networkidle"); pg.wait_for_timeout(1500); R["restored"] = geom(pg)
    # 검색/알림
    go(pg, "/dashboards", 1500)
    pg.get_by_role("button", name="검색").click(); pg.wait_for_timeout(1000); vshot(pg, "search-open2"); R["search dom"] = pg.evaluate("()=>[...document.querySelectorAll('[role=dialog],[cmdk-root],input[type=search],input[placeholder]')].map(e=>(e.tagName+' '+(e.getAttribute('placeholder')||e.innerText.replace(/\\s+/g,' ').slice(0,100))))")
    pg.keyboard.type("브랜드"); pg.wait_for_timeout(1500); vshot(pg, "search-typed2"); R["search after"] = pg.evaluate("()=>[...document.querySelectorAll('[role=dialog],[cmdk-root],[role=listbox]')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,300))"); pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    pg.get_by_role("button", name="알림").click(); pg.wait_for_timeout(1000); vshot(pg, "bell-open2"); R["bell dom"] = pg.evaluate("()=>[...document.querySelectorAll('[role=dialog],[role=menu],[data-radix-popper-content-wrapper],[data-state=open]')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,200)).filter(t=>t)")
    print(json.dumps(R, ensure_ascii=False, indent=1))
run(t)
