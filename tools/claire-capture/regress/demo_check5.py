"""시연 점검 5: 채팅 응답 대기(최대 4분, 네트워크 추적), 기간 프리셋 '최근 1주' 적용 화면."""
import sys, re, json, time; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt
wt.OUT = "out/demo1109"
R = {}; net = []
def go(pg, path, wait=1500): pg.goto(BASE+path, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(wait)
def vshot(pg, name): pg.screenshot(path=f"{wt.OUT}/{name}.png")
def chat(pg):
    pg.on("request", lambda r: net.append(("req", r.method, r.url[-60:], time.strftime("%H:%M:%S"))) if "/api/chat" in r.url else None)
    pg.on("response", lambda r: net.append(("res", r.status, r.url[-60:], (r.text()[:200] if r.status >= 400 else ""), time.strftime("%H:%M:%S"))) if "/api/chat" in r.url else None)
    pg.on("websocket", lambda ws: net.append(("ws", ws.url[-60:])))
    go(pg, "/dashboards", 2500)
    btn = pg.locator("button:visible").evaluate_all("bs=>bs.map((b,i)=>({i,x:b.getBoundingClientRect().x,y:b.getBoundingClientRect().y,w:b.getBoundingClientRect().width}))")
    c = [b for b in btn if b["x"] > 1250 and b["y"] > 800 and b["w"] >= 40]
    pg.locator("button:visible").nth(c[0]["i"]).click(); pg.locator("textarea:visible").first.wait_for(timeout=8000)
    q = "지금 무엇을 도와줄 수 있는지 한 문장으로 알려줘."
    ta = pg.locator("textarea:visible").last; ta.fill(q); t0 = time.time(); ta.press("Enter")
    last = ""; states = []
    for i in range(120):
        pg.wait_for_timeout(2000); txt = pg.evaluate("()=>document.body.innerText.replace(/\\s+/g,' ')")
        tail = txt[txt.rfind(q)+len(q):][:700] if q in txt else ""
        if tail != last: states.append((round(time.time()-t0), tail[:120])); last = tail
        if "전송하지 못했" in tail: break
        if len(tail.strip()) > 60 and "준비하고" not in tail and tail == last and i > 2: break
    R["chat s"] = round(time.time()-t0, 1); R["chat states"] = states[:8]; R["chat final"] = last[:700]; vshot(pg, "chat-general2")
    R["net"] = net[:20]
def cleanup(pg):
    go(pg, "/my-chats"); n = 0
    for _ in range(4):
        tr = pg.locator("tbody tr").filter(has_text=re.compile("무엇을 도와줄|어제 노출과 클릭")).first
        if not tr.count(): break
        tr.locator("button").last.click(); pg.wait_for_timeout(500); m = pg.get_by_role("menuitem", name=re.compile("삭제"))
        if not m.count(): pg.keyboard.press("Escape"); break
        m.first.click(); pg.wait_for_timeout(800); confirm(pg); n += 1; pg.wait_for_timeout(1000)
    R["chats deleted"] = n; R["my-chats left"] = rows(pg)[:4]
def preset(pg):
    go(pg, "/campaigns/32727667", 2500)
    pg.locator("main button").filter(has_text="최근 24시간").first.click(); pg.wait_for_timeout(1000)
    pop = pg.get_by_text("최근 1주", exact=True).first
    R["popup box"] = pop.evaluate("e=>{let p=e;for(let k=0;k<10&&p;k++){const s=getComputedStyle(p);if(s.position==='fixed'||s.position==='absolute')break;p=p.parentElement}const r=p.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,pos:getComputedStyle(p).position}}")
    pop.click(); pg.wait_for_timeout(300); pg.get_by_role("button", name="적용").click(); pg.wait_for_timeout(4000)
    R["preset after"] = main_text(pg, 300); vshot(pg, "camp-week"); pg.mouse.wheel(0, 450); pg.wait_for_timeout(1500); vshot(pg, "camp-week-2")
    go(pg, "/campaign-groups/50164236", 3000); R["group range btn"] = pg.locator("main button").filter(has_text=re.compile("최근")).first.inner_text(); vshot(pg, "group-after-preset")
    # 되돌리기
    go(pg, "/campaigns/32727667", 2000); pg.locator("main button").filter(has_text=re.compile("최근")).first.click(); pg.wait_for_timeout(800); pg.get_by_text("최근 24시간", exact=True).first.click(); pg.wait_for_timeout(300); pg.get_by_role("button", name="적용").click(); pg.wait_for_timeout(2000)
    R["restored"] = pg.locator("main button").filter(has_text=re.compile("최근")).first.inner_text()
def t(pg):
    for fn in (chat, cleanup, preset):
        try: fn(pg)
        except Exception as e: R[f"ERR {fn.__name__}"] = str(e).split("\n")[0][:200]
    print(json.dumps(R, ensure_ascii=False, indent=1))
run(t)
