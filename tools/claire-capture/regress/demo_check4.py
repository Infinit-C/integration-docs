"""시연 점검 4: 채팅 위젯 재시도(응답 본문 포함), 기간 프리셋 선택 구조 파악 후 지난주 화면."""
import sys, re, json, time; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt
wt.OUT = "out/demo1109"
R = {}; bodies = []
def go(pg, path, wait=1500): pg.goto(BASE+path, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(wait)
def vshot(pg, name): pg.screenshot(path=f"{wt.OUT}/{name}.png")
def open_widget(pg):
    if pg.locator("textarea:visible").count(): return True
    btn = pg.locator("button:visible").evaluate_all("bs=>bs.map((b,i)=>({i,x:b.getBoundingClientRect().x,y:b.getBoundingClientRect().y,w:b.getBoundingClientRect().width,h:b.getBoundingClientRect().height}))")
    c = [b for b in btn if b["x"] > 1250 and b["y"] > 800 and b["w"] >= 40 and b["h"] >= 40]
    if not c: return False
    pg.locator("button:visible").nth(c[0]["i"]).click(); 
    try: pg.locator("textarea:visible").first.wait_for(timeout=8000); return True
    except Exception: return False
def ask(pg, q, tag):
    if not open_widget(pg): R[tag] = "widget open fail"; vshot(pg, tag); return False
    ta = pg.locator("textarea:visible").last; ta.click(); ta.fill(q); t0 = time.time(); ta.press("Enter")
    last = ""; ok = None
    for _ in range(50):
        pg.wait_for_timeout(2000); txt = pg.evaluate("()=>document.body.innerText.replace(/\\s+/g,' ')")
        tail = txt[txt.rfind(q)+len(q):][:800] if q in txt else ""
        if "전송하지 못했" in tail or "unavailable" in tail.lower(): ok = False; break
        if tail == last and len(tail.strip()) > 60: ok = True; break
        last = tail
    R[tag] = {"ok": ok, "s": round(time.time()-t0, 1), "text": tail[:600]}; vshot(pg, tag); return ok
def chat(pg):
    pg.on("response", lambda r: bodies.append((r.status, r.url[-45:], r.text()[:300])) if "/api/chat" in r.url and r.status >= 400 else None)
    go(pg, "/campaigns/32727667", 2500)
    for i in range(3):
        if ask(pg, "이 캠페인의 어제 노출과 클릭 수를 알려줘.", f"chat-camp-try{i+1}"): break
        pg.wait_for_timeout(15000)
    go(pg, "/dashboards", 2500); ask(pg, "지금 무엇을 도와줄 수 있는지 한 문장으로 알려줘.", "chat-general")
    R["chat errors"] = bodies[:6]
def cleanup(pg):
    go(pg, "/my-chats"); n = 0
    for _ in range(6):
        tr = pg.locator("tbody tr").filter(has_text=re.compile("어제 노출과 클릭|무엇을 도와줄")).first
        if not tr.count(): break
        tr.locator("button").last.click(); pg.wait_for_timeout(500); m = pg.get_by_role("menuitem", name=re.compile("삭제"))
        if not m.count(): pg.keyboard.press("Escape"); break
        m.first.click(); pg.wait_for_timeout(800); confirm(pg); n += 1; pg.wait_for_timeout(1000)
    R["chats deleted"] = n; R["my-chats left"] = rows(pg)[:4]
def preset(pg):
    go(pg, "/campaigns/32727667", 2500)
    b = pg.locator("main button").filter(has_text="최근 24시간").first
    R["preset btn html"] = b.evaluate("e=>e.outerHTML.slice(0,300)")
    b.click(); pg.wait_for_timeout(1200); vshot(pg, "preset-popup2")
    R["preset popup2"] = pg.evaluate("()=>[...document.querySelectorAll('body > *:not(#root):not(#__next), [role=listbox], [role=menu], [data-radix-popper-content-wrapper], [data-state=open]')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,200)).filter(Boolean).slice(0,6)")
    R["preset options2"] = pg.locator("[role=option], [role=menuitem], [role=menuitemradio]").all_inner_texts()[:12]
    t = pg.locator("[role=option], [role=menuitem], [role=menuitemradio]").filter(has_text=re.compile("지난주|최근 7일|7일")).first
    if t.count():
        t.click(); pg.wait_for_timeout(4000); R["preset after"] = main_text(pg, 300); vshot(pg, "camp-week"); pg.mouse.wheel(0, 500); pg.wait_for_timeout(1500); vshot(pg, "camp-week-2")
        R["preset ls"] = pg.evaluate("()=>Object.entries(localStorage).filter(([k])=>/date-time-range/.test(k)).map(([k,v])=>k.slice(-45)+' = '+v.slice(0,120))")
        pg.locator("main button").filter(has_text=re.compile("지난주|7일")).first.click(); pg.wait_for_timeout(700); pg.locator("[role=option], [role=menuitem], [role=menuitemradio]").filter(has_text="최근 24시간").first.click(); pg.wait_for_timeout(1500)
        R["preset restored"] = "최근 24시간" in main_text(pg, 400)
    else: pg.keyboard.press("Escape")
def t(pg):
    for fn in (chat, cleanup, preset):
        try: fn(pg)
        except Exception as e: R[f"ERR {fn.__name__}"] = str(e).split("\n")[0][:200]
    print(json.dumps(R, ensure_ascii=False, indent=1))
run(t)
