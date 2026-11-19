"""탐색 6c: 보고서 링크 공개 페이지 — 새 링크(AI 채팅 on) 생성 후 /share/{token} 열람·뷰어 질문·모바일·소유자 '받은 질문'·링크 끊기·끊긴 뒤 접근. 기존 AUDIT-TEST 링크는 먼저 끊는다."""
import sys, re, json, time; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt
wt.OUT = "out/explore6"
R = {}; API = []
def go(pg, path, wait=1800): pg.goto(path if path.startswith("http") else BASE+path, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(wait)
def vshot(pg, name, full=False): pg.screenshot(path=f"{wt.OUT}/{name}.png", full_page=full)
def step(name, fn):
    n = len(wt.log)
    try: R[name] = fn()
    except Exception as e: R[name] = f"ERR {type(e).__name__}: {str(e)[:200]}"
    if len(wt.log) > n: R[name+" :log"] = wt.log[n:]
def D(pg): return pg.locator("[role=dialog]").first
def open_dialog(pg):
    pg.get_by_role("button", name=re.compile("보고서 링크")).first.click(); pg.wait_for_timeout(2000); return D(pg)
def revoke_all(pg):
    n = 0
    while D(pg).get_by_role("button", name="링크 끊기").count() and n < 5:
        D(pg).get_by_role("button", name="링크 끊기").first.click(); pg.wait_for_timeout(800)
        a = pg.locator("[role=alertdialog], [role=dialog]").last
        a.get_by_role("button").filter(has_text=re.compile("끊기")).last.click(); pg.wait_for_timeout(2000); n += 1
    return n
def t(pg):
    pg.on("response", lambda r: API.append((r.request.method, r.status, r.url, r.text())) if "report-shares" in r.url and r.request.method == "POST" else None)
    go(pg, "/campaigns/83901859", 2500)
    open_dialog(pg); R["0 revoked"] = revoke_all(pg)
    def create():
        d = D(pg)
        d.get_by_placeholder("예: 월간 성과 보고서").fill("AUDIT-TEST 주간 보고서")
        d.get_by_placeholder("리포트를 받는 분께 전할 내용을 입력하세요").fill("AUDIT-TEST 메모: 지난주 대비 클릭 증가")
        d.get_by_label("리포트 관련 AI 채팅 활성화").first.click(); pg.wait_for_timeout(300)
        for m in ("CTR", "클릭"): d.locator("label", has_text=re.compile(f"^{m}$")).last.click(); pg.wait_for_timeout(150)
        d.get_by_role("combobox").nth(0).click(); pg.wait_for_timeout(300); pg.get_by_role("option", name="최근 30일").click(); pg.wait_for_timeout(300)
        d.get_by_role("button", name="링크 만들기").click(); pg.wait_for_timeout(3500)
        for m, s, u, b in API:
            mt = re.search(r'"token"\s*:\s*"([^"]+)"', b)
            if s == 201 and mt: return BASE + "/share/" + mt.group(1)
        return "no token: " + (API[-1][3][:300] if API else "no api")
    step("1 create", create)
    url = R["1 create"] if str(R["1 create"]).startswith("http") else None
    R["share url"] = url
    vshot(pg, "33-created", True); pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    if url:
        p2 = pg.context.new_page(); errs = []
        p2.on("console", lambda m: errs.append(m.text[:200]) if m.type == "error" else None)
        p2.on("response", lambda r: errs.append((r.status, r.url[-80:])) if r.status >= 400 else None)
        p2.goto(url, wait_until="networkidle"); p2.wait_for_timeout(3500)
        def pub():
            vshot(p2, "34-public-report", True)
            return {"url": p2.url, "title": p2.title(), "text": p2.locator("body").inner_text()[:3500].replace("\n"," | "), "canvas": p2.locator("canvas").count(), "svg": p2.locator("svg").count(), "tables": p2.locator("table").count(),
                    "buttons": [b for b in p2.locator("button").all_inner_texts() if b.strip()][:20], "inputs": [(i.get_attribute("placeholder")) for i in p2.locator("textarea,input").all()], "links": [(a.inner_text()[:30], a.get_attribute("href")) for a in p2.locator("a").all()][:10]}
        step("2 public page", pub)
        def chat():
            box = p2.locator("textarea").last if p2.locator("textarea").count() else p2.locator("input").last
            if not box.count(): return "no box"
            box.fill("이 보고서에서 CTR이 가장 높은 날은 언제야?"); p2.wait_for_timeout(300)
            sb = p2.get_by_role("button", name=re.compile("질문|보내기|전송|Send|Ask"))
            if sb.count(): sb.last.click()
            else: p2.keyboard.press("Enter")
            t0 = time.time(); body = ""
            while time.time() - t0 < 150:
                p2.wait_for_timeout(3000); body = p2.locator("body").inner_text()
                if re.search(r"9개|오늘 9|9 questions|오류|실패|잠시 후", body): break
            vshot(p2, "35-public-report-chat", True)
            return {"elapsed": round(time.time()-t0), "tail": body[-1800:].replace("\n"," | ")}
        step("2 viewer chat", chat)
        def mobile():
            p2.set_viewport_size({"width":390,"height":844}); p2.wait_for_timeout(1500); vshot(p2, "36-public-390", True)
            w = p2.evaluate("document.documentElement.scrollWidth"); p2.set_viewport_size({"width":1440,"height":1000}); return {"scrollWidth@390": w}
        step("2 mobile", mobile)
        R["2 public errors"] = errs[:20]
        go(pg, "/campaigns/83901859", 2500)
        def owner():
            d = open_dialog(pg); vshot(pg, "37-owner-list", True)
            out = {"tail": d.inner_text()[-500:].replace("\n"," | ")}
            b = d.get_by_role("button", name="받은 질문")
            if b.count():
                b.first.click(); pg.wait_for_timeout(2500); vshot(pg, "38-owner-log", True)
                a = pg.locator("[role=dialog]").last; out["log"] = a.inner_text()[-1500:].replace("\n"," | "); out["log buttons"] = a.get_by_role("button").all_inner_texts()
                cl = a.get_by_role("button", name=re.compile("닫기|뒤로|Close")); 
                if cl.count(): cl.last.click(); pg.wait_for_timeout(500)
            return out
        step("3 owner log", owner)
        def revoke():
            if not D(pg).count(): open_dialog(pg)
            n = revoke_all(pg); vshot(pg, "39-after-revoke", True)
            return {"revoked": n, "toast": toast(pg)[:2], "tail": D(pg).inner_text()[-400:].replace("\n"," | ")}
        step("3 revoke", revoke)
        pg.keyboard.press("Escape")
        def after():
            p2.goto(url, wait_until="networkidle"); p2.wait_for_timeout(2500); vshot(p2, "40-public-after-revoke"); return p2.locator("body").inner_text()[:400].replace("\n"," | ")
        step("3 revoked page", after)
        p2.close()
    print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
run(t)
