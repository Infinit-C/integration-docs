"""시연 점검 2: 채팅 위젯 응답, 기간 프리셋 변경 후 캠페인/그룹 대시보드, 데이터 업로드·조직 전환·채널 추가 화면."""
import sys, re, json, time; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt
wt.OUT = "out/demo1109"
R = {}
def go(pg, path, wait=1500): pg.goto(BASE+path, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(wait)
def vshot(pg, name): pg.screenshot(path=f"{wt.OUT}/{name}.png")
def canvases(pg):
    return pg.locator("main").evaluate("""m=>[...m.querySelectorAll('canvas,svg')].filter(c=>c.getBoundingClientRect().width>200).map(c=>{let p=c;for(let k=0;k<8&&p;k++){if(p.offsetHeight>150)break;p=p.parentElement}
      let painted=null;if(c.tagName==='CANVAS'){try{const x=c.getContext('2d');const d=x.getImageData(0,0,c.width,c.height).data;let n=0;for(let i=3;i<d.length;i+=4*97){if(d[i]>0)n++}painted=n}catch(e){painted='err'}}
      return {tag:c.tagName,w:Math.round(c.getBoundingClientRect().width),painted,title:(p?p.innerText:'').replace(/\\s+/g,' ').slice(0,30)}})""")
def preset(pg, name):
    b = pg.locator("main button").filter(has_text=re.compile("최근 24시간|지난주|지난달|최근 3개월|최근 7일|최근 30일")).first
    b.click(); pg.wait_for_timeout(500)
    opts = pg.get_by_role("option"); items = pg.get_by_role("menuitem")
    src = opts if opts.count() else items
    names = src.all_inner_texts(); R.setdefault("preset options", names)
    t = src.filter(has_text=name)
    if t.count(): t.first.click(); pg.wait_for_timeout(3500); return True
    pg.keyboard.press("Escape"); return False
def dash_ranges(pg):
    go(pg, "/campaigns/32727667", 3000); R["camp 24h canvases"] = canvases(pg)
    ok = preset(pg, re.compile("지난주|최근 7일")); R["camp preset switched"] = ok
    R["camp week head"] = main_text(pg, 500); R["camp week canvases"] = canvases(pg); vshot(pg, "camp-32727667-week")
    pg.mouse.wheel(0, 700); pg.wait_for_timeout(1500); vshot(pg, "camp-32727667-week-2")
    go(pg, "/campaign-groups/50164236", 3000); R["group tabs"] = pg.get_by_role("tab").all_inner_texts(); R["group 24h canvases"] = canvases(pg)
    preset(pg, re.compile("지난주|최근 7일")); R["group week head"] = main_text(pg, 600); vshot(pg, "group-week")
    pg.mouse.wheel(0, 600); pg.wait_for_timeout(2000); R["group week canvases"] = canvases(pg); vshot(pg, "group-week-2")
    for tab in pg.get_by_role("tab").all_inner_texts()[1:]:
        pg.get_by_role("tab", name=tab, exact=True).click(); pg.wait_for_timeout(2000); R[f"group tab {tab}"] = main_text(pg, 300); vshot(pg, f"group-{tab}")
    # 24시간으로 되돌림 (사용자 환경 그대로 두기 위해)
    go(pg, "/campaigns/32727667", 2000); preset(pg, re.compile("최근 24시간"))
    go(pg, "/campaign-groups/50164236", 2000); preset(pg, re.compile("최근 24시간"))
def chat(pg):
    go(pg, "/campaigns/32727667", 2500)
    fab = pg.locator("button").filter(has=pg.locator("svg")).evaluate_all("bs=>bs.map((b,i)=>({i,fixed:getComputedStyle(b).position==='fixed'||getComputedStyle(b.parentElement).position==='fixed',x:b.getBoundingClientRect().x,y:b.getBoundingClientRect().y,w:b.getBoundingClientRect().width}))")
    cand = [f for f in fab if f["x"] > 1200 and f["y"] > 700 and f["w"] > 30]; R["fab"] = cand[:3]
    if not cand: R["chat"] = "위젯 버튼 못 찾음"; return
    pg.locator("button").filter(has=pg.locator("svg")).nth(cand[0]["i"]).click(); pg.wait_for_timeout(1500); vshot(pg, "chat-open")
    R["chat panel text"] = pg.evaluate("()=>document.body.innerText.replace(/\\s+/g,' ').slice(-600)")
    ta = pg.locator("textarea:visible, input[type=text]:visible").last
    R["chat input count"] = ta.count()
    if not ta.count(): return
    q = "이 캠페인의 최근 7일 노출과 클릭, ROAS를 한 문장으로 요약해줘."
    ta.fill(q); t0 = time.time(); ta.press("Enter"); pg.wait_for_timeout(1500)
    first = None; last = ""
    for _ in range(60):
        pg.wait_for_timeout(2000); txt = pg.evaluate("()=>document.body.innerText.replace(/\\s+/g,' ')")
        tail = txt[txt.find(q)+len(q):] if q in txt else txt[-1500:]
        if first is None and len(tail.strip()) > 40: first = round(time.time()-t0, 1)
        if tail == last and len(tail.strip()) > 40 and not re.search("생각 중|분석 중|입력 중|답변 생성|loading", tail, re.I): break
        last = tail
    R["chat first token s"] = first; R["chat total s"] = round(time.time()-t0, 1); R["chat answer"] = last[:1200]; vshot(pg, "chat-answer")
    go(pg, "/my-chats", 1500); R["my-chats after"] = rows(pg)[:3]
def misc(pg):
    go(pg, "/campaigns"); b = pg.get_by_role("button", name=re.compile("데이터 업로드"))
    if b.count(): b.first.click(); pg.wait_for_timeout(1500); R["upload url"] = pg.url[len(BASE):]; R["upload text"] = main_text(pg, 500) if "/campaigns" != pg.url[len(BASE):] else (dlg(pg) or main_text(pg, 300)); vshot(pg, "upload")
    # 조직 전환 메뉴
    go(pg, "/campaigns"); o = pg.locator("header button, header [role=button]").filter(has_text="데모")
    if o.count():
        o.first.click(); pg.wait_for_timeout(700); R["org menu"] = pg.evaluate("()=>[...document.querySelectorAll('[role=menu],[role=listbox],[role=dialog],[data-radix-popper-content-wrapper]')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,300))"); vshot(pg, "org-menu"); pg.keyboard.press("Escape")
    # 채널 추가 대화상자
    go(pg, "/communication-groups/T06TF0J0PDG"); a = pg.get_by_role("button", name=re.compile("채널 추가"))
    if a.count(): a.first.click(); pg.wait_for_timeout(1500); R["add channel dlg"] = dlg(pg); vshot(pg, "add-channel"); pg.keyboard.press("Escape")
    # 다크 모드 한 장
    go(pg, "/alerts"); 
    try: pg.locator("header button").nth(2).click(); pg.wait_for_timeout(1000); vshot(pg, "dark-alerts"); pg.locator("header button").nth(2).click(); pg.wait_for_timeout(500)
    except Exception as e: R["dark"] = str(e)[:80]
def t(pg):
    for fn in (dash_ranges, chat, misc):
        try: fn(pg)
        except Exception as e: R[f"ERR {fn.__name__}"] = str(e).split("\n")[0][:200]
    print(json.dumps(R, ensure_ascii=False, indent=1))
run(t)
