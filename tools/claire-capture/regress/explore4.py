"""탐색 4: 사이드바 겹침 상태 원인(localStorage) 확인·초기화·재현(390→1440), 캠페인 상세 ⋮ 메뉴."""
import sys, re, json, time; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt
wt.OUT = "out/explore"
R = {}
DANGER = re.compile("삭제|비활성|활성화|발송|보내기|연결 끊기|연결 해제|재수집|수집|초대|재발급|폐기|실행|로그아웃")
def go(pg, path, wait=1500): pg.goto(BASE+path, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(wait)
def vshot(pg, name): pg.screenshot(path=f"{wt.OUT}/{name}.png")
def geom(pg): return pg.evaluate("()=>{const m=document.querySelector('main');const a=document.querySelector('aside');const r=e=>e&&{l:Math.round(e.getBoundingClientRect().left),w:Math.round(e.getBoundingClientRect().width)};return {main:r(m),aside:r(a),ariaExp:[...document.querySelectorAll('header button')].map(b=>b.getAttribute('aria-label')+'='+b.getAttribute('aria-expanded')).filter(x=>/내비/.test(x))}}")
def t(pg):
    go(pg, "/campaigns", 2000); R["start"] = geom(pg)
    R["ls keys"] = pg.evaluate("()=>Object.entries(localStorage).filter(([k,v])=>/side|nav|collap|layout|menu|open/i.test(k)).map(([k,v])=>k+' = '+String(v).slice(0,80))")
    R["cookies"] = [c["name"] + "=" + c["value"][:30] for c in pg.context.cookies() if re.search("side|nav|collap|layout", c["name"], re.I)]
    # 헤더의 내비게이션 버튼으로 토글해 보기
    for lab in ("내비게이션 펼치기", "내비게이션 열기"):
        b = pg.get_by_role("button", name=lab)
        if b.count(): b.first.click(); pg.wait_for_timeout(800); R[f"after {lab}"] = geom(pg); vshot(pg, "sidebar-" + lab)
    R["ls keys after"] = pg.evaluate("()=>Object.entries(localStorage).filter(([k,v])=>/side|nav|collap|layout|menu|open/i.test(k)).map(([k,v])=>k+' = '+String(v).slice(0,80))")
    # 초기화: 관련 키 삭제 후 리로드
    pg.evaluate("()=>{for(const k of Object.keys(localStorage)){if(/side|nav|collap|layout/i.test(k))localStorage.removeItem(k)}}"); pg.reload(wait_until="networkidle"); pg.wait_for_timeout(2000); R["after reset"] = geom(pg); vshot(pg, "sidebar-reset")
    # 재현: 390 → 1440
    pg.set_viewport_size({"width": 390, "height": 900}); go(pg, "/campaigns", 1500); R["at 390"] = geom(pg)
    pg.set_viewport_size({"width": 1440, "height": 1000}); pg.wait_for_timeout(1500); R["back 1440 no reload"] = geom(pg); vshot(pg, "sidebar-back1440")
    pg.reload(wait_until="networkidle"); pg.wait_for_timeout(2000); R["back 1440 reload"] = geom(pg); vshot(pg, "sidebar-back1440-reload")
    R["ls keys repro"] = pg.evaluate("()=>Object.entries(localStorage).filter(([k,v])=>/side|nav|collap|layout|menu|open/i.test(k)).map(([k,v])=>k+' = '+String(v).slice(0,80))")
    # 복구
    pg.evaluate("()=>{for(const k of Object.keys(localStorage)){if(/side|nav|collap|layout/i.test(k))localStorage.removeItem(k)}}"); pg.reload(wait_until="networkidle"); pg.wait_for_timeout(2000); R["final"] = geom(pg)
    # 캠페인 상세 ⋮
    go(pg, "/campaigns/83901859", 2500)
    icons = [b for b in pg.locator("main button").all() if not b.inner_text().strip() and b.locator("svg").count() and b.is_visible()]
    R["icon btns"] = [(b.get_attribute("aria-label") or b.get_attribute("aria-haspopup") or "?") for b in icons]
    mb = next((b for b in icons if b.get_attribute("aria-haspopup")), icons[0] if icons else None)
    if mb:
        mb.click(); pg.wait_for_timeout(500); items = pg.get_by_role("menuitem").all_inner_texts(); R["camp menu"] = items; vshot(pg, "camp-menu"); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        for it in items:
            if DANGER.search(it): continue
            mb.click(); pg.wait_for_timeout(400); pg.get_by_role("menuitem", name=it, exact=True).click(); pg.wait_for_timeout(2000)
            R[f"camp menu:{it}"] = {"url": pg.url[len(BASE):][:80], "head": main_text(pg, 160), "dialog": (dlg(pg) or [None])[0]}; vshot(pg, "camp-" + re.sub(r"\W+", "_", it)[:20])
            c = pg.locator("[role=dialog] button").filter(has_text=re.compile("^(취소|닫기|Close)$"))
            if c.count(): c.first.click(); pg.wait_for_timeout(500)
            go(pg, "/campaigns/83901859", 1500); d = dlg(pg)
            if d: R[f"camp menu:{it} leave"] = d[0][:100]; confirm(pg, "나가기|확인|계속|취소")
            icons = [b for b in pg.locator("main button").all() if not b.inner_text().strip() and b.locator("svg").count() and b.is_visible()]; mb = next((b for b in icons if b.get_attribute("aria-haspopup")), icons[0])
    print(json.dumps(R, ensure_ascii=False, indent=1))
run(t)
