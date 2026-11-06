"""가이드 문서 용어 vs 실제 화면 라벨 대조 (가이드 조직). 사이드바(ko/en), 주요 화면의 제목·탭·버튼·라벨 수집."""
import sys, re, json; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt, os
from deck_shots import _set_language
wt.OUT = "out/docvsui"
S = str(__import__("pathlib").Path(__file__).parent / "out")
PAGES = ["/", "/dashboards", "/visualizations", "/visualizations/new", "/campaign-groups", "/campaign-groups/new", "/campaigns", "/my-chats", "/chats",
         "/metric-categories", "/metric-formulas", "/kpis", "/kpis/new", "/alerts", "/alerts/new", "/alert-events", "/custom-summaries", "/custom-summaries/new",
         "/reports", "/reports/new", "/organization-settings", "/platform-integrations", "/platform-integrations/new", "/communication-groups",
         "/org/users", "/org/user-groups", "/org/policies", "/api-keys", "/profile", "/preferences", "/security"]
def sidebar(pg):
    for b in pg.locator("nav button[aria-expanded='false'], aside button[aria-expanded='false']").all():
        try: b.click(); pg.wait_for_timeout(200)
        except Exception: pass
    return pg.locator("nav, aside").first.evaluate("""n=>Array.from(n.querySelectorAll('a,button,div[class*=group],span[class*=label],h2,h3,p')).map(e=>({t:(e.innerText||'').trim().split('\\n')[0].slice(0,30),h:e.getAttribute('href')})).filter(x=>x.t)""")
def page_labels(pg):
    return pg.locator("main").evaluate("""m=>({
      h:[...m.querySelectorAll('h1,h2,h3')].map(e=>e.innerText.trim().slice(0,60)).filter(Boolean).slice(0,12),
      tabs:[...m.querySelectorAll('[role=tab]')].map(e=>e.innerText.trim()).filter(Boolean).slice(0,12),
      btns:[...m.querySelectorAll('button,a.button,[role=button]')].map(e=>e.innerText.trim().split('\\n')[0]).filter(t=>t&&t.length<30).slice(0,25),
      labels:[...m.querySelectorAll('label,th')].map(e=>e.innerText.trim()).filter(t=>t&&t.length<40).slice(0,30),
      first:m.innerText.replace(/\\s+/g,' ').slice(0,300)})""")
def t(pg):
    out = {}
    for lang in ("ko", "en"):
        _set_language(pg, lang); pg.goto(BASE + "/", wait_until="networkidle"); pg.wait_for_timeout(1000)
        out[f"sidebar_{lang}"] = sidebar(pg)
        # 상단 사용자 메뉴
        try:
            pg.locator("header button, header [role=button]").last.click(timeout=2000); pg.wait_for_timeout(400)
            out[f"usermenu_{lang}"] = [x for x in pg.get_by_role("menuitem").all_inner_texts()]; pg.keyboard.press("Escape")
        except Exception as e: out[f"usermenu_{lang}"] = str(e)[:60]
    _set_language(pg, "ko")
    for p in PAGES:
        try:
            pg.goto(BASE + p, wait_until="networkidle", timeout=40000); pg.wait_for_timeout(1200)
            out[p] = dict(url=pg.url[len(BASE):], **page_labels(pg))
            if p in ("/campaigns", "/campaign-groups", "/custom-summaries", "/reports", "/alerts", "/visualizations", "/kpis", "/metric-formulas", "/communication-groups") and pg.locator("tbody tr").count():
                # 상세 화면 + 행 메뉴
                tr = pg.locator("tbody tr").first
                try: tr.locator("button").last.click(timeout=2000); pg.wait_for_timeout(400); out[p]["rowmenu"] = pg.get_by_role("menuitem").all_inner_texts(); pg.keyboard.press("Escape")
                except Exception: pass
                a = tr.locator("a")
                if a.count():
                    a.first.click(); pg.wait_for_timeout(2000); out[p + " [detail]"] = dict(url=pg.url[len(BASE):], **page_labels(pg))
            if p == "/campaigns" and pg.locator("tbody tr").count():
                pg.goto(BASE + p, wait_until="networkidle"); pg.wait_for_timeout(1000); pg.locator("tbody tr input[type=checkbox]").first.check(force=True); pg.wait_for_timeout(500)
                out[p]["bulk"] = [b for b in pg.locator("main button").all_inner_texts() if b.strip()][:15]
        except Exception as e: out[p] = {"err": str(e).split("\n")[0][:120]}
    json.dump(out, open(f"{S}/ui_labels.json", "w"), ensure_ascii=False, indent=1)
    print("saved", len(out))
run(t)
