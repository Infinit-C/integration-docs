---
sidebar_position: 5
title: 대시보드와 시각화
---

# 대시보드와 시각화

로그인하면 열리는 홈 화면이 **대시보드**입니다. 원하는 지표 차트(시각화)를
만들어 대시보드에 배치해 두면, 여러 캠페인의 현황을 한 화면에서 볼 수
있습니다. 대시보드는 조직 전체가 공유하므로 팀이 같은 화면을 보게 됩니다.

![대시보드](/img/claire/dashboard.png)

## 대시보드 다루기

- 사이드바 **Overview → Dashboard**를 누르면 내 기본 대시보드가 열립니다.
  조직에서 처음 만든 대시보드가 **Organization default**가 되고, 목록에서 다른
  대시보드의 [Set as default]를 누르면 나만의 기본 대시보드로 바뀝니다.
- [All dashboards]에서 조직의 대시보드 목록을 보고, [New dashboard]로 새
  대시보드를 만듭니다 (이름 필수, 설명 선택). 목록의 별 아이콘으로 자주
  보는 대시보드를 북마크할 수 있습니다.
- [Customize]를 누르면 편집 모드가 됩니다. [Add widget]으로 만들어 둔
  시각화를 검색해 올리고, 손잡이를 끌어 위치를 옮기거나 우하단 모서리로
  크기를 조절한 뒤 [Save layout]으로 저장합니다. 위젯은 별도 확인 없이 바로
  삭제되니 주의하세요.
- 대시보드 자체는 삭제할 수 없고 위젯만 뺄 수 있습니다. 레이아웃 편집은
  데스크톱 폭에서만 가능하며, 좁은 화면에서는 위젯이 세로로 쌓여 보기만 됩니다.

![대시보드 목록](/img/claire/dashboards-list.png)

## 시각화 만들기

**Overview → Visualizations**에서 [New visualization]을 누르면 왼쪽에 미리보기,
오른쪽에 설정 패널이 있는 편집기가 열립니다. 설정을 바꾼 뒤 [Update]로
미리보기를 갱신하고 [Create visualization]으로 저장합니다.

![시각화 편집기](/img/claire/visualization-editor.png)

**Data 탭**에서 정하는 것들:

| 항목 | 설명 |
|---|---|
| **Visualization type** | Date histogram(시계열) · Pie · Heat map · Gauge · Metric(단일 숫자) |
| **Metrics** | 기본 지표(Raw metric) 또는 공식(Formula)을 고릅니다. 최대 2개, Gauge·Metric은 1개 |
| **Buckets** | X-axis(날짜/시간 또는 지표)와 Split series(Platform · Campaign group · Campaign 중 하나)로 시리즈를 나눕니다 |
| **Minimum interval** | 시계열의 최소 집계 단위 (`auto`, `1h`, `1d`, `1w`, `1M` 등). auto는 기간에 맞춰 자동 선택 |
| **Filter** | 어떤 캠페인을 집계할지 조건식으로 좁힙니다 (아래 참고) |

Metric 유형에서는 [Add comparison]으로 **직전 같은 길이 구간과의 변화율**을
함께 표시할 수 있습니다. **Metrics & axes 탭**은 단위 표기(`KRW {VALUE}`
처럼 `{VALUE}` 포함), 합계/평균/최신값 집계, 차트 모양(area·bar·line, 누적,
백분율)을, **Panel settings 탭**은 범례·툴팁·색상 팔레트·임계선을 정합니다.

미리보기 상단의 기간 선택은 **Last 24 hours · 1 week · 1 month · 3 months**
네 가지이며 기본은 최근 1개월입니다. 편집 중인 설정은 주소(URL)에 담기므로
링크를 복사해 동료에게 그대로 보여줄 수 있습니다.

### 필터 조건식

Filter 칸에는 검색어 형태의 조건식을 씁니다. 입력 중에 필드와 값이 자동
완성됩니다.

```
platform: meta AND campaign.status: enabled
campaign_group.name: "브랜드A" AND NOT campaign.code: C-001
campaign.budget.daily >= 100000
```

쓸 수 있는 필드는 `platform`, `campaign_group.code` / `.name`,
`campaign.code` / `.name` / `.status`, `campaign.budget.daily` / `.total`,
`campaign.period.start` / `.end`이고, 연산자는 `:`(같음), `: *`(값 있음),
`>` `>=` `<` `<=`, `AND` `OR` `NOT`, 괄호입니다.

:::tip
시각화는 만든 사람 또는 조직 관리자만 수정할 수 있습니다. 목록의 톱니 아이콘으로
제목과 설정을 고칩니다. 화면에서 삭제하는 기능은 아직 없습니다.
:::
