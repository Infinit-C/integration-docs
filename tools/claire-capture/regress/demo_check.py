"""시연 전 데모 조직 점검: 대시보드·시각화·캠페인 상세 차트 렌더, 알림, 채팅 응답, 최소 쓰기 플로우(그룹·KPI 생성/삭제)."""
import sys, re, json, time; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt
from admin_shots import _api
wt.OUT = "out/demo1109"
R = {}
def go(pg, path, wait=1500): pg.goto(BASE+path, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(wait)
def vshot(pg, name): pg.screenshot(path=f"{wt.OUT}/{name}.png")
def cards(pg, name):
    """main 안의 차트 카드(svg path 포함 영역)를 하나씩 뷰포트에 넣어 렌더 확인."""
    out = []
    els = pg.locator("main svg").all()
    seen = set()
    for i, svg in enumerate(els[:30]):
        try:
            info = svg.evaluate("""s=>{let c=s;for(let k=0;k<8&&c;k++){if(c.offsetHeight>150)break;c=c.parentElement}if(!c)return null;const t=c.innerText.replace(/\\s+/g,' ').slice(0,50);return {t,h:c.offsetHeight,w:s.getBoundingClientRect().width}}""")
        except Exception: continue
        if not info or info["w"] < 150 or info["t"] in seen: continue
        seen.add(info["t"])
        svg.scroll_into_view_if_needed(); pg.wait_for_timeout(1500)
        n = svg.evaluate("s=>{let c=s;for(let k=0;k<8&&c;k++){if(c.offsetHeight>150)break;c=c.parentElement}return {paths:c.querySelectorAll('svg path').length,rects:c.querySelectorAll('svg rect').length,empty:/데이터 없음|No data|데이터가 없/.test(c.innerText)}}")
        out.append((info["t"][:40], n["paths"], n["rects"], n["empty"]))
        vshot(pg, f"{name}-card{len(out)}")
    R[f"{name} cards"] = out
def dashboards(pg):
    go(pg, "/", 3000); vshot(pg, "home-top"); R["home head"] = main_text(pg, 300); cards(pg, "home")
    go(pg, "/dashboards"); R["dashboards rows"] = rows(pg)[:6]; R["dashboards text"] = main_text(pg, 300)
    for a in pg.locator("main a[href^='/dashboards/']").all()[:3]:
        href = a.get_attribute("href"); go(pg, href, 3000); R[f"dash {href} head"] = main_text(pg, 200); cards(pg, "dash-"+href.split("/")[-1])
def visualizations(pg):
    go(pg, "/visualizations"); R["viz rows"] = rows(pg)[:5]
    for code in ("81109134", "48019753", "53382199"):
        go(pg, f"/visualizations/{code}", 3000); R[f"viz {code}"] = main_text(pg, 200); cards(pg, f"viz-{code}")
def campaigns(pg):
    go(pg, "/campaigns"); R["campaign rows"] = rows(pg)[:5]; vshot(pg, "campaigns")
    for code in ("32727667", "41512968"):
        go(pg, f"/campaigns/{code}", 3000); R[f"camp {code} head"] = main_text(pg, 300); R[f"camp {code} tabs"] = pg.get_by_role("tab").all_inner_texts()
        cards(pg, f"camp-{code}")
        for tab in pg.get_by_role("tab").all_inner_texts()[1:]:
            try: pg.get_by_role("tab", name=tab, exact=True).click(); pg.wait_for_timeout(2500); R[f"camp {code} tab {tab}"] = main_text(pg, 400); vshot(pg, f"camp-{code}-{tab}")
            except Exception as e: R[f"camp {code} tab {tab}"] = str(e)[:80]
    go(pg, "/campaign-groups"); R["group rows"] = rows(pg)[:3]
    a = pg.locator("main a[href^='/campaign-groups/']").first
    if a.count():
        href = a.get_attribute("href"); go(pg, href, 3000); R["group head"] = main_text(pg, 300); R["group tabs"] = pg.get_by_role("tab").all_inner_texts(); cards(pg, "group")
        for tab in pg.get_by_role("tab").all_inner_texts()[1:]:
            try: pg.get_by_role("tab", name=tab, exact=True).click(); pg.wait_for_timeout(2500); R[f"group tab {tab}"] = main_text(pg, 300); vshot(pg, f"group-{tab}")
            except Exception as e: R[f"group tab {tab}"] = str(e)[:80]
def alerts(pg):
    go(pg, "/alerts"); R["alerts rows"] = rows(pg)[:8]; vshot(pg, "alerts")
    open_row(pg, "게재 이상"); R["alert detail"] = main_text(pg, 500); vshot(pg, "alert-detail")
    go(pg, "/alert-events"); R["alert events"] = rows(pg)[:6]; R["alert events text"] = main_text(pg, 300); vshot(pg, "alert-events")
def chat(pg):
    go(pg, "/my-chats", 2000); R["my-chats"] = main_text(pg, 300); vshot(pg, "my-chats")
    go(pg, "/chats", 2000); R["chats head"] = main_text(pg, 300); R["chats buttons"] = [b for b in pg.locator("main button").all_inner_texts() if b.strip()][:10]
    ta = pg.locator("main textarea, main input[type=text]").last
    if ta.count():
        ta.fill("최근 7일 기준으로 노출이 가장 많은 캠페인은 무엇인가요? 한 문장으로 답해주세요."); t0 = time.time(); ta.press("Enter")
        last = ""; 
        for _ in range(45):
            pg.wait_for_timeout(2000); txt = main_text(pg, 3000)
            if txt == last and len(txt) > 300: break
            last = txt
        R["chat elapsed s"] = round(time.time()-t0, 1); R["chat text"] = last[-900:]; vshot(pg, "chat-answer")
    else: R["chat input"] = "없음"
def writes(pg):
    # 캠페인 그룹 생성→삭제
    go(pg, "/campaign-groups/new"); field(pg, "이름").fill(PREFIX+" 그룹"); pg.get_by_role("button", name="계속").click(); pg.wait_for_timeout(1500)
    R["grp step2 btns"] = [b for b in pg.locator("main button").all_inner_texts() if b.strip()][:8]
    b = pg.get_by_role("button", name=re.compile("캠페인 그룹 생성|생성"))
    if b.count(): b.last.click(); pg.wait_for_timeout(2000)
    R["grp create url"] = pg.url[len(BASE):]; R["grp create toast"] = toast(pg)[:2]
    st, body = _api(pg, "GET", "/campaign-groups?page=0&size=100"); data = body.get("data"); items = data if isinstance(data, list) else (data or {}).get("items", (data or {}).get("content", []))
    for g in items:
        if PREFIX in (g.get("name") or ""):
            _api(pg, "PATCH", f"/campaign-groups/{g['code']}/disable"); R.setdefault("grp cleanup", []).append(_api(pg, "DELETE", f"/campaign-groups/{g['code']}")[0])
    go(pg, "/campaign-groups"); R["grp leftover"] = [r for r in rows(pg) if PREFIX in r]
    # KPI 생성→비활성→삭제 (UI)
    go(pg, "/kpis/new"); field(pg, "이름").fill(PREFIX+" KPI")
    for cb in pg.locator("main [role=combobox]").all()[:3]:
        try: cb.click(timeout=1500); pg.wait_for_timeout(300); o = pg.get_by_role("option"); (o.first.click() if o.count() else pg.keyboard.press("Escape")); pg.wait_for_timeout(300)
        except Exception: pass
    for inp in pg.locator("main input[type=number]").all()[:2]: inp.fill("1000")
    R["kpi create"] = save(pg, "생성|저장"); R["kpi url"] = pg.url[len(BASE):]
    go(pg, "/kpis"); 
    if [r for r in rows(pg) if PREFIX in r]:
        r = row_action(pg, PREFIX, "비활성"); R["kpi disable"] = r and r[0]
        go(pg, "/kpis"); r = row_action(pg, PREFIX, "삭제"); R["kpi delete"] = r and (r[1], r[2])
    go(pg, "/kpis"); R["kpi leftover"] = [r for r in rows(pg) if PREFIX in r]
    # 폼 열기만 (저장 안 함)
    for p in ("/alerts/new", "/reports/new", "/custom-summaries/new", "/visualizations/new"):
        go(pg, p); R[f"form {p}"] = (main_text(pg, 250), [l.inner_text()[:14] for l in pg.locator("main label").all()][:8])
def t(pg):
    for fn in (dashboards, visualizations, campaigns, alerts, chat, writes):
        try: fn(pg)
        except Exception as e: R[f"ERR {fn.__name__}"] = str(e).split("\n")[0][:200]
    print(json.dumps(R, ensure_ascii=False, indent=1))
run(t)
