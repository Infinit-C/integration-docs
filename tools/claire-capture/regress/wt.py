"""쓰기 흐름 테스트 공용 헬퍼: AUDIT-TEST 접두어 항목만 만들고 지운다. CLAIRE_PROFILE로 세션 선택."""
import re, sys, json, os
sys.path.insert(0, "/Users/yoonjaehyon/dev/integration-docs/tools/claire-capture")
from playwright.sync_api import sync_playwright
from capture import BASE, PROFILE
from deck_shots import _set_language
OUT = "out/audit-guide3/write"
PREFIX = "AUDIT-TEST"
log = []
def run(fn):
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(PROFILE, headless=True, viewport={"width":1440,"height":1000}, locale="ko-KR", timezone_id="Asia/Seoul")
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        pg.on("dialog", lambda d: (log.append(("confirm", d.message)), d.accept()))
        pg.on("console", lambda m: log.append(("console", m.type, m.text[:200])) if m.type in ("error",) else None)
        pg.on("response", lambda r: log.append(("http", r.status, r.request.method, r.url[-90:])) if r.status >= 400 and "refresh" not in r.url else None)
        try:
            pg.goto(BASE + "/", wait_until="networkidle"); pg.wait_for_timeout(800)
            _set_language(pg, "ko")
            fn(pg)
        finally:
            for l in log: print("  LOG", *l)
            ctx.close()
def toast(pg):
    t = pg.locator("[role=status], [role=alert], li[data-sonner-toast], .toast")
    return [x.strip().replace("\n", " | ") for x in t.all_inner_texts() if x.strip()]
def shot(pg, name): pg.screenshot(path=f"{OUT}/{name}.png", full_page=True)
def main_text(pg, n=1500): return pg.locator("main").inner_text()[:n].replace("\n", " | ")
def field(pg, label):
    l = pg.get_by_label(label, exact=False)
    if l.count(): return l.first
    return pg.locator(f"xpath=//label[contains(normalize-space(),'{label}')]/following::*[self::input or self::textarea][1]").first
def rows(pg): return [r.strip() for r in pg.locator("tbody tr").all_inner_texts()]
def dlg(pg):
    d = pg.locator("[role=dialog],[role=alertdialog]")
    return (d.inner_text()[:160].replace("\n", " | "), d.get_by_role("button").all_inner_texts()) if d.count() else None
def confirm(pg, pat="삭제|비활성|계속|확인|활성"):
    d = pg.locator("[role=dialog],[role=alertdialog]")
    if d.count():
        d.get_by_role("button").filter(has_text=re.compile(pat)).last.click(); pg.wait_for_timeout(2000); return True
    return False
def open_row(pg, text):
    tr = pg.locator("tbody tr", has_text=text).first
    a = tr.locator("a")
    (a.first if a.count() else tr).click(); pg.wait_for_timeout(1500)
def row_action(pg, text, action):
    """행 ⋮ 메뉴에서 action 클릭 → (메뉴항목, 대화상자, 토스트). 메뉴에 없으면 (항목, None, None)."""
    tr = pg.locator("tbody tr", has_text=text).first
    if not tr.count(): return None
    tr.locator("button").last.click(); pg.wait_for_timeout(500)
    items = pg.get_by_role("menuitem").all_inner_texts()
    m = pg.get_by_role("menuitem", name=re.compile(action))
    if not m.count(): pg.keyboard.press("Escape"); return (items, None, None)
    m.first.click(); pg.wait_for_timeout(800)
    d = dlg(pg); confirm(pg)
    return (items, d, toast(pg)[:2])
def click_action(pg, pattern):
    """상세 화면의 버튼 또는 ⋮ 메뉴 항목 클릭. 반환: 'button'/'menu'/None"""
    b = pg.locator("main button, main a").filter(has_text=re.compile(pattern))
    if b.count(): b.first.click(); pg.wait_for_timeout(800); return "button"
    for mb in pg.locator("main button[aria-haspopup], main button:has(svg)").all()[::-1]:
        try: mb.click(timeout=1500); pg.wait_for_timeout(400)
        except Exception: continue
        m = pg.get_by_role("menuitem", name=re.compile(pattern))
        if m.count(): m.first.click(); pg.wait_for_timeout(800); return "menu"
        pg.keyboard.press("Escape")
    return None
def save(pg, name="저장|생성|변경사항 저장"):
    pg.get_by_role("button", name=re.compile(name)).last.click(); pg.wait_for_timeout(2500); return toast(pg)[:2]
