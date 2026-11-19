"""탐색 6b: 보고서 링크 2차 — 남은 AUDIT-TEST 링크 끊기, AI 채팅 켜서 새 링크 생성(URL은 API 응답에서), 공개 페이지·뷰어 질문·소유자 로그·링크 끊기·끊긴 뒤 접근. 소재 탭 기간, 일괄 편집."""
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
    n = 0; c = None
    while pg.locator("[role=dialog]").first.get_by_role("button", name="링크 끊기").count() and n < 5:
        pg.locator("[role=dialog]").first.get_by_role("button", name="링크 끊기").first.click(); pg.wait_for_timeout(800)
        a = pg.locator("[role=alertdialog], [role=dialog]").last
        c = (a.inner_text()[:200].replace("\n"," | "), a.get_by_role("button").all_inner_texts())
        a.get_by_role("button").filter(has_text=re.compile("끊기|해지|확인|삭제")).last.click(); pg.wait_for_timeout(2000); n += 1
    return n, c
def t(pg):
    pg.on("response", lambda r: API.append((r.request.method, r.status, r.url, (r.text()[:600] if "json" in (r.headers.get("content-type") or "") else ""))) if re.search(r"share", r.url) and r.request.method in ("POST","PATCH","PUT","DELETE") else None)
    go(pg, "/campaigns/83901859", 2500)
    step("0 revoke leftover", lambda: (open_dialog(pg), revoke_all(pg))[1])
    def create_ai():
        d = D(pg)
        d.get_by_placeholder("예: 월간 성과 보고서").fill("AUDIT-TEST 주간 보고서")
        d.get_by_placeholder("리포트를 받는 분께 전할 내용을 입력하세요").fill("AUDIT-TEST 메모입니다.")
        sw = d.get_by_label("리포트 관련 AI 채팅 활성화")
        info = {"ai switch found": sw.count()}
        if sw.count():
            info["before"] = sw.first.get_attribute("aria-checked") or sw.first.get_attribute("data-state")
            sw.first.click(); pg.wait_for_timeout(300); info["after"] = sw.first.get_attribute("aria-checked") or sw.first.get_attribute("data-state")
        # 함께 보기 CTR + 클릭
        for m in ("CTR", "클릭"):
            lab = d.locator("label", has_text=re.compile(f"^{m}$")).last  # 두 번째(함께 보기) 라벨
            lab.click(); pg.wait_for_timeout(200)
        # 기간: 최근 30일
        d.get_by_role("combobox").nth(0).click(); pg.wait_for_timeout(300); pg.get_by_role("option", name="최근 30일").click(); pg.wait_for_timeout(300)
        vshot(pg, "22-report-dialog-ai", True)
        n0 = len(API)
        d.get_by_role("button", name="링크 만들기").click(); pg.wait_for_timeout(3500)
        info["api"] = [(m, s, u[-70:], b[:300]) for m, s, u, b in API[n0:]]
        info["tail"] = D(pg).inner_text()[-400:].replace("\n"," | ")
        return info
    step("1 create with AI", create_ai)
    url = None
    for m, s, u, b in API:
        mm = re.search(r"https?://[^\"\\s]+", b)
        if m == "POST" and s < 300 and mm: url = mm.group(0)
    if not url:
        for m, s, u, b in API:
            mt = re.search(r'"(token|slug|code|id)"\s*:\s*"([^"]+)"', b)
            if m == "POST" and s < 300 and mt: R["token guess"] = mt.group(0)
    R["share url"] = url
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    if url:
        p2 = pg.context.new_page(); errs = []
        p2.on("console", lambda m: errs.append(m.text[:200]) if m.type == "error" else None)
        p2.on("response", lambda r: errs.append((r.status, r.url[-80:])) if r.status >= 400 else None)
        p2.goto(url, wait_until="networkidle"); p2.wait_for_timeout(3000)
        def pub():
            vshot(p2, "23-public-report", True)
            return {"url": p2.url, "title": p2.title(), "text": p2.locator("body").inner_text()[:3000].replace("\n"," | "), "canvas": p2.locator("canvas").count(), "svg": p2.locator("svg").count(), "tables": p2.locator("table").count(),
                    "buttons": [b for b in p2.locator("button").all_inner_texts() if b.strip()][:20], "inputs": [(i.get_attribute("placeholder")) for i in p2.locator("textarea,input").all()], "links": [(a.inner_text()[:30], a.get_attribute("href")) for a in p2.locator("a").all()][:10]}
        step("2 public page", pub)
        def chat():
            box = p2.locator("textarea").last if p2.locator("textarea").count() else p2.locator("input[type=text]").last
            if not box.count(): return "no box"
            box.fill("이 보고서에서 CTR이 가장 높은 날은 언제야?"); p2.wait_for_timeout(300)
            sb = p2.get_by_role("button", name=re.compile("질문|보내기|전송|Send|Ask"))
            if sb.count(): sb.last.click()
            else: p2.keyboard.press("Enter")
            t0 = time.time(); body = ""
            while time.time() - t0 < 120:
                p2.wait_for_timeout(3000); body = p2.locator("body").inner_text()
                if re.search(r"9개|9 ", body) or "오류" in body or "잠시" in body: break
            vshot(p2, "24-public-report-chat", True)
            return {"elapsed": round(time.time()-t0), "tail": body[-1500:].replace("\n"," | ")}
        step("2 viewer chat", chat)
        def mobile():
            p2.set_viewport_size({"width":390,"height":844}); p2.wait_for_timeout(1500); vshot(p2, "25-public-390", True)
            w = p2.evaluate("document.documentElement.scrollWidth"); p2.set_viewport_size({"width":1440,"height":1000}); return {"scrollWidth@390": w}
        step("2 mobile", mobile)
        R["2 public errors"] = errs[:20]
        # 소유자 로그
        go(pg, "/campaigns/83901859", 2500)
        def owner():
            d = open_dialog(pg); vshot(pg, "26-owner-list", True)
            out = {"buttons": d.get_by_role("button").all_inner_texts()[-8:], "tail": d.inner_text()[-500:].replace("\n"," | ")}
            b = d.get_by_role("button", name=re.compile("질문|로그|기록|대화|채팅"))
            if b.count():
                b.first.click(); pg.wait_for_timeout(2500); vshot(pg, "27-owner-log", True); out["log"] = D(pg).inner_text()[-1200:].replace("\n"," | ")
            return out
        step("3 owner log", owner)
        def revoke():
            d = D(pg)
            if not d.count(): d = open_dialog(pg)
            n, c = revoke_all(pg); vshot(pg, "28-after-revoke", True)
            return {"revoked": n, "confirm": c, "toast": toast(pg)[:2], "tail": D(pg).inner_text()[-300:].replace("\n"," | ")}
        step("3 revoke", revoke)
        pg.keyboard.press("Escape")
        def after():
            p2.goto(url, wait_until="networkidle"); p2.wait_for_timeout(2000); vshot(p2, "29-public-after-revoke"); return p2.locator("body").inner_text()[:400].replace("\n"," | ")
        step("3 revoked page", after)
        p2.close()
    # 소재 탭 기간 넓히기
    go(pg, "/campaigns/83901859", 2500)
    def creatives():
        pg.get_by_role("tab", name="소재").click(); pg.wait_for_timeout(2500)
        cb = pg.locator("main").get_by_role("combobox").first
        out = {"combobox": cb.inner_text() if cb.count() else None}
        if cb.count():
            cb.click(); pg.wait_for_timeout(300); opts = pg.get_by_role("option").all_inner_texts(); out["options"] = opts
            pick = [o for o in opts if "1년" in o or "365" in o or "전체" in o or "지금까지" in o]
            pg.get_by_role("option", name=(pick or opts)[-1]).click(); pg.wait_for_timeout(4000)
        else:
            btn = pg.locator("main button").filter(has_text=re.compile("최근 30일")).first
            if btn.count():
                btn.click(); pg.wait_for_timeout(500); out["menu"] = pg.get_by_role("menuitem").all_inner_texts() + pg.get_by_role("option").all_inner_texts()
                m = pg.get_by_role("menuitem", name=re.compile("1년|전체")); o = pg.get_by_role("option", name=re.compile("1년|전체"))
                (m if m.count() else o).first.click(); pg.wait_for_timeout(4000)
        vshot(pg, "30-creatives-wide", True)
        out.update({"headers": pg.locator("main thead th").all_inner_texts(), "rows": [r[:100].replace("\n"," ") for r in rows(pg)[:4]], "imgs": pg.locator("main img").count(), "text": main_text(pg, 600)})
        th = pg.locator("main thead th").filter(has_text=re.compile("노출|클릭")).first
        if th.count(): th.click(); pg.wait_for_timeout(1500); out["after sort"] = [r[:80].replace("\n"," ") for r in rows(pg)[:2]]
        return out
    step("5 creatives", creatives)
    # 일괄 편집
    go(pg, "/campaigns", 2500)
    def bulk():
        tr = pg.locator("tbody tr").first; tr.locator("[role=checkbox]").first.click(); pg.wait_for_timeout(600)
        pg.get_by_role("button", name=re.compile(r"^작업 \(")).click(); pg.wait_for_timeout(600)
        items = pg.get_by_role("menuitem").all_inner_texts()
        pg.get_by_role("menuitem", name=re.compile("일괄 편집")).click(); pg.wait_for_timeout(1500); vshot(pg, "31-bulk-edit", True)
        d = D(pg); out = {"menu": items, "text": d.inner_text()[:900].replace("\n"," | "), "labels": d.locator("label").all_inner_texts(), "buttons": d.get_by_role("button").all_inner_texts(), "inputs": [(i.get_attribute("type"), i.get_attribute("placeholder")) for i in d.locator("input").all()]}
        pg.keyboard.press("Escape"); pg.wait_for_timeout(300); return out
    step("8 bulk edit", bulk)
    # 내 데이터/팀 전체 상태 표시
    def scope():
        a = pg.get_by_role("button", name="내 데이터"); b = pg.get_by_role("button", name="팀 전체")
        attrs = lambda l: {k: l.get_attribute(k) for k in ("aria-pressed","data-state","aria-checked","class")}
        out = {"내 데이터": attrs(a), "팀 전체": attrs(b)}
        a.click(); pg.wait_for_timeout(2000); out["after click 내 데이터"] = {"내": attrs(a), "팀": attrs(b), "rows": len(rows(pg))}; vshot(pg, "32-scope-mine")
        b.click(); pg.wait_for_timeout(2000); out["after click 팀 전체"] = {"내": attrs(a), "팀": attrs(b), "rows": len(rows(pg))}
        return out
    step("6 scope", scope)
    print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
run(t)
