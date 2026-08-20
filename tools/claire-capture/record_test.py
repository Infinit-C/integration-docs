#!/usr/bin/env python3
"""영상 테스트 v2: 부드러운 마우스 이동 + 한글 자막 오버레이.

시나리오: Overview → Campaign Groups → 그룹 상세(Campaigns 탭) → 캠페인 상세
→ Trends 탭 → Claire Chat 열고 질문 입력(전송 안 함).
출력: out/claire-flow.webm
"""
import math
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from capture import BASE, PROFILE, SENSITIVE, BLUR_JS

HERE = Path(__file__).parent
OUT = HERE / "out"

# 정적 캡처와 달리 영상은 로딩 타이밍을 못 맞추므로,
# MutationObserver로 새로 렌더되는 텍스트까지 계속 블러한다.
AUTO_BLUR_JS = """
(words) => {
  const blurEl = (el) => { el.style.filter = 'blur(7px)'; };
  const hit = (t) => words.some((w) => t.includes(w));
  const scan = (root) => {
    if (root.nodeType === 3) {
      if (hit(root.textContent || '') && root.parentElement) blurEl(root.parentElement);
      return;
    }
    if (root.nodeType !== 1) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = walker.nextNode())) {
      if (hit(n.textContent || '') && n.parentElement) blurEl(n.parentElement);
    }
    root.querySelectorAll && root.querySelectorAll('*').forEach((el) => {
      if (el.children.length === 0 && (el.textContent || '').trim() === 'JY') blurEl(el);
    });
  };
  scan(document.body);
  if (!window.__blurObs) {
    window.__blurObs = new MutationObserver((muts) => {
      for (const m of muts) {
        m.addedNodes && m.addedNodes.forEach(scan);
        if (m.type === 'characterData' && m.target.parentElement &&
            hit(m.target.textContent || '')) blurEl(m.target.parentElement);
      }
    });
    window.__blurObs.observe(document.body,
      {childList: true, subtree: true, characterData: true});
  }
}
"""

CURSOR_JS = """
() => {
  if (document.getElementById('__cursor')) return;
  const c = document.createElement('div');
  c.id = '__cursor';
  Object.assign(c.style, {
    position: 'fixed', zIndex: 999999, width: '20px', height: '20px',
    borderRadius: '50%', background: 'rgba(255,0,130,.4)',
    border: '2px solid rgba(255,0,130,.9)', pointerEvents: 'none',
    transform: 'translate(-50%,-50%)',
    boxShadow: '0 0 12px rgba(255,0,130,.35)',
    left: '-50px', top: '-50px',
  });
  document.body.appendChild(c);
  window.addEventListener('mousemove', (e) => {
    c.style.left = e.clientX + 'px';
    c.style.top = e.clientY + 'px';
  }, true);
  window.addEventListener('mousedown', () => {
    c.style.transform = 'translate(-50%,-50%) scale(.75)';
    c.style.background = 'rgba(255,0,130,.85)';
  }, true);
  window.addEventListener('mouseup', () => {
    c.style.transform = 'translate(-50%,-50%) scale(1)';
    c.style.background = 'rgba(255,0,130,.4)';
  }, true);
}
"""

CAPTION_JS = """
(text) => {
  let bar = document.getElementById('__caption');
  if (!bar) {
    bar = document.createElement('div');
    bar.id = '__caption';
    Object.assign(bar.style, {
      position: 'fixed', zIndex: 999998, left: '50%', bottom: '36px',
      transform: 'translateX(-50%)', maxWidth: '72%',
      padding: '12px 22px', borderRadius: '12px',
      background: 'rgba(11,11,16,.82)', color: '#fff',
      fontSize: '19px', fontWeight: '600', letterSpacing: '-0.01em',
      fontFamily: "'Pretendard Variable', Pretendard, 'Apple SD Gothic Neo', sans-serif",
      textAlign: 'center', pointerEvents: 'none',
      transition: 'opacity .3s', opacity: '0',
      boxShadow: '0 8px 30px rgba(0,0,0,.35)',
    });
    document.body.appendChild(bar);
  }
  if (!text) { bar.style.opacity = '0'; return; }
  bar.textContent = text;
  bar.style.opacity = '1';
}
"""


