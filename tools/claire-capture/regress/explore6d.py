"""탐색 6d: 가이드용 보고서 링크 — 기간 지정(2026-07-01~08-31)으로 캠페인·그룹 링크 생성, 공개 페이지(데이터 있음) 캡처, 뷰어 질문, 소유자 '받은 질문', 끝나면 끊기."""
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
        pg.locator("[role=alertdialog], [role=dialog]").last.get_by_role("button").filter(has_text=re.compile("끊기")).last.click(); pg.wait_for_timeout(2000); n += 1
    return n
def create(pg, title, shot, per_campaign=False):
    d = D(pg); n0 = len(API)
    d.get_by_placeholder("예: 월간 성과 보고서").fill(title)
    d.get_by_placeholder("리포트를 받는 분께 전할 내용을 입력하세요").fill("7~8월 협력광고 캠페인 성과입니다. 8월 둘째 주부터 CTR이 개선됐습니다.")
    d.get_by_label("리포트 관련 AI 채팅 활성화").first.click(); pg.wait_for_timeout(200)
    if per_campaign:
        sw = d.get_by_label("캠페인별")
        if sw.count() and (sw.first.get_attribute("aria-checked") != "true"): sw.first.click(); pg.wait_for_timeout(200)
    for m in ("CTR", "클릭"): d.locator("label", has_text=re.compile(f"^{m}$")).last.click(); pg.wait_for_timeout(150)
    d.get_by_role("combobox").nth(0).click(); pg.wait_for_timeout(300); pg.get_by_role("option", name="기간 지정").click(); pg.wait_for_timeout(500)
    dates = d.locator("input[type=date]"); info = {"date inputs": dates.count()}
    if dates.count() >= 2: dates.nth(0).fill("2026-07-01"); dates.nth(1).fill("2026-08-31")
    else:
        info["text after 기간 지정"] = d.inner_text()[-500:].replace("\n"," | ")
    pg.wait_for_timeout(300); vshot(pg, shot, True)
    d.get_by_role("button", name="링크 만들기").click(); pg.wait_for_timeout(3500)
    info["toast"] = toast(pg)[:2]
    for m, s, u, b in API[n0:]:
        mt = re.search(r'"token"\s*:\s*"([^"]+)"', b)
        if s == 201 and mt: info["url"] = BASE + "/share/" + mt.group(1)
        else: info["api"] = (s, b[:300])
    return info
def view(pg, url, prefix, ask=True):
    p2 = pg.context.new_page(); errs = []
    p2.on("console", lambda m: errs.append(m.text[:200]) if m.type == "error" else None)
    p2.on("response", lambda r: errs.append((r.status, r.url[-80:])) if r.status >= 400 else None)
    p2.goto(url, wait_until="networkidle"); p2.wait_for_timeout(4000)
    out = {"text": p2.locator("body").inner_text()[:2500].replace("\n"," | "), "svg": p2.locator("svg").count(), "canvas": p2.locator("canvas").count(), "tables": p2.locator("table").count()}
    vshot(p2, f"{prefix}-public", True)
    if ask:
        p2.get_by_role("button", name="리포트에 대해 질문하기").click(); p2.wait_for_timeout(1500)
        out["box"] = {"placeholders": [i.get_attribute("placeholder") for i in p2.locator("textarea,input").all()], "buttons": [b for b in p2.locator("button").all_inner_texts() if b.strip()][:12], "text": p2.locator("body").inner_text()[-600:].replace("\n"," | ")}
        vshot(p2, f"{prefix}-public-chatbox", True)
        box = p2.locator("textarea").last if p2.locator("textarea").count() else p2.locator("input").last
        box.fill("이 기간에 CTR이 가장 높았던 날은 언제이고 얼마였어?"); p2.wait_for_timeout(300)
        sb = p2.get_by_role("button", name=re.compile("질문|보내기|전송|Send|Ask"))
        (sb.last.click() if sb.count() else p2.keyboard.press("Enter"))
        t0 = time.time(); body = ""
        while time.time() - t0 < 150:
            p2.wait_for_timeout(3000); body = p2.locator("body").inner_text()
            if re.search(r"9개|오류|실패|잠시 후|다시 시도", body): break
        out["chat"] = {"elapsed": round(time.time()-t0), "tail": body[-1500:].replace("\n"," | ")}
        vshot(p2, f"{prefix}-public-chat", True)
    p2.set_viewport_size({"width":390,"height":844}); p2.wait_for_timeout(1500); vshot(p2, f"{prefix}-public-390", True)
    out["scrollWidth@390"] = p2.evaluate("document.documentElement.scrollWidth"); out["errors"] = errs[:15]
    p2.close(); return out
def t(pg):
    pg.on("response", lambda r: API.append((r.request.method, r.status, r.url, r.text())) if "report-shares" in r.url and r.request.method == "POST" else None)
    # 캠페인
    go(pg, "/campaigns/83901859", 2500); open_dialog(pg); revoke_all(pg)
    step("1 campaign create", lambda: create(pg, "협력광고 7~8월 성과 보고서", "41-dialog-campaign-filled"))
    cu = (R["1 campaign create"] or {}).get("url") if isinstance(R["1 campaign create"], dict) else None
    vshot(pg, "42-dialog-campaign-created", True); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    if cu: step("2 campaign public", lambda: view(pg, cu, "43-campaign"))
    def owner():
        go(pg, "/campaigns/83901859", 2500); d = open_dialog(pg)
        d.get_by_role("button", name="받은 질문").first.click(); pg.wait_for_timeout(2500); vshot(pg, "44-owner-questions", True)
        return pg.locator("[role=dialog]").last.inner_text()[-900:].replace("\n"," | ")
    step("3 owner questions", owner)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    # 그룹
    go(pg, "/campaign-groups/82936400", 2500); open_dialog(pg); revoke_all(pg)
    step("4 group create", lambda: create(pg, "브랜드B 7~8월 성과 보고서", "45-dialog-group-filled", per_campaign=True))
    gu = R["4 group create"].get("url") if isinstance(R["4 group create"], dict) else None
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    if gu: step("5 group public", lambda: view(pg, gu, "46-group", ask=False))
    # 정리: 둘 다 끊기 (가이드 캡처는 끝났음)
    def cleanup():
        n = 0
        for path in ("/campaigns/83901859", "/campaign-groups/82936400"):
            go(pg, path, 2500); open_dialog(pg); n += revoke_all(pg); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        return n
    step("6 cleanup revoked", cleanup)
    R["urls"] = {"campaign": cu, "group": gu}
    print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
run(t)
