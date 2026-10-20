#!/usr/bin/env python3
"""관리자 계정으로 덱 캡처 1·2번을 한 번의 헤드 브라우저 세션으로 처리한다.
(ops/DECK_SCREENSHOT_PROMPT_20261021_KO.md 10/19판)

사용법: CLAIRE_PROFILE=.profile-admin python admin_shots.py [cleanup]
- 창을 띄우고 사용자가 로그인할 때까지 기다린다. 작업이 끝날 때까지 창을 닫지 않는다.
- 알림 채널 그룹 "운영 알림 (이메일)"(수신 jh.yoon@infinit-c.com)만 써서 알림 3개(긴급·주의·참고)를 만든 뒤
  목록을 캡처하고 3개를 끈다. 사용자 목록도 캡처한다.
- 폼 입력은 영어 UI, 캡처는 한국어 UI로 하고 끝나면 원래 언어로 돌린다.
- cleanup: 만든 알림 3개와 이메일 채널 그룹을 지운다 (덱 작업이 끝난 뒤).
"""
import re
import sys

from playwright.sync_api import sync_playwright

from capture import BASE, PROFILE
from deck_shots import OUT, _set_language, shot_alerts, shot_chat, shot_summary, shot_users

MANUAL = 10 * 60 * 1000
CHANNEL_GROUP = "운영 알림 (이메일)"
CHANNEL_EMAIL = "jh.yoon@infinit-c.com"
# 10/19 확인: 관리자 조직의 DV360 캠페인은 전부 테스트용이고 그룹이 없다. 데이터가 있는 DV360 캠페인은 서정욱 조직(453382227500)의
# GUGUS YT Search On 뿐이라 그 조직에 이메일 채널 그룹을 API로 만들고(화면엔 조직 전환이 없음) 거기에 알림을 건다.
TARGET_ORG = "453382227500"
CAMPAIGN, GROUP = "GUGUS YT Search On", "GUGUS"
# (이름, 지표, 조건, 기준값, 중요도) — GUGUS에는 CTR 공식이 없어 Impressions로 대체. Maximum CPM은 KPI 목표 소스라 조건이 자동
ALERTS = [
    ("미디어 비용 상한 알림", "Media cost", "is above or equal to", "500000", "Critical"),
    ("CPM 목표 초과 알림", "Maximum CPM", None, None, "Warning"),
    ("노출 수 참고 알림", "Impressions", "is below", "1000", "Info"),
]


def wait_login(page):
    page.goto(BASE, wait_until="networkidle")
    if "/login" in page.url:
        print(">> 브라우저에서 관리자 계정으로 로그인해 주세요 (창은 닫지 않습니다)")
        page.wait_for_selector("a[href='/campaigns'], a[href^='/dashboards']", timeout=MANUAL)
        page.wait_for_timeout(1500)
    print("로그인 확인:", page.url)


def _combo(page, id_):
    return page.locator(f"[role=combobox][id='{id_}']").first


def _pick(page, id_, label):
    """Radix 셀렉트(버튼 + 팝업 listbox)에서 label 항목을 고른다."""
    _combo(page, id_).click()
    page.get_by_role("option", name=label, exact=True).first.click()
    page.wait_for_timeout(400)


def _campaign_combo_id(page):
    ids = page.locator("[role=combobox]").evaluate_all("els=>els.map(e=>e.id)")
    return next((i for i in ids if i.lower().startswith("targetcampaign") and i != "targetCampaignGroup"), None)


def _api(page, method, path, body=None):
    """프론트가 쓰는 Bearer 토큰(localStorage claire.authentication)으로 API를 호출한다."""
    auth = page.evaluate("JSON.parse(localStorage.getItem('claire.authentication')||'{}')")
    token = next((v for k, v in auth.items() if "access" in k.lower() and isinstance(v, str)), None) or auth.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    if body is not None:
        headers["Content-Type"] = "application/json"  # DELETE는 본문 없이 (JSON 헤더만 있으면 400)
    res = page.request.fetch(BASE + "/api" + path, method=method, data=body, headers=headers)
    try:
        return res.status, res.json()
    except Exception:
        return res.status, res.text()


