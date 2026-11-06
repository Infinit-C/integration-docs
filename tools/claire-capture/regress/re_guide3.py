"""가이드 조직 쓰기 플로우 재확인 (11/3 배포분): N2 그룹 마법사, G2/G8 KPI·수식 삭제 버튼, G3 수식 400, G4/G5 시각화 삭제, G6 알림 폼, G10 보고서, G14 대시보드."""
import sys, re, json, time; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt, os
from admin_shots import _api
wt.OUT = "out/regress-guide3"
R={}; bodies=[]
def go(pg, path, wait=1200): pg.goto(BASE+path, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(wait)
def leftovers(pg, path): go(pg, path, 900); return [r.split("\t")[0].strip() for r in rows(pg) if PREFIX in r]
def api_list(pg, path):
    st, body = _api(pg, "GET", f"{path}?page=0&size=100"); data = (body or {}).get("data"); return data if isinstance(data, list) else (data or {}).get("items", [])
def n2(pg):
    go(pg, "/campaign-groups/new"); field(pg, "이름").fill(PREFIX+" N2"); pg.get_by_role("button", name="계속").click(); pg.wait_for_timeout(1800)
    R["N2 after 계속: url"] = pg.url[len(BASE):]; R["N2 step2 head"] = main_text(pg, 400); R["N2 toasts"] = toast(pg)[:2]
    R["N2 created on step1?"] = leftovers(pg, "/campaign-groups")
    # Enter 키
    go(pg, "/campaign-groups/new"); f = field(pg, "이름"); f.fill(PREFIX+" N2E"); f.press("Enter"); pg.wait_for_timeout(1800); R["N2 enter: url"] = pg.url[len(BASE):]; R["N2 enter created?"] = leftovers(pg, "/campaign-groups")
    # 끝까지 만들어 중복 이름 메시지 확인
    go(pg, "/campaign-groups/new"); field(pg, "이름").fill(PREFIX+" N2"); pg.get_by_role("button", name="계속").click(); pg.wait_for_timeout(1500)
    R["N2 step2 buttons"] = [b for b in pg.locator("main button").all_inner_texts() if b.strip()][:8]; shot(pg, "n2-step2")
    for _ in range(4):
        b = pg.get_by_role("button", name=re.compile("^(계속|건너뛰기|완료|그룹 생성|생성)$")).last
        if not b.count() or not b.is_enabled(): break
        b.click(); pg.wait_for_timeout(1800)
        if "/campaign-groups/new" not in pg.url: break
    R["N2 final url"] = pg.url[len(BASE):]; R["N2 final toast"] = toast(pg)[:2]; R["N2 created list"] = leftovers(pg, "/campaign-groups")
    if R["N2 created list"]:
        go(pg, "/campaign-groups/new"); field(pg, "이름").fill(PREFIX+" N2"); pg.get_by_role("button", name="계속").click(); pg.wait_for_timeout(1500)
        for _ in range(4):
            b = pg.get_by_role("button", name=re.compile("^(계속|건너뛰기|완료|그룹 생성|생성)$")).last
            if not b.count() or not b.is_enabled(): break
            b.click(); pg.wait_for_timeout(1800)
            if "/campaign-groups/new" not in pg.url: break
        R["N2 dup toast"] = toast(pg)[:2]; R["N2 dup inline"] = [l for l in main_text(pg, 2000).split(" | ") if "이미" in l or "exists" in l][:2]; shot(pg, "n2-dup")
    # 정리 (API: disable → delete)
    for g in api_list(pg, "/campaign-groups"):
        if PREFIX in json.dumps(g, ensure_ascii=False):
            _api(pg, "PATCH", f"/campaign-groups/{g['code']}/disable"); R.setdefault("N2 cleanup", []).append(_api(pg, "DELETE", f"/campaign-groups/{g['code']}")[0])
    R["N2 leftover"] = leftovers(pg, "/campaign-groups")
def g2(pg):
    # KPI 규칙 생성 → 삭제 대화상자 버튼 문구
    go(pg, "/kpis/new", 1500); R["G2 kpi labels"] = [l.inner_text()[:16] for l in pg.locator("main label").all()][:10]
    field(pg, "이름").fill(PREFIX+" KPI")
    for cb in pg.locator("main [role=combobox]").all()[:3]:
        try: cb.click(timeout=1500); pg.wait_for_timeout(300); o = pg.get_by_role("option"); (o.first.click() if o.count() else pg.keyboard.press("Escape")); pg.wait_for_timeout(300)
        except Exception: pass
    for inp in pg.locator("main input[type=number]").all()[:2]: inp.fill("1000")
    R["G2 kpi create"] = save(pg, "생성|저장"); R["G2 kpi url"] = pg.url[len(BASE):]; shot(pg, "g2-kpi-after-create")
    r = row_action(pg, PREFIX, "비활성") if leftovers(pg, "/kpis") else None; R["G2 kpi disable"] = r and (r[0], r[1])
    r = row_action(pg, PREFIX, "삭제") if leftovers(pg, "/kpis") else None; R["G2 kpi delete dialog"] = r and (r[1], r[2]); R["G2 kpi leftover"] = leftovers(pg, "/kpis")
def g3(pg):
    go(pg, "/metric-formulas/new", 1500); R["G3 labels"] = [l.inner_text()[:16] for l in pg.locator("main label").all()][:10]
    field(pg, "이름").fill(PREFIX+" F");
    try: field(pg, "단위").fill("{VALUE} %")
    except Exception: pass
    ta = pg.locator("main textarea").last; ta.click(); ta.fill("${clicks} / ${impressions}")
    bodies.clear(); R["G3 create (no platform)"] = save(pg, "생성|저장"); R["G3 400 body"] = bodies[:2]; R["G3 url"] = pg.url[len(BASE):]; shot(pg, "g3-after-create")
    if "/new" in pg.url:  # 플랫폼 하나 선택 후 재시도
        cbs = pg.locator("main input[type=checkbox]"); R["G3 checkboxes"] = cbs.count()
        if cbs.count(): cbs.first.check(force=True); bodies.clear(); R["G3 create (1 platform)"] = save(pg, "생성|저장"); R["G3 400 body 2"] = bodies[:2]; R["G3 url 2"] = pg.url[len(BASE):]
    if leftovers(pg, "/metric-formulas"):
        row_action(pg, PREFIX, "비활성"); r = row_action(pg, PREFIX, "삭제") if leftovers(pg, "/metric-formulas") else None; R["G3 delete dialog"] = r and (r[1], r[2])
    R["G3 leftover"] = leftovers(pg, "/metric-formulas")
def g4(pg):
    go(pg, "/visualizations/new", 1500); field(pg, "이름").fill(PREFIX+" VIZ")
    R["G15 default period"] = [l for l in main_text(pg, 2000).split(" | ") if "최근" in l][:2]
    btn = pg.get_by_role("button", name=re.compile("생성|저장")).last; R["G15 create enabled w/o metric"] = btn.is_enabled()
    for cb in pg.locator("main [role=combobox]").all()[:4]:
        try: cb.click(timeout=1500); pg.wait_for_timeout(300); o = pg.get_by_role("option"); (o.first.click() if o.count() else pg.keyboard.press("Escape")); pg.wait_for_timeout(300)
        except Exception: pass
    btn = pg.get_by_role("button", name=re.compile("생성|저장")).last
    if btn.is_enabled(): R["G4 viz create"] = save(pg, "생성|저장"); R["G4 viz url"] = pg.url[len(BASE):]
    shot(pg, "g4-viz")
    if leftovers(pg, "/visualizations"): r = row_action(pg, PREFIX, "삭제"); R["G5 viz delete"] = r and (r[1], r[2])
    R["G4 viz leftover"] = leftovers(pg, "/visualizations")
    for v in api_list(pg, "/visualizations"):
        if PREFIX in json.dumps(v, ensure_ascii=False): R.setdefault("G4 api cleanup", []).append(_api(pg, "DELETE", f"/visualizations/{v['code']}")[0])
def g6(pg):
    go(pg, "/alerts/new", 1500); R["G6 labels"] = [l.inner_text()[:14] for l in pg.locator("main label").all()][:12]
    R["G6 initial errors"] = [l for l in main_text(pg, 2000).split(" | ") if re.search("필수|오류|입력하세요", l)][:3]; shot(pg, "g6-form")
    go(pg, "/alerts"); R["G7 alerts rows"] = len(rows(pg))
def g10(pg):
    go(pg, "/reports/new", 1500); R["G10 step1"] = main_text(pg, 300); R["G10 buttons"] = [b for b in pg.locator("main button").all_inner_texts() if b.strip()][:8]; shot(pg, "g10-step1")
    go(pg, "/reports"); R["G10 report rows"] = [r.replace("\t"," / ")[:90] for r in rows(pg)[:3]]
    if pg.locator("tbody tr").count(): r = row_action(pg, "", "zzz"); R["G10 row menu"] = r and r[0]
def g14(pg):
    go(pg, "/", 3000); mt = main_text(pg, 3000).split(" | "); R["G14 subtitle/period"] = [l for l in mt if "최근" in l][:4]; R["G14 compare"] = [l for l in mt if "비교" in l or re.search(r"[+-]\d+(\.\d+)?%", l)][:6]
    R["21 en-lower titles"] = [l for l in mt if re.fullmatch(r"[a-z][a-z ]+(chart|trends|trend)", l.strip())][:6]; shot(pg, "g14-dash")
def t(pg):
    pg.on("response", lambda r: bodies.append((r.status, r.url[-40:], r.text()[:160])) if r.status>=400 and "/api/" in r.url and "refresh" not in r.url else None)
    for f in (n2, g2, g3, g4, g6, g10, g14):
        try: f(pg)
        except Exception as e: R["!! "+f.__name__] = str(e)[:200]; shot(pg, f.__name__+"-fail")
    for k,v in R.items(): print(f"{k}: {v}")
run(t)
