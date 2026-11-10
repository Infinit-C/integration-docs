"""시연 점검 7: 캠페인 채팅 전송 후 4분 대기, 요청 본문·응답 기록, 서버에 답변이 저장됐는지 API로 확인. 일반 위젯 열기 재확인."""
import sys, re, json, time; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt
from admin_shots import _api
wt.OUT = "out/demo1109"
R = {}; net = []
def go(pg, path, wait=1500): pg.goto(BASE+path, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(wait)
def vshot(pg, name): pg.screenshot(path=f"{wt.OUT}/{name}.png")
def fab(pg):
    b = pg.locator("button:visible").evaluate_all("bs=>bs.map((b,i)=>({i,x:b.getBoundingClientRect().x,y:b.getBoundingClientRect().y,w:b.getBoundingClientRect().width}))")
    c = [x for x in b if x["x"] > 1250 and x["y"] > 800 and x["w"] >= 40]
    return pg.locator("button:visible").nth(c[0]["i"]) if c else None
def t(pg):
    pg.on("request", lambda r: net.append(("req", r.method, r.url[-50:], (r.post_data or "")[:200], time.strftime("%H:%M:%S"))) if "/api/chat" in r.url else None)
    def on_res(r):
        if "/api/chat" in r.url:
            try: body = r.text()[:200]
            except Exception: body = "(stream)"
            net.append(("res", r.status, r.url[-50:], body, time.strftime("%H:%M:%S")))
    pg.on("response", on_res)
    # 일반 위젯
    go(pg, "/dashboards", 3000); f = fab(pg); f.click(); pg.wait_for_timeout(3000); vshot(pg, "chat7-general-open")
    R["general after click"] = pg.evaluate("()=>document.body.innerText.replace(/\\s+/g,' ').slice(-400)"); R["general textarea"] = pg.locator("textarea:visible").count()
    pg.keyboard.press("Escape")
    # 캠페인 채팅
    go(pg, "/campaigns/32727667", 3000); f = fab(pg); f.click(); pg.locator("textarea:visible").first.wait_for(timeout=8000)
    q = "이 캠페인의 어제 노출 수를 알려줘."
    ta = pg.locator("textarea:visible").last; ta.fill(q); t0 = time.time(); ta.press("Enter")
    last = ""; states = []
    for i in range(120):
        pg.wait_for_timeout(2000); txt = pg.evaluate("()=>document.body.innerText.replace(/\\s+/g,' ')")
        tail = txt[txt.rfind(q)+len(q):][:600] if q in txt else ""
        if tail != last: states.append((round(time.time()-t0), tail[:200])); last = tail
        if "전송하지 못했" in tail or (len(tail.strip()) > 60 and "준비하고" not in tail and i > 2 and tail == last): break
    R["camp chat s"] = round(time.time()-t0, 1); R["camp states"] = states[:8]; vshot(pg, "chat7-camp-answer")
    st, body = _api(pg, "GET", "/chat/messages?resourceCode=32727667&resourceType=campaign")
    msgs = ((body or {}).get("data") or {}).get("messages") or []
    R["server msgs"] = [(m.get("role") or m.get("sender") or m.get("type"), (m.get("message") or m.get("content") or "")[:120]) for m in msgs][-4:]
    R["net"] = net[:30]
    go(pg, "/my-chats"); n = 0
    for _ in range(4):
        tr = pg.locator("tbody tr").filter(has_text=re.compile("어제 노출 수|무엇을 도와줄")).first
        if not tr.count(): break
        tr.locator("button").last.click(); pg.wait_for_timeout(500); m = pg.get_by_role("menuitem", name=re.compile("삭제"))
        if not m.count(): pg.keyboard.press("Escape"); break
        m.first.click(); pg.wait_for_timeout(800); confirm(pg); n += 1; pg.wait_for_timeout(1000)
    R["chats deleted"] = n; R["my-chats left"] = rows(pg)[:4]
    print(json.dumps(R, ensure_ascii=False, indent=1))
run(t)
