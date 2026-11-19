"""데모 팀 pMax·YT Search On 캠페인에 [지금 수집] → [캠페인 전체 기간] → [데이터 수집]. 끝나면 Product 복귀."""
import re, json
from playwright.sync_api import sync_playwright
from capture import BASE, _context, _collect_dialog
CODES = ["44852176", "38448161"]
R = {}

def switch(page, team):
    btn = page.get_by_role("button", name=re.compile("팀 전환"))
    if team in btn.inner_text(): return
    btn.click(); page.wait_for_timeout(500)
    page.get_by_role("menuitem", name=team).click(); page.wait_for_load_state("networkidle"); page.wait_for_timeout(1500)

with sync_playwright() as p:
    ctx = _context(p, False); page = ctx.pages[0] if ctx.pages else ctx.new_page()
    resp = []
    page.on("response", lambda r: resp.append((r.request.method, r.url.split(".com")[-1], r.status)) if r.request.method == "POST" and "/campaigns/" in r.url else None)
    page.goto(BASE + "/campaigns", wait_until="networkidle"); page.wait_for_timeout(1000)
    try:
        switch(page, "데모")
        for code in CODES:
            page.goto(f"{BASE}/campaigns/{code}", wait_until="networkidle"); page.wait_for_timeout(1500)
            _collect_dialog(page)
            d = page.locator("[role=dialog]").last
            d.get_by_role("button", name="캠페인 전체 기간").click(); page.wait_for_timeout(600)
            rng = d.inner_text().replace("\n", " | ")[:300]
            resp.clear()
            d.get_by_role("button", name="데이터 수집").click(); page.wait_for_timeout(5000)
            toast = page.locator("[data-sonner-toast], [role=status], li[role=alert]").all_inner_texts()
            R[code] = {"range": rng, "post": list(resp), "toast": toast, "dialog_open": page.locator("[role=dialog]").count()}
            print(code, json.dumps(R[code], ensure_ascii=False)[:600])
    finally:
        page.keyboard.press("Escape"); page.goto(BASE + "/campaigns", wait_until="networkidle"); page.wait_for_timeout(1000); switch(page, "Product"); ctx.close()
        json.dump(R, open("regress/out/collect_now.json", "w"), ensure_ascii=False, indent=1)
