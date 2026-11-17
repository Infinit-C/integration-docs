"""클릭 탐색 점검: 목록 정렬·페이지 크기·행 메뉴(읽기성 항목만)·새로 만들기 폼 빈 제출 검증·상세 ⋮ 메뉴·탭·편집 모드 진입/취소·
시각화 유형 전환·필터 자동완성·다크모드·영문·좁은 폭. 삭제/비활성/발송/연결 류는 절대 누르지 않는다."""
import sys, re, json, time; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt
wt.OUT = "out/explore"
R = {}; ERR = []
SAFE = re.compile("수정|편집|상세|보기|JSON 내보내기|이름 변경|계속 채팅|평가 기록|미리보기|복사")
DANGER = re.compile("삭제|비활성|활성화|발송|보내기|연결 끊기|연결 해제|재수집|수집|초대|재발급|폐기|실행|Delete|Disable|Enable|Send|Run")
LISTS = ["/campaigns", "/campaign-groups", "/visualizations", "/dashboards", "/kpis", "/metric-formulas", "/metric-categories", "/alerts", "/alert-events",
         "/custom-summaries", "/reports", "/communication-groups", "/platform-integrations", "/org/users", "/org/user-groups", "/org/policies", "/api-keys", "/my-chats", "/chats"]
NEWS = ["/campaign-groups/new", "/visualizations/new", "/kpis/new", "/metric-formulas/new", "/alerts/new", "/custom-summaries/new", "/reports/new", "/org/user-groups/new", "/org/policies/new", "/org/users/new", "/dashboards/new"]
def go(pg, path, wait=1500): pg.goto(BASE+path, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(wait)
def vshot(pg, name): pg.screenshot(path=f"{wt.OUT}/{name}.png")
def mark(step):
    """이 단계에서 새로 생긴 콘솔/HTTP 오류를 step 이름으로 묶는다."""
    n = len(wt.log)
    def done():
        new = [l for l in wt.log[n:] if l[0] in ("console", "http")]
        if new: ERR.append((step, new[:4]))
    return done
def step(pg, name, fn):
    d = mark(name)
    try: r = fn(); R[name] = r if r is not None else "ok"
    except Exception as e: R[name] = "ERR " + str(e).split("\n")[0][:160]; vshot(pg, "err-" + re.sub(r"[^\w]+", "_", name)[:60])
    d()
def lists(pg):
    for p in LISTS:
        def f(p=p):
            go(pg, p); out = {"rows": pg.locator("tbody tr").count(), "h1": main_text(pg, 80)}
            # 정렬 헤더 두 번씩
            ths = pg.locator("thead th").all(); sorted_cols = []
            for th in ths[:6]:
                t = th.inner_text().strip()
                if not t or not (th.locator("button, svg").count()): continue
                try: th.locator("button, [role=button], svg").first.click(timeout=1500); pg.wait_for_timeout(700); th.locator("button, [role=button], svg").first.click(timeout=1500); pg.wait_for_timeout(700); sorted_cols.append(t)
                except Exception: pass
            out["sorted"] = sorted_cols
            # 페이지당 행 수
            sel = pg.locator("main [role=combobox]").filter(has_text=re.compile("^(10|20|25|50|100)$"))
            if sel.count():
                sel.first.click(); pg.wait_for_timeout(400); o = pg.get_by_role("option").filter(has_text=re.compile("^(10|20|25)$"))
                if o.count(): o.first.click(); pg.wait_for_timeout(1000); out["pagesize"] = main_text(pg, 2000).split("페이지당 행 수")[-1][:30]
                else: pg.keyboard.press("Escape")
            # 행 메뉴 (첫 행)
            tr = pg.locator("tbody tr").first
            if tr.count() and tr.locator("button").count():
                tr.locator("button").last.click(); pg.wait_for_timeout(500); items = pg.get_by_role("menuitem").all_inner_texts(); out["rowmenu"] = items; pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
                for it in items:
                    if DANGER.search(it) or not SAFE.search(it): continue
                    tr = pg.locator("tbody tr").first; tr.locator("button").last.click(); pg.wait_for_timeout(400)
                    pg.get_by_role("menuitem", name=it, exact=True).first.click(); pg.wait_for_timeout(1500)
                    d = dlg(pg); out[f"menu:{it}"] = {"url": pg.url[len(BASE):], "dialog": d and d[0][:100], "toast": toast(pg)[:1]}
                    if d: 
                        c = pg.locator("[role=dialog] button, [role=alertdialog] button").filter(has_text=re.compile("취소|닫기|Close|확인"))
                        (c.first.click() if c.count() else pg.keyboard.press("Escape")); pg.wait_for_timeout(500)
                    if pg.url[len(BASE):] != p: go(pg, p, 1000)
            # 첫 행 클릭 → 상세
            a = pg.locator("tbody tr").first.locator("a")
            if a.count(): a.first.click(); pg.wait_for_timeout(1800); out["detail"] = {"url": pg.url[len(BASE):], "tabs": pg.get_by_role("tab").all_inner_texts(), "btns": [b for b in pg.locator("main button").all_inner_texts() if b.strip()][:10]}
            return out
        step(pg, f"list {p}", f)
def news(pg):
    for p in NEWS:
        def f(p=p):
            go(pg, p); out = {"url": pg.url[len(BASE):], "labels": [l.inner_text()[:16] for l in pg.locator("main label").all()][:12]}
            b = pg.locator("main button").filter(has_text=re.compile("^(생성|저장|계속|.* 생성|.* 추가|초대 보내기|만들기)$")).last
            if b.count():
                out["submit"] = b.inner_text(); out["enabled"] = b.is_enabled()
                if b.is_enabled():
                    b.click(); pg.wait_for_timeout(1500); out["after url"] = pg.url[len(BASE):]; out["toast"] = toast(pg)[:2]
                    out["validation"] = [t for t in pg.locator("main [role=alert], main p, main span").all_inner_texts() if re.search("필수|입력|선택|required|invalid|올바", t)][:4]
                    if out["after url"] != p: out["!! navigated"] = True
            return out
        step(pg, f"new {p}", f)
def details(pg):
    def camp():
        go(pg, "/campaigns/83901859", 2500); out = {"tabs": pg.get_by_role("tab").all_inner_texts()}
        for tab in out["tabs"]: pg.get_by_role("tab", name=tab, exact=True).click(); pg.wait_for_timeout(1500); out[f"tab {tab}"] = main_text(pg, 120)
        pg.get_by_role("tab", name=out["tabs"][0], exact=True).click(); pg.wait_for_timeout(800)
        mb = pg.locator("main button[aria-haspopup='menu']").last; mb.click(); pg.wait_for_timeout(500); items = pg.get_by_role("menuitem").all_inner_texts(); out["menu"] = items; pg.keyboard.press("Escape")
        for it in items:
            if DANGER.search(it) or not re.search("수정|KPI|사용자 지정", it): continue
            mb.click(); pg.wait_for_timeout(400); pg.get_by_role("menuitem", name=it, exact=True).click(); pg.wait_for_timeout(2000)
            out[f"menu:{it}"] = {"url": pg.url[len(BASE):], "head": main_text(pg, 150), "dialog": (dlg(pg) or [None])[0]}
            vshot(pg, "camp-" + re.sub(r"\W+", "_", it)[:20])
            c = pg.locator("main button, [role=dialog] button").filter(has_text=re.compile("^(취소|닫기|편집 취소|Cancel)$"))
            if c.count(): c.last.click(); pg.wait_for_timeout(800)
            if "/campaigns/83901859" not in pg.url: go(pg, "/campaigns/83901859", 2000)
            cd = dlg(pg)
            if cd: out[f"menu:{it} leave-dialog"] = cd[0][:100]; confirm(pg, "나가기|확인|계속|취소")
        return out
    step(pg, "campaign detail", camp)
    def grp():
        go(pg, "/campaign-groups/50103304", 2500); out = {"tabs": pg.get_by_role("tab").all_inner_texts(), "btns": [b for b in pg.locator("main button").all_inner_texts() if b.strip()][:8]}
        b = pg.locator("main button").filter(has_text=re.compile("^사용자 지정$"))
        if b.count():
            b.first.click(); pg.wait_for_timeout(2000); out["customize"] = {"url": pg.url[len(BASE):], "btns": [x for x in pg.locator("main button").all_inner_texts() if x.strip()][:10], "dialog": (dlg(pg) or [None])[0]}; vshot(pg, "group-customize")
            c = pg.locator("main button, [role=dialog] button").filter(has_text=re.compile("^(취소|편집 취소|닫기)$"))
            if c.count(): c.last.click(); pg.wait_for_timeout(800); out["customize cancel"] = main_text(pg, 100)
        mb = pg.locator("main button[aria-haspopup='menu']")
        if mb.count(): mb.last.click(); pg.wait_for_timeout(400); out["menu"] = pg.get_by_role("menuitem").all_inner_texts(); pg.keyboard.press("Escape")
        return out
    step(pg, "group detail", grp)
    def kpi():
        go(pg, "/campaigns/83901859/kpis/edit", 2500); out = {"head": main_text(pg, 300), "btns": [b for b in pg.locator("main button").all_inner_texts() if b.strip()][:12]}; vshot(pg, "kpi-edit"); return out
    step(pg, "kpi edit", kpi)
    def viz():
        go(pg, "/visualizations/78949445", 3000); out = {"head": main_text(pg, 120)}
        pg.get_by_role("tab", name="데이터").click(); pg.wait_for_timeout(500)
        cb = pg.locator("main [role=combobox]").first; cb.click(); pg.wait_for_timeout(400); opts = pg.get_by_role("option").all_inner_texts(); out["types"] = opts; pg.keyboard.press("Escape")
        for o in opts[:6]:
            cb = pg.locator("main [role=combobox]").first; cb.click(); pg.wait_for_timeout(300); pg.get_by_role("option", name=o, exact=True).click(); pg.wait_for_timeout(600)
            ap = pg.get_by_role("button", name=re.compile("미리보기 적용|적용"))
            if ap.count() and ap.first.is_enabled(): ap.first.click(); pg.wait_for_timeout(2500)
            out[f"type {o}"] = {"canvas": pg.locator("main canvas, main svg.recharts-surface, main table").count(), "err": [t for t in pg.locator("main").all_inner_texts()[0].split("\n") if re.search("오류|실패|error|failed", t, re.I)][:2], "toast": toast(pg)[:1]}
        for t in ("지표 및 축", "패널 설정"): pg.get_by_role("tab", name=t).click(); pg.wait_for_timeout(600); out[f"tab {t}"] = [l.inner_text()[:14] for l in pg.locator("main label").all()][:10]
        return out
    step(pg, "viz editor", viz)
    def filt():
        go(pg, "/campaigns"); inp = pg.locator("main input[type=text], main input:not([type])").first; inp.click(); inp.type("campaign.", delay=60); pg.wait_for_timeout(1200)
        out = {"suggest": pg.locator("[role=listbox] *, [role=option], [cmdk-item]").all_inner_texts()[:8]}
        inp.fill("campaign.status: enabled"); pg.get_by_role("button", name=re.compile("적용")).click(); pg.wait_for_timeout(1500); out["rows"] = pg.locator("tbody tr").count(); out["url"] = pg.url[len(BASE):][:80]
        inp.fill("campaign.name: ???"); pg.get_by_role("button", name=re.compile("적용")).click(); pg.wait_for_timeout(1500); out["bad query"] = main_text(pg, 400)[-200:]; out["toast"] = toast(pg)[:1]
        return out
    step(pg, "campaign filter", filt)
    def profile():
        go(pg, "/profile", 2000); out = {"labels": [l.inner_text()[:16] for l in pg.locator("main label").all()][:12], "btns": [b for b in pg.locator("main button").all_inner_texts() if b.strip()][:10], "tabs": pg.get_by_role("tab").all_inner_texts()}; vshot(pg, "profile"); return out
    step(pg, "profile", profile)
    def menus():
        go(pg, "/dashboards"); pg.locator("header button").last.click(); pg.wait_for_timeout(500); out = {"user menu": pg.get_by_role("menuitem").all_inner_texts()}; pg.keyboard.press("Escape")
        b = pg.locator("header button").nth(1); b.click(); pg.wait_for_timeout(600); out["bell"] = pg.evaluate("()=>[...document.querySelectorAll('[role=dialog],[data-radix-popper-content-wrapper]')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,150))"); pg.keyboard.press("Escape")
        pg.locator("header button").first.click(); pg.wait_for_timeout(600); out["search"] = pg.evaluate("()=>[...document.querySelectorAll('[role=dialog],[cmdk-root]')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,150))")
        if out["search"]: pg.keyboard.type("브랜드"); pg.wait_for_timeout(1200); out["search 브랜드"] = pg.evaluate("()=>[...document.querySelectorAll('[role=dialog],[cmdk-root]')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,300))"); vshot(pg, "search")
        pg.keyboard.press("Escape"); return out
    step(pg, "header menus", menus)
def modes(pg):
    def dark():
        go(pg, "/campaigns/83901859", 2500); btn = pg.locator("header button").filter(has=pg.locator("svg")).all()
        for b in btn:
            if re.search("dark|light|테마|모드", (b.get_attribute("aria-label") or "") + (b.get_attribute("title") or ""), re.I): b.click(); pg.wait_for_timeout(1200); break
        out = {"html class": pg.evaluate("()=>document.documentElement.className")}; vshot(pg, "dark-campaign"); go(pg, "/alerts/new", 2000); vshot(pg, "dark-alert-new")
        for b in pg.locator("header button").filter(has=pg.locator("svg")).all():
            if re.search("dark|light|테마|모드", (b.get_attribute("aria-label") or "") + (b.get_attribute("title") or ""), re.I): b.click(); pg.wait_for_timeout(800); break
        out["restored"] = pg.evaluate("()=>document.documentElement.className"); return out
    step(pg, "dark mode", dark)
    def narrow():
        out = {}
        for w in (1024, 390):
            pg.set_viewport_size({"width": w, "height": 900})
            for p in ("/campaigns", "/campaigns/83901859", "/alerts/new", "/visualizations/78949445"):
                go(pg, p, 1500); ov = pg.evaluate("()=>document.documentElement.scrollWidth>document.documentElement.clientWidth+2"); out[f"{w} {p}"] = {"overflow": ov}; vshot(pg, f"w{w}-{p.strip('/').replace('/','_')}")
        pg.set_viewport_size({"width": 1440, "height": 1000}); return out
    step(pg, "narrow widths", narrow)
    def english():
        _set_language(pg, "en"); out = {}
        for p in ("/campaigns/83901859", "/alerts/new", "/custom-summaries/new", "/profile"):
            go(pg, p, 1500); txt = main_text(pg, 3000); out[p] = [w for w in re.findall(r"[가-힣]{2,}[^|]*", txt)][:5]; vshot(pg, f"en-{p.strip('/').replace('/','_')}")
        _set_language(pg, "ko"); return out
    step(pg, "english leftovers", english)
def t(pg):
    for fn in (lists, news, details, modes):
        try: fn(pg)
        except Exception as e: R[f"FATAL {fn.__name__}"] = str(e)[:200]
    print(json.dumps(R, ensure_ascii=False, indent=1)); print("ERRORS", json.dumps(ERR, ensure_ascii=False, indent=1))
run(t)
