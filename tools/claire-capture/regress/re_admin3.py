"""관리자 조직 재확인 (11/3 배포분): 1차-5/7/11/12/13/15/21, N2 중복 이름 메시지, 4 시각화 404, 20 그룹 대시보드."""
import sys, re, json, time; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt, os
wt.OUT = "out/regress-admin3"
R={}; reqs=[]
CAMP="85837881"
def go(pg, path, wait=1500, until="networkidle"):
    t0=time.time(); pg.goto(BASE+path, wait_until=until, timeout=60000); pg.wait_for_timeout(wait); return round(time.time()-t0,1)
def s5(pg):
    go(pg, "/alerts"); R["5 alerts rows"] = [r.replace("\t"," / ")[:110] for r in rows(pg)[:4]]; shot(pg, "alerts")
    R["5 raw codes in list"] = sorted(set(re.findall(r"\b(spend|cpm_max|media_cost|impressions_min|ctr_min)\b", main_text(pg, 4000))))
    tr = pg.locator("tbody tr").first; R["G7 row cells"] = tr.locator("td").count(); R["G7 row links"] = tr.locator("a").count()
    tr.click(timeout=5000); pg.wait_for_timeout(1500); R["G7 row click url"] = pg.url[len(BASE):]
def s6(pg):
    go(pg, "/alert-events"); R["6 events rows"] = [r.replace("\t"," / ")[:110] for r in rows(pg)[:3]]
    R["6 raw codes"] = sorted(set(re.findall(r"\b(spend|cpm_max|media_cost|sent)\b", main_text(pg, 4000))))
def s7(pg):
    go(pg, f"/campaigns/{CAMP}?tab=alerts", 2500); R["7 campaign alerts"] = [l for l in main_text(pg, 3000).split(" | ") if re.search(r"A:|조건|cpm|CPM|Spend|지출", l)][:5]; shot(pg, "campaign-alerts")
def s21(pg):
    go(pg, f"/campaigns/{CAMP}", 3000); R["21 campaign dash en-lower titles"] = [l for l in main_text(pg, 4000).split(" | ") if re.fullmatch(r"[a-z][a-z ]+(chart|trends|trend)", l.strip())][:6]
    R["1 refresh calls"] = sum(1 for r in reqs if r[0]=="POST" and "auth/refresh" in r[1]); R["1 429s"] = [r for r in reqs if r[0]=="RES" and r[1]==429][:2]
def s20(pg):
    go(pg, "/campaign-groups"); pg.locator("tbody tr a").first.click(); pg.wait_for_timeout(3500); shot(pg, "group-dash")
    mt = main_text(pg, 3000).split(" | "); R["20 upper cards"] = [l for l in mt if l.isupper()][:8]; R["G14 subtitle"] = [l for l in mt if "최근" in l][:4]
    R["21 group dash en-lower titles"] = [l for l in mt if re.fullmatch(r"[a-z][a-z ]+(chart|trends|trend)", l.strip())][:6]
    R["G14 compare"] = [l for l in mt if "비교" in l or "%" in l][:6]
def s4(pg):
    reqs.clear(); go(pg, "/visualizations/32753865", 3000); R["4 toasts"] = toast(pg)[:2]; R["4 404s"] = [r for r in reqs if r[0]=="RES" and r[1]==404][:3]; R["4 note"] = [l for l in main_text(pg, 800).split(" | ") if "제외" in l or "연결" in l][:2]
def s11(pg):
    go(pg, "/org/policies"); R["11 policies"] = [r.replace("\t"," / ")[:100] for r in rows(pg)[:6]]
def s12(pg):
    links = pg.locator("a[href*='status']"); R["12 status links"] = [a.get_attribute("href") for a in links.all()][:3]
    for path in (R["12 status links"] or []) + ["/status", "/system-status", "/admin/status", "/system/status"]:
        try:
            go(pg, path, 2500)
            if pg.url.endswith(path) and "로그인" not in main_text(pg, 200):
                mt = main_text(pg, 4000); R["12 status url"] = path; R["12 raw names"] = sorted(set(re.findall(r"\b(database|storage|memory_heap|memory_rss|event_handler|microservice|scheduler|version)\b", mt))); R["12 head"] = mt[:300]; shot(pg, "status"); return
        except Exception as e: R["12 err "+path] = str(e)[:60]
def s13(pg):
    reqs.clear(); R["13 audit-events load(s)"] = go(pg, "/audit-events", 2000, until="load")
    pg.get_by_role("tab", name="파이프라인", exact=True).click(); t0=time.time()
    pg.locator("tbody tr").first.wait_for(timeout=15000); R["13 pipeline first-row(s)"] = round(time.time()-t0,1); R["13 pipeline rows"] = [r[:90] for r in rows(pg)[:2]]; shot(pg, "pipeline")
def s15(pg):
    go(pg, "/custom-summaries/new"); pg.locator("button[name=customSummaryCampaignGroup], #customSummaryCampaignGroup").first.click(); pg.wait_for_timeout(400); opts = pg.get_by_role("option").all_inner_texts()
    g = next((o for o in opts if "GUGUS" in o), None); R["15 group"] = g
    if g:
        pg.get_by_role("option", name=g).click(); pg.wait_for_timeout(1000)
        try: pg.get_by_role("button", name="마크다운").click(); pg.wait_for_timeout(800)
        except Exception: pass
        pv = pg.get_by_role("tab", name=re.compile("미리보기"))
        if pv.count(): pv.first.click(); pg.wait_for_timeout(3500); R["15 preview labels"] = [l for l in main_text(pg, 2000).split(" | ") if re.search(r"media_cost|Media cost|미디어 비용|spend|최근 7일|last_7", l)][:4]; shot(pg, "summary-preview")
def sN2(pg):
    go(pg, "/org/user-groups"); names = [r.split("\t")[0].strip() for r in rows(pg)]; R["N2 existing group"] = names[:1]
    if names:
        go(pg, "/org/user-groups/new"); field(pg, "이름").fill(names[0]); pg.get_by_role("button", name=re.compile("생성|저장")).last.click(); pg.wait_for_timeout(2500)
        R["N2 dup toast"] = toast(pg)[:2]; R["N2 dup inline"] = [l for l in main_text(pg, 1500).split(" | ") if "이미" in l or "exists" in l][:2]; R["N2 url"] = pg.url[len(BASE):]; shot(pg, "n2-dup")
        go(pg, "/org/user-groups"); R["N2 dup created?"] = sum(1 for r in rows(pg) if r.split("\t")[0].strip()==names[0])
def t(pg):
    pg.on("request", lambda r: reqs.append((r.method, r.url[len(BASE):][:110])) if "/api/" in r.url else None)
    pg.on("response", lambda r: reqs.append(("RES", r.status, r.url[len(BASE):][:80])) if r.status>=400 and "/api/" in r.url else None)
    for f in (s5, s6, s7, s21, s20, s4, s11, s12, s13, s15, sN2):
        try: f(pg)
        except Exception as e: R["!! "+f.__name__] = str(e).split("\n")[0][:160]; shot(pg, f.__name__+"-fail")
    for k,v in R.items(): print(f"{k}: {v}")
run(t)
