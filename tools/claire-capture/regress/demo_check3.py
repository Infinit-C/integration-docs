"""시연 점검 3: 채팅 503 재시도(위젯·일반), 테스트 채팅 삭제, 기간 프리셋 UI 구조, 데이터 업로드 화면."""
import sys, re, json, time; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt
from admin_shots import _api
wt.OUT = "out/demo1109"
R = {}; bodies = []
def go(pg, path, wait=1500): pg.goto(BASE+path, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(wait)
def vshot(pg, name): pg.screenshot(path=f"{wt.OUT}/{name}.png")
def send(pg, q, tag, wait_rounds=45):
    fab = pg.locator("button").filter(has=pg.locator("svg")).evaluate_all("bs=>bs.map((b,i)=>({i,x:b.getBoundingClientRect().x,y:b.getBoundingClientRect().y,w:b.getBoundingClientRect().width}))")
    c = [f for f in fab if f["x"] > 1200 and f["y"] > 700 and f["w"] > 30]
    if not pg.locator("textarea:visible").count():
        if not c: R[tag] = "no fab"; return
        pg.locator("button").filter(has=pg.locator("svg")).nth(c[0]["i"]).click(); pg.wait_for_timeout(1200)
    ta = pg.locator("textarea:visible").last; ta.fill(q); t0 = time.time(); ta.press("Enter")
    last = ""
    for _ in range(wait_rounds):
        pg.wait_for_timeout(2000); txt = pg.evaluate("()=>document.body.innerText.replace(/\\s+/g,' ')")
        tail = txt[txt.rfind(q)+len(q):] if q in txt else txt[-800:]
        if "전송하지 못했습니다" in tail or "unavailable" in tail: break
        if tail == last and len(tail.strip()) > 60: break
        last = tail
    R[tag] = {"s": round(time.time()-t0, 1), "text": tail[:700]}
    vshot(pg, tag)
def chat_retry(pg):
    pg.on("response", lambda r: bodies.append((r.status, r.url[-40:], r.text()[:300])) if "/api/chat" in r.url and r.status >= 400 else None)
    go(pg, "/campaigns/32727667", 2500)
    for i in range(3):
        send(pg, "이 캠페인의 어제 노출과 클릭 수를 알려줘.", f"chat-camp-try{i+1}")
        if "전송하지 못했" not in json.dumps(R.get(f"chat-camp-try{i+1}", ""), ensure_ascii=False): break
        pg.wait_for_timeout(20000)
    go(pg, "/dashboards", 2500)
    send(pg, "안녕하세요. 지금 무엇을 도와줄 수 있나요? 한 문장으로.", "chat-general")
    R["chat errors"] = bodies[:6]
def cleanup_chats(pg):
    go(pg, "/my-chats"); n = 0
    for _ in range(6):
        tr = pg.locator("tbody tr").filter(has_text=re.compile("노출과 클릭|무엇을 도와줄")).first
        if not tr.count(): break
        tr.locator("button").last.click(); pg.wait_for_timeout(500); R.setdefault("chat row menu", pg.get_by_role("menuitem").all_inner_texts())
        m = pg.get_by_role("menuitem", name=re.compile("삭제"))
        if not m.count(): pg.keyboard.press("Escape"); break
        m.first.click(); pg.wait_for_timeout(800); confirm(pg); n += 1; pg.wait_for_timeout(1000)
    R["chats deleted"] = n; R["my-chats left"] = rows(pg)[:4]
def preset_ui(pg):
    go(pg, "/campaigns/32727667", 2500)
    b = pg.locator("main button").filter(has_text="최근 24시간").first; b.click(); pg.wait_for_timeout(700)
    R["preset popup"] = pg.evaluate("()=>[...document.querySelectorAll('[data-radix-popper-content-wrapper],[role=listbox],[role=menu],[role=dialog],[data-state=open]')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,300)).filter(Boolean).slice(0,4)")
    vshot(pg, "preset-popup")
    t = pg.get_by_text(re.compile("^(지난주|최근 7일|지난 7일)$")).first
    if t.count():
        t.click(); pg.wait_for_timeout(4000); R["preset after"] = main_text(pg, 400); vshot(pg, "camp-week"); pg.mouse.wheel(0, 500); pg.wait_for_timeout(1500); vshot(pg, "camp-week-2")
        R["preset ls"] = pg.evaluate("()=>Object.entries(localStorage).filter(([k])=>/date-time-range/.test(k)).map(([k,v])=>k.slice(-40)+' = '+v.slice(0,120))")
        # 되돌리기
        pg.locator("main button").filter(has_text=re.compile("지난주|최근 7일|지난 7일")).first.click(); pg.wait_for_timeout(500); pg.get_by_text(re.compile("^최근 24시간$")).first.click(); pg.wait_for_timeout(1500)
    else: pg.keyboard.press("Escape")
def upload(pg):
    go(pg, "/campaigns"); e = pg.get_by_text("데이터 업로드").first
    R["upload el"] = e.evaluate("e=>e.closest('a,button')?.outerHTML.slice(0,200)") if e.count() else None
    if e.count(): e.click(); pg.wait_for_timeout(1500); R["upload url"] = pg.url[len(BASE):]; R["upload text"] = (dlg(pg) or main_text(pg, 600)); vshot(pg, "upload")
def t(pg):
    for fn in (chat_retry, cleanup_chats, preset_ui, upload):
        try: fn(pg)
        except Exception as e: R[f"ERR {fn.__name__}"] = str(e).split("\n")[0][:200]
    print(json.dumps(R, ensure_ascii=False, indent=1))
run(t)
