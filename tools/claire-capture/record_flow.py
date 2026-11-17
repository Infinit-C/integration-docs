#!/usr/bin/env python3
"""가이드 소개 영상(한국어 UI): 대시보드 → 플랫폼 연동(연결 위저드·관리) → 캠페인 그룹 → 그룹 상세(캠페인 탭) → 캠페인 상세 대시보드 → Claire 채팅.
출력: out/claire-flow.webm (record_test.py의 Recorder·블러·자막 재사용)"""
import re
from pathlib import Path
from playwright.sync_api import sync_playwright
from capture import BASE, PROFILE, SENSITIVE
from record_test import Recorder, AUTO_BLUR_JS, CAPTION_JS, OUT

def main():
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(PROFILE, headless=True, viewport={"width": 1440, "height": 900},
            record_video_dir=str(OUT), record_video_size={"width": 1440, "height": 900}, locale="ko-KR", timezone_id="Asia/Seoul")
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        r = Recorder(page)
        page.goto(BASE + "/", wait_until="networkidle"); r.prep(2500)
        r.caption("Claire에 로그인하면 대시보드가 열립니다", 2200)

        r.caption("먼저 설정 → 플랫폼 연동에서 매체를 연동합니다", 900)
        r.click(page.get_by_role("link", name="플랫폼 연동")); r.prep(1500); page.wait_for_timeout(600)
        r.caption("새 매체는 [연결] 버튼으로 연동합니다", 900)
        r.click(page.locator("main").get_by_role("link", name="연결").or_(page.locator("main").get_by_role("button", name="연결")).first); r.prep(1800)
        r.caption("플랫폼 선택 → 인증 → 계정 선택 → 캠페인 선택, 4단계 안내", 2600)
        r.click(page.locator("main").get_by_role("link", name="취소").or_(page.locator("main").get_by_role("button", name="취소")).first); r.prep(1500)
        r.caption("연동한 플랫폼에서 광고 계정과 캠페인을 불러옵니다", 900)
        r.click(page.locator("tbody tr").first.locator("button").last); page.wait_for_timeout(600)
        r.click(page.get_by_role("menuitem", name="관리")); r.prep(1500); page.wait_for_timeout(1500)

        r.caption("불러온 캠페인은 캠페인 그룹으로 묶어 관리합니다", 800)
        side_camp = page.locator("aside, nav").get_by_role("button", name="캠페인")
        if side_camp.count() and side_camp.first.get_attribute("aria-expanded") != "true": r.click(side_camp.first); page.wait_for_timeout(500)
        r.click(page.get_by_role("link", name="캠페인 그룹")); r.prep(1500)
        r.caption("연결된 광고주(캠페인 그룹) 목록입니다", 2000)
        r.click(page.locator("tbody tr", has_text="브랜드B").locator("a").first); r.prep(1800)
        r.caption("그룹 상세 — 캠페인 탭에 연동 계정에서 불러온 캠페인이 모입니다", 900)
        r.click(page.get_by_role("tab", name="캠페인", exact=True)); r.prep(1200); page.wait_for_timeout(1400)

        r.caption("캠페인 상세로 들어가 성과를 확인합니다", 900)
        r.click(page.locator("tbody tr", has_text="협력광고").locator("a").first); r.prep(2500)
        r.caption("대시보드 탭 — KPI 목표 대비 현황과 성과 추이가 표시됩니다", 1800)
        page.mouse.wheel(0, 300); page.wait_for_timeout(1200); page.mouse.wheel(0, -300); page.wait_for_timeout(600)

        r.caption("우하단 버튼으로 Claire에게 바로 질문할 수 있습니다", 900)
        r.click(page.get_by_role("button", name=re.compile("Open chat|채팅 열기"))); page.wait_for_timeout(1800)
        new_chat = page.get_by_role("button", name="새로운 채팅")
        if new_chat.count(): r.click(new_chat); page.wait_for_timeout(1500)
        page.evaluate(AUTO_BLUR_JS, SENSITIVE)
        box = page.get_by_placeholder("메시지를 입력하세요"); bb = box.bounding_box()
        r.move_to(bb["x"] + 60, bb["y"] + bb["height"] / 2); page.mouse.down(); page.wait_for_timeout(80); page.mouse.up(); page.wait_for_timeout(300)
        box.press_sequentially("이 캠페인 최근 성과를 요약해줘", delay=75)
        r.caption("캠페인 데이터를 아는 Claire가 바로 답합니다", 2400)
        page.evaluate(CAPTION_JS, None); page.wait_for_timeout(700)
        video = page.video; ctx.close(); path = video.path()
        final = OUT / "claire-flow.webm"; final.unlink(missing_ok=True); Path(path).rename(final); print(f"saved: {final}")

if __name__ == "__main__":
    main()
