import re, sys, json
sys.path.insert(0, "/Users/yoonjaehyon/dev/integration-docs/tools/claire-capture/regress")
import wt
from wt import run, toast, main_text
from capture import BASE
wt.OUT = "out/explore7"; R = {}; CAMP = "83901859"; created = {}

def main(pg):
    pg.on("response", lambda r: created.update(r.json().get("data", {})) if r.request.method == "POST" and r.url.endswith("/report-shares") and r.status == 201 else None)
    pg.goto(BASE + f"/campaigns/{CAMP}", wait_until="networkidle"); pg.wait_for_timeout(1500)
    pg.locator("main button, main a").filter(has_text=re.compile("보고서 링크")).first.click(); pg.wait_for_timeout(1200)
    d = pg.locator("[role=dialog]").first
    # 기존 AUDIT-TEST 사용 중 링크 먼저 끊기 (alertdialog 디버그)
    for li in d.locator("li", has_text="AUDIT-TEST").all():
        if "사용 중" not in li.inner_text(): continue
        li.get_by_role("button", name=re.compile("링크 끊기")).click(); pg.wait_for_timeout(800)
        ad = pg.locator("[role=dialog]", has_text="이 링크를 끊을까요")
        R.setdefault("revoke_dialogs", []).append((ad.count(), ad.last.inner_text()[:200].replace("\n"," | ") if ad.count() else None, ad.last.get_by_role("button").all_inner_texts() if ad.count() else None))
        if ad.count(): ad.last.get_by_role("button").filter(has_text=re.compile("끊기")).last.click(); pg.wait_for_timeout(2000)
        R["revoke_toast"] = toast(pg)
    d.get_by_label(re.compile("소재 성과"), exact=False).first.check(); pg.wait_for_timeout(300)
    d.get_by_placeholder(re.compile("월간 성과")).fill("AUDIT-TEST 소재 포함 링크")
    sw = d.get_by_label(re.compile("AI 채팅"), exact=False)
    if sw.count() and sw.first.get_attribute("aria-checked") != "true": sw.first.click()
    # 기간 지정 7~8월
    d.get_by_role("combobox").filter(has_text=re.compile("최근 7일")).click(); pg.wait_for_timeout(300)
    pg.get_by_role("option", name=re.compile("기간 지정")).click(); pg.wait_for_timeout(500)
    dates = d.locator("input[type=date]")
    if dates.count() >= 2: dates.nth(0).fill("2026-07-01"); dates.nth(1).fill("2026-08-31")
    d.get_by_role("button", name=re.compile("^링크 만들기")).click(); pg.wait_for_timeout(2500)
    R["create_toast"] = toast(pg); R["created"] = {k: str(v)[:40] for k, v in created.items()}
    url = BASE + "/share/" + created["token"] if "token" in created else None
    R["dialog_after"] = d.inner_text()[-500:].replace("\n"," | ")
    pg.keyboard.press("Escape")
    if url:
        p2 = pg.context.new_page(); p2.goto(url, wait_until="networkidle"); p2.wait_for_timeout(3000)
        R["title"] = p2.title()
        t2 = p2.locator("body").inner_text(); R["page_text"] = t2.replace("\n"," | ")[:3500]
        R["ads_section"] = t2[t2.find("소재"):][:400].replace("\n"," | ") if "소재" in t2 else None
        R["lines_bars"] = (p2.locator(".recharts-line").count(), p2.locator(".recharts-bar").count())
        p2.screenshot(path=f"{wt.OUT}/share-page.png", full_page=True)
        qb = p2.get_by_role("button", name=re.compile("질문하기"))
        if qb.count():
            qb.first.click(); p2.wait_for_timeout(800)
            R["chat_box"] = p2.locator("body").inner_text().split("질문하기")[-1][:300].replace("\n"," | ")
            p2.get_by_placeholder(re.compile("질문")).fill("이 기간 CTR 합계는 얼마야?"); p2.keyboard.press("Enter")
            for _ in range(40):
                p2.wait_for_timeout(1000)
                bt = p2.locator("body").inner_text()
                if "%" in bt.split("CTR 합계는 얼마야?")[-1]: break
            R["ai_answer"] = p2.locator("body").inner_text().split("CTR 합계는 얼마야?")[-1][:700].replace("\n"," | ")
            p2.screenshot(path=f"{wt.OUT}/share-page-ai.png", full_page=True)
        p2.close()
    # 끊기
    pg.goto(BASE + f"/campaigns/{CAMP}", wait_until="networkidle"); pg.wait_for_timeout(1500)
    pg.locator("main button, main a").filter(has_text=re.compile("보고서 링크")).first.click(); pg.wait_for_timeout(1200)
    d = pg.locator("[role=dialog]").first
    li = d.locator("li", has_text="AUDIT-TEST 소재 포함 링크").first
    li.get_by_role("button", name=re.compile("링크 끊기")).click(); pg.wait_for_timeout(800)
    ad = pg.locator("[role=dialog]", has_text="이 링크를 끊을까요")
    R["revoke_dialog2"] = (ad.count(), ad.last.get_by_role("button").all_inner_texts() if ad.count() else None)
    if ad.count(): ad.last.get_by_role("button").filter(has_text=re.compile("끊기")).last.click(); pg.wait_for_timeout(2000)
    R["revoke_toast2"] = toast(pg)
    R["active_audit_left"] = [x[:80] for x in d.locator("li", has_text="AUDIT-TEST").all_inner_texts() if "사용 중" in x]
    if url:
        p3 = pg.context.new_page(); p3.goto(url, wait_until="networkidle"); p3.wait_for_timeout(1500); R["revoked_page"] = p3.locator("body").inner_text()[:150].replace("\n"," | "); p3.close()
try: run(main)
finally:
    json.dump(R, open(f"{wt.OUT}/result-b.json","w"), ensure_ascii=False, indent=1)
    for k, v in R.items(): print(k, "=>", str(v)[:900])
