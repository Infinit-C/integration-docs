---
sidebar_position: 8
title: 리포트 내려받기
---

# 리포트 내려받기

**Monitor → Reports**에서 캠페인 성과를 표 형태의 파일(CSV · XLSX)로
뽑습니다. 어떤 열(차원)과 지표를 어떤 기간·단위로 볼지를 정한 리포트 정의를 만들어
두고, 필요할 때 [Run report]로 실행해 파일을 내려받습니다.

![Reports](/img/claire/reports.png)

## 리포트 정의 만들기

[New]를 누르면 6단계 안내 화면이 열립니다.

1. **Definition** — 이름, 집계 단위(Breakdown: Cumulative · Monthly · Weekly ·
   Daily · Hourly), 열로 쓸 차원(Dimensions: 캠페인 그룹 이름/코드, 캠페인
   이름/코드/시작일/종료일, 플랫폼, 플랫폼 계정), 지표(기본 지표·공식)를
   고릅니다. 고른 순서가 열 순서입니다.
2. **Date** — 기간과 시간대. Yesterday · Last 7/30/60/90 days · Last week ·
   Last month · Month/Quarter/Year to date 같은 상대 기간 또는 Custom(직접 지정).
3. **Filters** — 캠페인 그룹 · 캠페인 · 플랫폼별로 포함(Include)/제외(Exclude)
   조건을 겁니다. 비워 두면 전체 데이터입니다.
4. **Delivery** — 수신 이메일을 고릅니다 (이메일 채널로 등록된 주소 중 선택).
5. **Output** — CSV · XLSX · Styled XLSX(서식 적용 엑셀).
6. **Schedule** — 자동 실행 예약(One time · Daily · Weekly · Monthly, 분 단위는
   00 또는 30). 켜 두면 예정 실행 시각 5개가 미리 표시됩니다.

## 실행과 다운로드

목록의 **Report definitions** 탭에서 재생 아이콘 [Run report]를 누르면
**Generated reports** 탭으로 이동하고 실행이 큐에 들어갑니다(queued → running
→ completed). 완료되면 행의 다운로드 아이콘으로 파일을 받습니다. 파일명은
`리포트이름-실행시각` 뒤에 형식에 맞는 확장자(.csv 또는 .xlsx)가 붙습니다.

:::note
현재 버전에서는 실행 결과를 화면에서 내려받는 방식이 기준입니다. 예약 실행과
이메일 발송 설정은 저장되지만 아직 자동으로 동작하지 않으니, 정기 발송이
필요하면 [정기 요약 보내기](/claire/custom-summaries)를 이용하세요.
:::
