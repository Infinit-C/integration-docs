#!/usr/bin/env python3
"""데모 조직(Guide Organization)에 덱 캡처용 데이터를 심는다.

사용법: python seed_demo.py channel | alerts
- channel: 이메일 알림 채널 그룹 하나 (알림 규칙 저장에 채널이 필요)
- alerts : 중요도별 알림 규칙 3개 (긴급·주의·참고). 기간 데이터가 없으면 '데이터 없음'으로만 기록되고 알림은 가지 않는다.
영어 UI 기준 라벨로 입력하므로 시작할 때 영어로 바꾸고 끝나면 되돌린다.
"""
import re
import sys

from playwright.sync_api import sync_playwright

from capture import BASE, _context
from deck_shots import _set_language

CHANNEL_GROUP = "운영 알림 (이메일)"
CHANNEL_EMAIL = "jh.yoon@infinit-c.com"

# (이름, 캠페인 그룹, 지표, 조건, 기준값, 중요도)
ALERTS = [
    ("노출 수 하한 알림", "브랜드B", "Impressions", "is below", "1000", "Warning"),
    ("미디어 비용 상한 알림", "브랜드B", "Media cost", "is above or equal to", "500000", "Critical"),
    ("CPM 참고 알림", "브랜드A", "CPM", "is above", "10000", "Info"),
]


def _select(page, label, value):
    el = page.get_by_label(label, exact=False).first
    if el.evaluate("e=>e.tagName") == "SELECT":
        el.select_option(label=value)
    else:
        el.click()
        page.get_by_role("option", name=value).first.click()
    page.wait_for_timeout(400)


def channel(page):
    page.goto(BASE + "/communication-groups", wait_until="networkidle")
    page.wait_for_timeout(1500)
    if page.locator("tr", has_text=CHANNEL_GROUP).count():
        print("채널 그룹 이미 있음"); return
    page.get_by_role("button", name=re.compile("Add communication group|알림 채널 그룹 추가")).first.click()
    page.wait_for_timeout(1000)
    d = page.get_by_role("dialog").first
    d.locator("select").first.select_option(index=0)  # Email
    d.locator("input[name='name']").fill(CHANNEL_GROUP)
    d.locator("input[type='email']").fill(CHANNEL_EMAIL)
    d.get_by_role("button").filter(has_text=re.compile("Add|추가")).last.click()
    page.wait_for_timeout(2500)
    print("채널 그룹:", page.inner_text("main")[-200:].replace("\n", " | "))


def alerts(page):
    for name, group, metric, cond, threshold, severity in ALERTS:
        page.goto(BASE + "/alerts/new", wait_until="networkidle")
        page.wait_for_timeout(2000)
        _select(page, "Campaign group", group)
        _select(page, "Query source", metric)
        _select(page, "Condition", cond)
        th = page.get_by_label("Threshold").first
        th.click(); th.fill(threshold)
        page.get_by_label("Alert name").first.fill(name)
        _select(page, "Severity", severity)
        boxes = page.get_by_role("checkbox")
        for i in range(boxes.count()):
            if boxes.nth(i).get_attribute("aria-checked") != "true":
                boxes.nth(i).click()
        page.get_by_role("button", name="Create alert").click()
        page.wait_for_timeout(3000)
        ok = "/alerts/new" not in page.url
        errs = page.locator("[role=alert], .text-destructive, [aria-invalid=true]").all_inner_texts()
        print(("✓" if ok else "✗"), name, "->", page.url, "" if ok else errs)
        if not ok:
            page.screenshot(path="out/seed-alert-fail.png", full_page=True)
            break


if __name__ == "__main__":
    step = {"channel": channel, "alerts": alerts}[sys.argv[1]]
    with sync_playwright() as p:
        ctx, page = None, None
        ctx = _context(p, headed=False)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(BASE, wait_until="networkidle")
        prev = _set_language(page, "en")
        step(page)
        if prev:
            _set_language(page, prev)
        ctx.close()
