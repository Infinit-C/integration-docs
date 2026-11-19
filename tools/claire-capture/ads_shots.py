"""소재 탭 캡처 (팀 전환 포함). 실고객 이름·소재 이름은 블러, 썸네일은 약하게 블러. 끝나면 Product 팀으로 복귀."""
import re, json
from playwright.sync_api import sync_playwright
from capture import BASE, OUT, BLUR_JS, SENSITIVE, _context
EXTRA = ["GUGUS", "Gugus", "gugus", "구구스", "T MAP", "TMAP", "Tmap", "SearchOn", "Search On", "JungKwanJang", "정관장",
         "뉴키키", "Newkiki", "BSN", "pMax"]
# (팀, 캠페인 코드, 파일 이름, 기간)
TARGETS = [
    ("데모", "69042985", "campaign-ads-tab-meta", "최근 90일"),
    ("데모", "44852176", "campaign-ads-tab-google", "최근 90일"),
    ("운영팀", "80116610", "campaign-ads-tab-dv360", "최근 90일"),
    ("데모", "38448161", "campaign-ads-tab-dv360-yt", "최근 90일"),
]
R = {}

def switch(page, team):
    btn = page.get_by_role("button", name=re.compile("팀 전환"))
    if team in btn.inner_text(): return
    btn.click(); page.wait_for_timeout(500)
    page.get_by_role("menuitem", name=team).click(); page.wait_for_load_state("networkidle"); page.wait_for_timeout(1500)

def ads_tab(page, code, period):
    page.goto(f"{BASE}/campaigns/{code}", wait_until="networkidle"); page.wait_for_timeout(1500)
    page.get_by_role("tab", name=re.compile("소재")).click(); page.wait_for_timeout(2500)
    cb = page.locator("main").get_by_role("combobox").filter(has_text=re.compile("최근")).first
    if cb.count() and period not in cb.inner_text():
        cb.click(); page.wait_for_timeout(300); page.get_by_role("option", name=period).click(); page.wait_for_timeout(2500)
    main = page.locator("main").inner_text()
    return (page.locator("main table tbody tr").count(), main[main.find("소재별 성과"):][:400].replace("\n"," | "))

BLUR_NAMES = """() => {
  document.querySelectorAll('main table tbody tr td:first-child').forEach(td => {
    td.querySelectorAll('img').forEach(i => { i.style.filter = 'blur(5px)'; });
    td.querySelectorAll('*').forEach(e => { if (e.children.length === 0 && e.tagName !== 'IMG' && (e.textContent||'').trim()) e.style.filter = 'blur(7px)'; });
  });
}"""

with sync_playwright() as p:
    ctx = _context(p, False); page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto(BASE + "/campaigns", wait_until="networkidle"); page.wait_for_timeout(1000)
    try:
        for team, code, name, period in TARGETS:
            switch(page, team)
            R[name] = ads_tab(page, code, period)
            page.evaluate(BLUR_JS, SENSITIVE + EXTRA); page.evaluate(BLUR_NAMES); page.wait_for_timeout(300)
            page.screenshot(path=str(OUT / f"{name}.png"))
            if R[name][0] > 1:  # 정렬 반전 확인
                h = page.locator("main table thead th").filter(has_text=re.compile("노출")).first
                h.click(); page.wait_for_timeout(700); a = page.locator("main table tbody tr td:nth-child(3)").first.inner_text()
                h.click(); page.wait_for_timeout(700); b = page.locator("main table tbody tr td:nth-child(3)").first.inner_text()
                R[name + "_sort"] = (a, b)
    finally:
        switch(page, "Product"); ctx.close()
        json.dump(R, open("out/ads_shots.json","w"), ensure_ascii=False, indent=1)
        for k, v in R.items(): print(k, "=>", str(v)[:500])
