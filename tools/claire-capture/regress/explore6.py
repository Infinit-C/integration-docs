"""탐색 6 (PoC 전 점검): 보고서 링크 전체 흐름(생성→공개 페이지→뷰어 AI 질문→소유자 로그→수정→해지), 소재 탭, 내 데이터/팀 전체,
대시보드 탭, 일괄 편집, 알림 기준값, 팀 이력, 약관, 가입 화면, 반응형. AUDIT-TEST 데이터만 만들고 지운다."""
import sys, re, json, time; sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from wt import *
import wt
wt.OUT = "out/explore6"
R = {}; SHARE = {}
def go(pg, path, wait=1800): pg.goto(path if path.startswith("http") else BASE+path, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(wait)
def vshot(pg, name, full=False): pg.screenshot(path=f"{wt.OUT}/{name}.png", full_page=full)
def step(name, fn):
    n = len(wt.log)
    try: R[name] = fn()
    except Exception as e: R[name] = f"ERR {type(e).__name__}: {str(e)[:200]}"
    if len(wt.log) > n: R[name+" :log"] = wt.log[n:]
def D(pg): return pg.locator("[role=dialog]").last
def switch_by_label(pg, label, on=True):
    d = D(pg)
    lab = d.locator("label", has_text=re.compile(f"^{re.escape(label)}$")).first
    sw = None
    if lab.count():
        fid = lab.get_attribute("for")
        if fid: sw = d.locator(f"#{fid}")
    if not sw or not sw.count():
        sw = d.locator("[role=switch],[role=checkbox]").filter(has=pg.locator(f"xpath=ancestor::*[1]//*[normalize-space()='{label}']")).first
    if not sw.count(): return f"no switch {label}"
    cur = sw.get_attribute("aria-checked") == "true" or sw.get_attribute("data-state") == "checked"
    if cur != on: sw.click(); pg.wait_for_timeout(200)
    return (label, cur, on)

def t(pg):
    # ---------- 1. 보고서 링크 (캠페인) ----------
    go(pg, "/campaigns/83901859", 2500)
    def open_dialog():
        pg.get_by_role("button", name=re.compile("보고서 링크")).first.click(); pg.wait_for_timeout(2000); return D(pg).inner_text()[:200].replace("\n"," | ")
    step("1 open dialog", open_dialog)
    def fill_create():
        d = D(pg)
        d.get_by_placeholder("예: 월간 성과 보고서").fill("AUDIT-TEST 월간 성과 보고서")
        d.get_by_placeholder("리포트를 받는 분께 전할 내용을 입력하세요").fill("AUDIT-TEST 메모: 10월 대비 CTR 개선")
        out = {}
        out["ai"] = switch_by_label(pg, "리포트 관련 AI 채팅 활성화", True)
        # 함께 보기: CTR+클릭 체크
        for m in ("CTR", "클릭"):
            boxes = d.locator("[role=checkbox],[role=switch]")
            lab = d.locator("label", has_text=re.compile(f"^{m}$"))
            out[f"combo-{m}-labels"] = lab.count()
        vshot(pg, "01-report-dialog-filled", True)
        # 기간 콤보박스 옵션
        cbs = d.get_by_role("combobox"); cbs.nth(0).click(); pg.wait_for_timeout(400)
        out["period options"] = pg.get_by_role("option").all_inner_texts(); pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
        cbs.nth(1).click(); pg.wait_for_timeout(400)
        out["expiry options"] = pg.get_by_role("option").all_inner_texts(); pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
        d.get_by_role("button", name="링크 만들기").click(); pg.wait_for_timeout(3000)
        out["toast"] = toast(pg)[:2]
        out["after"] = D(pg).inner_text()[-900:].replace("\n"," | ") if D(pg).count() else "dialog closed"
        vshot(pg, "02-report-dialog-created", True)
        links = [a.get_attribute("href") for a in D(pg).locator("a[href*='/share'],a[href*='/r/'],a[href*='report']").all()] if D(pg).count() else []
        out["links"] = links
        # 복사 버튼 / URL 텍스트
        txt = D(pg).inner_text() if D(pg).count() else ""
        m = re.findall(r"https?://\S+", txt); out["urls in text"] = m
        SHARE["url"] = (links or m or [None])[0]
        out["buttons"] = D(pg).get_by_role("button").all_inner_texts() if D(pg).count() else []
        return out
    step("1 create link", fill_create)
    def copy_btn():
        d = D(pg); b = d.get_by_role("button", name=re.compile("복사|Copy"))
        if not b.count(): return "no copy button"
        b.first.click(); pg.wait_for_timeout(800)
        try: clip = pg.evaluate("navigator.clipboard.readText()")
        except Exception as e: clip = f"clipboard ERR {e}"
        if isinstance(clip, str) and clip.startswith("http"): SHARE["url"] = clip
        return {"toast": toast(pg)[:2], "clip": clip}
    step("1 copy link", copy_btn)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
    R["share url"] = SHARE.get("url")

    # ---------- 2. 공개 보고서 페이지 (로그아웃 컨텍스트) ----------
    if SHARE.get("url"):
        ctx2 = pg.context.browser.new_context(viewport={"width":1440,"height":1000}, locale="ko-KR") if pg.context.browser else None
        if ctx2 is None:
            # persistent context: browser 없음 → 새 플레이라이트 컨텍스트 대신 쿠키 없는 페이지로 대체 불가 → 같은 컨텍스트에서 시크릿 흉내: localStorage 토큰 제거 후 방문
            p2 = pg.context.new_page()
            p2.goto(SHARE["url"], wait_until="networkidle"); p2.wait_for_timeout(2500)
        else:
            p2 = ctx2.new_page(); p2.goto(SHARE["url"], wait_until="networkidle"); p2.wait_for_timeout(2500)
        errs = []
        p2.on("console", lambda m: errs.append(m.text[:200]) if m.type == "error" else None)
        p2.on("response", lambda r: errs.append((r.status, r.url[-80:])) if r.status >= 400 else None)
        def pub():
            vshot(p2, "03-public-report", True)
            return {"url": p2.url, "title": p2.title(), "h": p2.locator("h1,h2").all_inner_texts()[:12], "text": p2.locator("body").inner_text()[:2500].replace("\n"," | "),
                    "canvas": p2.locator("canvas").count(), "tables": p2.locator("table").count(), "buttons": [b for b in p2.locator("button").all_inner_texts() if b.strip()][:20],
                    "links": [(a.inner_text()[:30], a.get_attribute("href")) for a in p2.locator("a").all()][:10]}
        step("2 public page", pub)
        def pub_chat():
            box = p2.locator("textarea, input[type=text]").last
            if not box.count(): return "no question box"
            box.fill("이 보고서에서 CTR이 가장 높은 날은 언제야?"); p2.wait_for_timeout(300)
            p2.keyboard.press("Enter"); p2.wait_for_timeout(1500)
            sb = p2.get_by_role("button", name=re.compile("질문|보내기|전송|Send|Ask"))
            if sb.count() and sb.last.is_enabled(): sb.last.click()
            t0 = time.time(); last = ""
            while time.time() - t0 < 90:
                p2.wait_for_timeout(3000); txt = p2.locator("body").inner_text()
                if txt != last and ("남았" in txt or "답변" in txt or "오늘" in txt): last = txt
                if re.search(r"(9|아홉).{0,6}(남|left)|questions left|남은 질문", txt): break
            vshot(p2, "04-public-report-chat", True)
            return {"body tail": p2.locator("body").inner_text()[-1500:].replace("\n"," | "), "elapsed": round(time.time()-t0)}
        step("2 public chat", pub_chat)
        def pub_mobile():
            p2.set_viewport_size({"width": 390, "height": 844}); p2.wait_for_timeout(1500); vshot(p2, "05-public-report-390", True)
            w = p2.evaluate("document.documentElement.scrollWidth"); p2.set_viewport_size({"width":1440,"height":1000}); return {"scrollWidth@390": w}
        step("2 public mobile", pub_mobile)
        R["2 public errors"] = errs[:20]
        p2.close()
        if ctx2: ctx2.close()

    # ---------- 3. 소유자: 질문 로그 / 링크 수정 / 해지 ----------
    go(pg, "/campaigns/83901859", 2500)
    def owner_list():
        pg.get_by_role("button", name=re.compile("보고서 링크")).first.click(); pg.wait_for_timeout(2000)
        d = D(pg); vshot(pg, "06-report-dialog-list", True)
        tail = d.inner_text()[-1200:].replace("\n"," | ")
        # 만든 링크 영역의 버튼들
        return {"tail": tail, "buttons": d.get_by_role("button").all_inner_texts()[-12:]}
    step("3 owner list", owner_list)
    def owner_log():
        d = D(pg); b = d.get_by_role("button", name=re.compile("질문|로그|기록|대화"))
        if not b.count(): return "no log button: " + str(d.get_by_role("button").all_inner_texts()[-12:])
        b.first.click(); pg.wait_for_timeout(2500); vshot(pg, "07-report-question-log", True)
        return D(pg).inner_text()[-1500:].replace("\n"," | ")
    step("3 owner log", owner_log)
    def owner_edit():
        d = D(pg); b = d.get_by_role("button", name=re.compile("수정|편집|Edit"))
        if not b.count():
            back = d.get_by_role("button", name=re.compile("뒤로|닫기|Back")); 
            if back.count(): back.first.click(); pg.wait_for_timeout(800); d = D(pg); b = d.get_by_role("button", name=re.compile("수정|편집|Edit"))
        if not b.count(): return "no edit button: " + str(d.get_by_role("button").all_inner_texts()[-12:])
        b.first.click(); pg.wait_for_timeout(1500); vshot(pg, "08-report-edit", True)
        ti = d.get_by_placeholder("예: 월간 성과 보고서")
        val = ti.input_value() if ti.count() else None
        if ti.count(): ti.fill("AUDIT-TEST 월간 성과 보고서 (수정)")
        sb = d.get_by_role("button", name=re.compile("저장|변경|수정 완료|업데이트|Save"))
        names = d.get_by_role("button").all_inner_texts()
        if sb.count(): sb.last.click(); pg.wait_for_timeout(2500)
        return {"prefilled title": val, "buttons": names[-10:], "toast": toast(pg)[:2], "tail": D(pg).inner_text()[-500:].replace("\n"," | ") if D(pg).count() else "closed"}
    step("3 owner edit", owner_edit)
    def owner_revoke():
        d = D(pg)
        if not d.count(): pg.get_by_role("button", name=re.compile("보고서 링크")).first.click(); pg.wait_for_timeout(2000); d = D(pg)
        b = d.get_by_role("button", name=re.compile("해지|삭제|철회|Revoke"))
        if not b.count(): return "no revoke button: " + str(d.get_by_role("button").all_inner_texts()[-12:])
        b.first.click(); pg.wait_for_timeout(1000)
        c = dlg(pg); vshot(pg, "09-report-revoke-confirm", True)
        confirm(pg, "해지|삭제|철회|확인|Revoke")
        pg.wait_for_timeout(1500)
        return {"confirm": c, "toast": toast(pg)[:2], "tail": D(pg).inner_text()[-400:].replace("\n"," | ") if D(pg).count() else "closed"}
    step("3 owner revoke", owner_revoke)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    def revoked_page():
        if not SHARE.get("url"): return "no url"
        p3 = pg.context.new_page(); p3.goto(SHARE["url"], wait_until="networkidle"); p3.wait_for_timeout(2000)
        vshot(p3, "10-public-after-revoke"); t = p3.locator("body").inner_text()[:400].replace("\n"," | "); p3.close(); return t
    step("3 revoked page", revoked_page)

    # ---------- 4. 그룹 보고서 링크: 캠페인별 토글만 확인 (생성 안 함) ----------
    go(pg, "/campaign-groups/82936400", 2500)
    def grp():
        pg.get_by_role("button", name=re.compile("보고서 링크")).first.click(); pg.wait_for_timeout(2000)
        d = D(pg); vshot(pg, "11-report-dialog-group", True); t = d.inner_text(); pg.keyboard.press("Escape"); return "캠페인별" in t
    step("4 group dialog has 캠페인별", grp)

    # ---------- 5. 소재 탭 ----------
    go(pg, "/campaigns/83901859", 2500)
    def creatives():
        pg.get_by_role("tab", name="소재").click(); pg.wait_for_timeout(4000); vshot(pg, "12-creatives-tab", True)
        out = {"text": main_text(pg, 1500), "imgs": pg.locator("main img").count(), "headers": pg.locator("main thead th").all_inner_texts(), "rows": len(rows(pg))}
        th = pg.locator("main thead th").filter(has_text=re.compile("노출|클릭|지출")).first
        if th.count(): th.click(); pg.wait_for_timeout(1500); out["after sort"] = rows(pg)[:2]
        return out
    step("5 creatives tab", creatives)

    # ---------- 6. 내 데이터 / 팀 전체 ----------
    go(pg, "/campaigns", 2500)
    def scope():
        out = {"rows team?": len(rows(pg))}
        for lab in ("내 데이터", "팀 전체", "내 데이터"):
            pg.get_by_role("button", name=lab).click(); pg.wait_for_timeout(2500)
            out[lab] = {"rows": len(rows(pg)), "url": pg.url[-60:], "pressed": pg.get_by_role("button", name=lab).get_attribute("aria-pressed") or pg.get_by_role("button", name=lab).get_attribute("data-state")}
            vshot(pg, f"13-scope-{lab}")
        go(pg, "/dashboards", 2000); out["dashboards after"] = main_text(pg, 300)
        go(pg, "/platform-integrations", 2000); out["platform after"] = main_text(pg, 300)
        pg.get_by_role("button", name="팀 전체").click(); pg.wait_for_timeout(1500)
        return out
    step("6 my data toggle", scope)

    # ---------- 7. 대시보드 탭 ----------
    go(pg, "/dashboards", 2000)
    def dash_tabs():
        out = {}
        for tb in ("내 대시보드", "모든 대시보드"):
            pg.get_by_role("tab", name=tb).click(); pg.wait_for_timeout(1500); out[tb] = [r[:60] for r in rows(pg)]
        vshot(pg, "14-dashboards-all")
        star = pg.locator("tbody tr").first.locator("button").first
        star.click(); pg.wait_for_timeout(1200); out["bookmark toggle toast"] = toast(pg)[:2]
        star.click(); pg.wait_for_timeout(1200)
        return out
    step("7 dashboards tabs", dash_tabs)

    # ---------- 8. 일괄 편집 ----------
    go(pg, "/campaigns", 2500)
    def bulk():
        box = pg.locator("tbody tr").first.locator("button[role=checkbox]").first
        if not box.count(): box = pg.locator("tbody tr").first.locator("[role=checkbox]").first
        box.click(); pg.wait_for_timeout(600)
        pg.get_by_role("button", name=re.compile("^작업")).click(); pg.wait_for_timeout(600)
        items = pg.get_by_role("menuitem").all_inner_texts()
        pg.get_by_role("menuitem", name=re.compile("일괄 편집")).click(); pg.wait_for_timeout(1500); vshot(pg, "15-bulk-edit", True)
        d = D(pg); out = {"menu": items, "text": d.inner_text()[:800].replace("\n"," | "), "labels": d.locator("label").all_inner_texts(), "buttons": d.get_by_role("button").all_inner_texts()}
        pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        return out
    step("8 bulk edit", bulk)
    def colpick():
        pg.get_by_role("button", name=re.compile("열 선택")).click(); pg.wait_for_timeout(600)
        items = [x for x in pg.locator("[role=menuitemcheckbox]").all_inner_texts()]
        if not items: items = pg.locator("[data-radix-popper-content-wrapper]").inner_text().split("\n")
        vshot(pg, "16-columns"); pg.keyboard.press("Escape"); return items
    step("8 column picker", colpick)

    # ---------- 9. 알림 기준값 / 팀 이력 / 약관 / 가입 ----------
    go(pg, "/alerts", 2000); step("9 alerts", lambda: {"headers": pg.locator("thead th").all_inner_texts(), "rows": rows(pg)[:3]}); vshot(pg, "17-alerts")
    go(pg, "/org/users", 2500)
    def hist():
        pg.get_by_text("팀 이력").first.scroll_into_view_if_needed(); pg.wait_for_timeout(800); vshot(pg, "18-team-history", True)
        tbls = pg.locator("main table"); last = tbls.nth(tbls.count()-1)
        return {"headers": last.locator("thead th").all_inner_texts(), "rows": [r[:120].replace("\n"," ") for r in last.locator("tbody tr").all_inner_texts()[:5]], "pager": main_text(pg, 3000)[-300:]}
    step("9 team history", hist)
    go(pg, "/terms?lang=ko", 1500); vshot(pg, "19-terms"); step("9 terms", lambda: pg.locator("body").inner_text()[:300].replace("\n"," | "))
    go(pg, "/privacy?lang=ko", 1500); step("9 privacy sections", lambda: pg.locator("h2,h3").all_inner_texts()[:20])
    go(pg, "/signup", 2000); vshot(pg, "20-signup"); step("9 signup", lambda: {"text": pg.locator("main, body").first.inner_text()[:600].replace("\n"," | "), "labels": pg.locator("label").all_inner_texts()})
    # 홈 대시보드 고정 기간 표시
    go(pg, "/", 2500)
    step("9 home range area", lambda: {"buttons": [b.get_attribute("aria-label") or b.inner_text().strip() for b in pg.locator("main button").all()][:15], "flag": pg.locator("main").inner_text()[:400].replace("\n"," | ")})
    vshot(pg, "21-home-fixed-period")
    print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
run(t)