class Recorder:
    def __init__(self, page):
        self.page = page
        self.pos = (60.0, 60.0)

    def prep(self, wait=1800):
        """화면 전환 직후: 블러 + 커서 + 자막 레이어 재주입."""
        self.page.wait_for_timeout(wait)
        self.page.evaluate(AUTO_BLUR_JS, SENSITIVE)
        self.page.evaluate(CURSOR_JS)
        self.page.evaluate(CAPTION_JS, None)

    def caption(self, text, hold=1200):
        self.page.evaluate(CAPTION_JS, text)
        self.page.wait_for_timeout(hold)

    def move_to(self, x, y, duration_ms=650):
        """ease-in-out 곡선으로 부드럽게 이동."""
        x0, y0 = self.pos
        steps = max(12, int(duration_ms / 16))
        for i in range(1, steps + 1):
            t = i / steps
            e = 0.5 - 0.5 * math.cos(math.pi * t)  # ease-in-out
            # 살짝 호를 그리는 경로
            arc = math.sin(math.pi * t) * min(40, abs(x - x0) * 0.08)
            self.page.mouse.move(x0 + (x - x0) * e, y0 + (y - y0) * e - arc)
            self.page.wait_for_timeout(max(8, duration_ms // steps))
        self.pos = (x, y)

    def click(self, locator, settle=500):
        box = locator.bounding_box()
        if not box:
            locator.scroll_into_view_if_needed()
            self.page.wait_for_timeout(400)
            box = locator.bounding_box()
        cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
        self.move_to(cx, cy)
        self.page.wait_for_timeout(250)
        self.page.mouse.down()
        self.page.wait_for_timeout(90)
        self.page.mouse.up()
        self.page.wait_for_timeout(settle)


def main():
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=True,
            viewport={"width": 1440, "height": 900},
            record_video_dir=str(OUT),
            record_video_size={"width": 1440, "height": 900},
            locale="ko-KR",
            timezone_id="Asia/Seoul",
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        r = Recorder(page)

        # 1. Overview
        page.goto(BASE + "/", wait_until="networkidle")
        r.prep()
        r.caption("Claire에 로그인하면 Overview가 열립니다", 2000)

        # 2. Campaign Groups
        r.caption("캠페인 그룹 목록으로 이동합니다", 800)
        r.click(page.get_by_role("link", name="Browse campaignGroups"))
        r.prep(1500)
        r.caption("연결된 광고주(캠페인 그룹) 목록입니다", 2000)

        # 3. 그룹 상세 → Campaigns 탭
        r.click(page.get_by_role("link", name="View details").first)
        r.prep(1500)
        r.caption("그룹 상세 — Campaigns 탭에서 매체와 캠페인을 연결합니다", 900)
        r.click(page.get_by_role("tab", name="Campaigns"))
        r.prep(1200)
        page.wait_for_timeout(1400)

        # 4. 캠페인 상세 → Trends 탭
        r.caption("캠페인 상세로 들어가 성과를 확인합니다", 900)
        r.click(page.get_by_role("link", name="View details").first)
        r.prep(1500)
        r.click(page.get_by_role("tab", name="Trends"))
        r.prep(1000)
        r.caption("Trends 탭 — 수집된 성과 추이가 표시됩니다", 1800)

        # 5. Claire Chat
        r.caption("우하단 버튼으로 Claire에게 바로 질문할 수 있습니다", 900)
        r.click(page.get_by_role("button", name="Open chat"))
        page.wait_for_timeout(1800)
        page.evaluate(AUTO_BLUR_JS, SENSITIVE)
        box = page.get_by_placeholder("메시지를 입력하세요")
        bb = box.bounding_box()
        r.move_to(bb["x"] + 60, bb["y"] + bb["height"] / 2)
        page.mouse.down(); page.wait_for_timeout(80); page.mouse.up()
        page.wait_for_timeout(300)
        box.press_sequentially("이 캠페인 최근 성과를 요약해줘", delay=75)
        r.caption("캠페인 데이터를 아는 Claire가 바로 답합니다", 2400)
        page.evaluate(CAPTION_JS, None)
        page.wait_for_timeout(700)

        video = page.video
        ctx.close()
        path = video.path()
        final = OUT / "claire-flow.webm"
        final.unlink(missing_ok=True)
        Path(path).rename(final)
        print(f"saved: {final}")


if __name__ == "__main__":
    main()