def _groups(page, org_code):
    path = f'/channel-groups?filters=[{{"c":"orgCode","v":"{org_code}"}}]&page=0&size=100' if org_code else "/channel-groups?page=0&size=100"
    st, body = _api(page, "GET", path)
    return [g for g in ((body.get("data") or []) if isinstance(body, dict) else [])
            if g.get("name") == CHANNEL_GROUP and not g.get("deleted")]


def ensure_channel_api(page, org_code):
    """org_code 조직에 '운영 알림 (이메일)' 그룹이 없으면 API로 만든다. 그룹 code를 돌려준다."""
    found = _groups(page, org_code)
    if found:
        print("채널 그룹 있음:", found[0]["code"]); return found[0]["code"]
    st, body = _api(page, "POST", "/channel-groups",
                    {"orgCode": org_code, "type": "email", "email": CHANNEL_EMAIL, "name": CHANNEL_GROUP})
    code = (body.get("data") or {}).get("code") if isinstance(body, dict) else None
    print("채널 그룹 생성:", st, code or body)
    return code


def create_alerts(page, campaign, group):
    made = []
    for name, metric, cond, threshold, severity in ALERTS:
        page.goto(BASE + "/alerts/new", wait_until="networkidle")
        page.wait_for_timeout(1500)
        _pick(page, "targetCampaignGroup", group)
        _pick(page, "targetScope", "Campaign"); page.wait_for_timeout(800)
        _pick(page, _campaign_combo_id(page), campaign); page.wait_for_timeout(1200)
        _pick(page, "querySource-0", metric); page.wait_for_timeout(800)
        if cond:
            _pick(page, "conditions.0.comparisonOperator", cond)
            th = page.locator("[id='conditions.0.thresholdValue']"); th.click(); th.fill(threshold)
        page.locator("input#name").fill(name)
        _pick(page, "severity", severity)
        # 채널: 지정한 그룹만 체크 (다른 사람 채널은 절대 고르지 않는다)
        lab = page.locator("label", has_text=CHANNEL_GROUP)
        if not lab.count():
            print("✗ 채널 목록에", CHANNEL_GROUP, "없음 — 중단"); page.screenshot(path=str(OUT / "fail-channel.png"), full_page=True); break
        lab.first.click()
        page.wait_for_timeout(300)
        page.get_by_role("button", name="Create alert").click()
        page.wait_for_timeout(3000)
        ok = "/alerts/new" not in page.url
        print(("✓" if ok else "✗"), name, "->", page.url)
        if not ok:
            page.screenshot(path=str(OUT / f"fail-{metric}.png"), full_page=True)
            print("   errors:", page.locator("[aria-invalid=true], [role=alert]").all_inner_texts())
            continue
        made.append(name)
    return made


def _row_action(page, name, want_re):
    row = page.locator("tbody tr", has_text=name)
    if not row.count():
        print("  행 없음:", name); return False
    row.first.get_by_role("button").last.click(); page.wait_for_timeout(600)
    item = page.get_by_role("menuitem", name=re.compile(want_re))
    if not item.count():
        print("  메뉴 없음:", name, page.get_by_role("menuitem").all_inner_texts()); page.keyboard.press("Escape"); return False
    item.first.click(); page.wait_for_timeout(2000)
    return True


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE, headless=False, viewport={"width": 1600, "height": 1180},
            device_scale_factor=2, locale="ko-KR", timezone_id="Asia/Seoul")
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.on("dialog", lambda d: d.accept())
        wait_login(page)
        prev = _set_language(page, "en")
        ensure_channel_api(page, TARGET_ORG)
        made = create_alerts(page, CAMPAIGN, GROUP)
        _set_language(page, "ko")
        print("alerts:", shot_alerts(page) or "OK")
        page.goto(BASE + "/alerts", wait_until="networkidle"); page.wait_for_timeout(1500)
        for n in made:
            print("  끔:", n, _row_action(page, n, "^(끄기|Disable)"))
        print("users:", shot_users(page) or "OK")
        if prev:
            _set_language(page, prev)
        ctx.close()
    print("\n저장:", OUT, "| 만든 알림(꺼 둠):", made)


