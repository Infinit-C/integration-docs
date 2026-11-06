"""후속: N2 그룹 생성 완료+중복 메시지, 시각화 폼 구조, G7 알림 행 클릭, 1차-21 차트 제목 위치."""
import sys, re, json; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt
from admin_shots import _api
wt.OUT = "out/regress-guide3"
R={}; bodies=[]
def go(pg, path, wait=1200): pg.goto(BASE+path, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(wait)
def leftovers(pg, path): go(pg, path, 900); return [r.split("\t")[0].strip() for r in rows(pg) if PREFIX in r]
def api_list(pg, path):
    st, body = _api(pg, "GET", f"{path}?page=0&size=100"); data = (body or {}).get("data"); return data if isinstance(data, list) else (data or {}).get("items", [])
def create_group(pg, name):
    go(pg, "/campaign-groups/new"); field(pg, "이름").fill(name); pg.get_by_role("button", name="계속").click(); pg.wait_for_timeout(1500)
    bodies.clear(); pg.get_by_role("button", name="캠페인 그룹 생성").click(); pg.wait_for_timeout(2500)
    return (pg.url[len(BASE):], toast(pg)[:2], [l for l in main_text(pg, 2500).split(" | ") if "이미" in l or "exists" in l or "오류" in l][:2], bodies[:2])
def n2(pg):
    R["N2 create #1"] = create_group(pg, PREFIX+" N2"); R["N2 list after #1"] = leftovers(pg, "/campaign-groups")
    R["N2 create #2 (dup)"] = create_group(pg, PREFIX+" N2"); shot(pg, "n2-dup"); R["N2 list after #2"] = leftovers(pg, "/campaign-groups")
    for g in api_list(pg, "/campaign-groups"):
        if PREFIX in json.dumps(g, ensure_ascii=False):
            _api(pg, "PATCH", f"/campaign-groups/{g['code']}/disable"); R.setdefault("N2 cleanup", []).append(_api(pg, "DELETE", f"/campaign-groups/{g['code']}")[0])
    R["N2 leftover"] = leftovers(pg, "/campaign-groups")
def viz(pg):
    go(pg, "/visualizations/new", 1500); R["viz labels"] = [l.inner_text()[:20] for l in pg.locator("main label").all()][:15]
    R["viz inputs"] = [(i.get_attribute("name") or i.get_attribute("id") or i.get_attribute("placeholder") or "")[:30] for i in pg.locator("main input, main textarea").all()][:12]
    R["viz tabs"] = pg.locator("main [role=tab]").all_inner_texts(); R["viz buttons"] = [b for b in pg.locator("main button").all_inner_texts() if b.strip()][:12]
    R["viz period"] = [l for l in main_text(pg, 2500).split(" | ") if "최근" in l][:2]; shot(pg, "viz-new")
def g7(pg):
    go(pg, "/alerts"); R["G7 rows"] = [r.replace("\t"," / ")[:140] for r in rows(pg)[:2]]
    R["G7 raw codes"] = sorted(set(re.findall(r"\b(spend|cpm_max|media_cost|impressions|clicks|ctr)\b", main_text(pg, 3000))))
    tr = pg.locator("tbody tr").first; R["G7 links"] = [a.get_attribute("href") for a in tr.locator("a").all()][:3]
    tr.locator("td").nth(1).click(); pg.wait_for_timeout(1500); R["G7 url after cell click"] = pg.url[len(BASE):]
    if pg.url.rstrip("/").endswith("/alerts"):
        r = row_action(pg, "", "zzz"); R["G7 row menu"] = r and r[0]; pg.keyboard.press("Escape")
    go(pg, "/alert-events"); R["6 events"] = [r.replace("\t"," / ")[:140] for r in rows(pg)[:2]]
def c21(pg):
    go(pg, "/", 4000)
    R["21 where"] = pg.locator("main").evaluate("""m=>[...m.querySelectorAll('*')].filter(e=>e.children.length==0&&/^(line|bar|area) chart$/.test((e.textContent||'').trim())).map(e=>({tag:e.tagName,cls:(e.className||'').toString().slice(0,60),vis:e.offsetHeight>0,parent:(e.parentElement.className||'').toString().slice(0,60)})).slice(0,4)""")
    R["21 subtitle els"] = pg.locator("main").evaluate("""m=>[...m.querySelectorAll('*')].filter(e=>e.children.length==0&&/핵심 캠페인|비교 데이터 없음/.test(e.textContent||'')).map(e=>({t:e.textContent.trim().slice(0,40),cls:(e.className||'').toString().slice(0,50),sib:(e.parentElement.innerText||'').replace(/\\s+/g,' ').slice(0,100)})).slice(0,4)""")
def t(pg):
    pg.on("response", lambda r: bodies.append((r.status, r.url[-40:], r.text()[:200])) if r.status>=400 and "/api/" in r.url and "refresh" not in r.url else None)
    for f in (n2, viz, g7, c21):
        try: f(pg)
        except Exception as e: R["!! "+f.__name__] = str(e).split("\n")[0][:160]; shot(pg, f.__name__+"-fail")
    for k,v in R.items(): print(f"{k}: {v}")
run(t)
