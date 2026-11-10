"""시연 점검 6: 채팅 위젯 단계별 확인(열기→입력→응답 최대 3분), 네트워크 추적."""
import sys, re, json, time; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt
wt.OUT = "out/demo1109"
R = {}; net = []
def go(pg, path, wait=1500): pg.goto(BASE+path, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(wait)
def vshot(pg, name): pg.screenshot(path=f"{wt.OUT}/{name}.png")
def t(pg):
    pg.on("request", lambda r: net.append(("req", r.method, r.url[-70:], time.strftime("%H:%M:%S"))) if "/api/chat" in r.url else None)
    def on_res(r):
        if "/api/chat" in r.url:
            try: body = r.text()[:300]
            except Exception: body = "(stream)"
            net.append(("res", r.status, r.url[-70:], body if r.status >= 400 else body[:120], time.strftime("%H:%M:%S")))
    pg.on("response", on_res)
    for path in ("/dashboards", "/campaigns/32727667"):
        go(pg, path, 3000); tag = path.strip("/").replace("/", "_")
        fab = pg.locator("button:visible").evaluate_all("bs=>bs.map((b,i)=>({i,x:b.getBoundingClientRect().x,y:b.getBoundingClientRect().y,w:b.getBoundingClientRect().width,h:b.getBoundingClientRect().height,html:b.outerHTML.slice(0,120)}))")
        c = [b for b in fab if b["x"] > 1250 and b["y"] > 800 and b["w"] >= 40]; R[f"{tag} fab"] = c[:2]
        if not c: continue
        pg.locator("button:visible").nth(c[0]["i"]).click(); pg.wait_for_timeout(3000); vshot(pg, f"chat6-{tag}-open")
        R[f"{tag} panel"] = pg.evaluate("()=>{const d=[...document.querySelectorAll('div')].filter(e=>getComputedStyle(e).position==='fixed'&&e.getBoundingClientRect().width>300&&e.getBoundingClientRect().height>300);return d.map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,300))}")
        ta = pg.locator("textarea:visible"); R[f"{tag} textarea"] = ta.count()
        if not ta.count(): continue
        q = "지금 무엇을 도와줄 수 있는지 한 문장으로 알려줘." if "dash" in tag else "이 캠페인의 어제 노출 수를 알려줘."
        ta.last.fill(q); t0 = time.time(); ta.last.press("Enter"); last = ""; states = []
        for i in range(90):
            pg.wait_for_timeout(2000); txt = pg.evaluate("()=>document.body.innerText.replace(/\\s+/g,' ')")
            tail = txt[txt.rfind(q)+len(q):][:700] if q in txt else ""
            if tail != last: states.append((round(time.time()-t0), tail[:150])); last = tail
            if "전송하지 못했" in tail or (len(tail.strip()) > 60 and "준비하고" not in tail and i > 2 and tail == last): break
        R[f"{tag} chat s"] = round(time.time()-t0, 1); R[f"{tag} states"] = states[:8]; vshot(pg, f"chat6-{tag}-answer")
        try: pg.locator("button:visible").filter(has=pg.locator("svg")).evaluate_all("bs=>0"); pg.keyboard.press("Escape")
        except Exception: pass
    R["net"] = net[:30]
    # 정리
    go(pg, "/my-chats"); n = 0
    for _ in range(4):
        tr = pg.locator("tbody tr").filter(has_text=re.compile("무엇을 도와줄|어제 노출 수")).first
        if not tr.count(): break
        tr.locator("button").last.click(); pg.wait_for_timeout(500); m = pg.get_by_role("menuitem", name=re.compile("삭제"))
        if not m.count(): pg.keyboard.press("Escape"); break
        m.first.click(); pg.wait_for_timeout(800); confirm(pg); n += 1; pg.wait_for_timeout(1000)
    R["chats deleted"] = n; R["my-chats left"] = rows(pg)[:4]
    print(json.dumps(R, ensure_ascii=False, indent=1))
run(t)