def cleanup():
    """덱 작업이 끝난 뒤: 만든 알림 3개와 이메일 채널 그룹(서정욱 조직·관리자 조직)을 API로 지운다.
    (목록 행 메뉴에는 확인 기록·수정만 있어 화면에서는 못 지운다.)"""
    names = {n for n, *_ in ALERTS}
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(PROFILE, headless=False, viewport={"width": 1600, "height": 1180})
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        wait_login(page)
        st, body = _api(page, "GET", "/alerts?page=0&size=100")
        rows = (body.get("data") or []) if isinstance(body, dict) else []
        mine = [r for r in rows if r.get("name") in names and (r.get("campaign") or {}).get("name", CAMPAIGN) == CAMPAIGN]
        print(f"알림 목록 {st}: 전체 {len(rows)}개, 삭제 대상 {len(mine)}개")
        for r in mine:
            # 켜진 알림은 삭제가 409라서 먼저 끈다
            st0, _ = _api(page, "PATCH", f"/alerts/{r['code']}/enabled", {"enabled": False})
            st, _ = _api(page, "DELETE", f"/alerts/{r['code']}")
            print("  알림 끄기/삭제:", r["code"], r["name"], "->", st0, st)
        for org in (TARGET_ORG, None):
            for g in _groups(page, org):
                st, _ = _api(page, "DELETE", f"/channel-groups/{g['code']}")
                print("  채널 그룹 삭제:", g["code"], (g.get("org") or {}).get("name"), "->", st)
        st, body = _api(page, "GET", "/alerts?page=0&size=100")
        left = [r["name"] for r in ((body.get("data") or []) if isinstance(body, dict) else []) if r.get("name") in names]
        print("남은 알림:", left or "없음", "| 남은 그룹:", [g["code"] for o in (TARGET_ORG, None) for g in _groups(page, o)] or "없음")
        ctx.close()


def shots():
    """캡처만 다시 (쓰기 없음). 관리자 목록에는 다른 광고주 알림이 섞여 보이므로 이름을 더 가린다."""
    import deck_shots
    from capture import SENSITIVE
    SENSITIVE.extend(["정림", "현대건설", "Smart City", "Newkiki", "카카오모먼트 캠페인", "GUGUS", "Dorelan", "VVC", "ROAS 500%"])
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE, headless=False, viewport={"width": 1600, "height": 1180},
            device_scale_factor=2, locale="ko-KR", timezone_id="Asia/Seoul")
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        wait_login(page)
        prev = _set_language(page, "ko")
        print("alerts:", shot_alerts(page) or "OK")
        print("users:", shot_users(page) or "OK")
        if prev:
            _set_language(page, prev)
        ctx.close()


def shots2():
    """10/20 배포 후: 5번 맞춤 요약 편집기(저장 안 함) + 3번 채팅. 관리자 계정은 다른 조직 캠페인 채팅이 403이라 채팅은 실패할 수 있다."""
    from capture import SENSITIVE
    SENSITIVE.extend(["정림", "현대건설", "Smart City", "Newkiki", "카카오모먼트 캠페인", "GUGUS", "Dorelan", "VVC", "ROAS 500%"])
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE, headless=False, viewport={"width": 1600, "height": 1180},
            device_scale_factor=2, locale="ko-KR", timezone_id="Asia/Seoul")
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.on("response", lambda r: print(f"  [{r.status}] {r.request.method} {r.url.replace(BASE, '')[:100]} {r.text()[:300]}")
                if "/api/" in r.url and r.status >= 400 else None)
        wait_login(page)
        prev = _set_language(page, "ko")
        print("summary:", shot_summary(page, GROUP, CAMPAIGN) or "OK")
        if "chat" in sys.argv:
            print("chat:", shot_chat(page) or "OK")
        if prev:
            _set_language(page, prev)
        ctx.close()


if __name__ == "__main__":
    {"cleanup": cleanup, "shots": shots, "shots2": shots2}.get(sys.argv[1] if len(sys.argv) > 1 else "", main)()
