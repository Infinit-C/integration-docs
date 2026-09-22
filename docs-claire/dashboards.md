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

목록 상단 [Import JSON]으로 내보내 둔 대시보드 정의를 붙여 넣으면 새 대시보드와
그 안의 시각화가 함께 만들어집니다.

## 시각화 만들기

**Overview → Visualizations**에서 [New visualization]을 누르면 왼쪽에 미리보기,
오른쪽에 설정 패널이 있는 편집기가 열립니다. 설정을 바꾼 뒤 [Update visualization]으로
미리보기를 갱신하고 [Create visualization]으로 저장합니다.

![시각화 편집기](/img/claire/visualization-editor.png)

**Data 탭**에서 정하는 것들:

| 항목 | 설명 |
|---|---|
| **Visualization type** | Date histogram(시계열) · Pie · Heat map · Gauge · Metric(단일 숫자) · Table(표) |
| **Metrics** | 기본 지표(Raw metric) 또는 공식(Formula)을 고릅니다. 최대 2개, Gauge·Metric은 1개 |
| **Buckets** | X-axis(날짜/시간 또는 지표)와 Split series(Platform · Campaign group · Campaign 중 하나)로 시리즈를 나눕니다 |
| **Minimum interval** | 시계열의 최소 집계 단위 (`auto`, `1h`, `1d`, `1w`, `1M` 등). auto는 기간에 맞춰 자동 선택 |
| **Filter** | 어떤 캠페인을 집계할지 조건식으로 좁힙니다 (아래 참고) |

Table은 X축 값(날짜 또는 지표)을 행, 시리즈를 열로 펼친 표입니다. 행은
X축 값 오름차순으로 고정이고 열 구성이나 정렬을 따로 설정하는 항목은 없습니다.
조직 첫 화면의 Welcome Dashboard에 있는 안내 문구 위젯(Markdown)은 시스템이
넣는 것이라 직접 만들거나 편집할 수 없고, 대시보드 [Add widget] 목록에도
나오지 않습니다.

**Metrics & axes 탭**은 단위 표기(`KRW {VALUE}`처럼 `{VALUE}` 포함),
합계/평균/최신값 집계, 차트 모양(area·bar·line, 누적, 백분율)을,
**Panel settings 탭**은 범례·툴팁·색상 팔레트·임계선을 정합니다.

Metric 유형을 고르면 Metrics & axes 탭 맨 위에 **Display mode**가 나타납니다.

| Display mode | 결과 |
|---|---|
| **Normal** | 값 하나를 그대로 보여주는 기본 형태 |
| **Comparison card** | 현재 값과 비교 대상을 나란히 놓는 KPI 카드 |

Comparison card를 고르면 **Compare with**가 따라 나옵니다. **None**(비교 없음),
**Previous period**(직전 같은 길이 구간), **KPI target**(캠페인 KPI 목표) 중에서
고르며, KPI target은 [Select KPI target]으로 대상 목표를 지정합니다. Display
mode를 Normal로 되돌리면 설정해 둔 비교는 지워집니다.

**KPI target은 캠페인이 정해진 편집기에서만 고를 수 있습니다.** 캠페인·캠페인
그룹 대시보드에서 만든 시각화가 여기에 해당하고, Overview → Visualizations에서
새로 만드는 시각화처럼 대상 캠페인이 없으면 이 선택지가 잠깁니다. 캠페인이
정해져 있어도 고른 지표와 원천 지표가 같은 KPI 목표만 후보로 나옵니다.

미리보기 상단의 기간 선택은 **Last 24 hours · Last week · Last month ·
Last 3 months** 네 가지이며 기본은 최근 1개월입니다. 설정을 바꾼 뒤
[Update visualization]을 누르면 미리보기만 새로 그려지고, 저장은 아래쪽
[Create visualization] 또는 [Save changes]로 합니다. 편집 중인 설정은
주소(URL)에 담기므로 링크를 복사해 동료에게 그대로 보여줄 수 있습니다.

### 필터 조건식

Filter 검색창에 **검색할 항목과 조건**을 입력하면 원하는 데이터만 볼 수 있습니다. 입력 중에는 사용 가능한 필드와 값이 자동 완성됩니다.

```text
campaign.name: "가을 프로모션"
```

- `campaign.name`: 검색할 항목
- `:`: 일치 조건
- `"가을 프로모션"`: 찾을 값

#### 검색할 수 있는 항목

| 필드 | 설명 |
|---|---|
| `platform` | 플랫폼 |
| `campaign.code` | 캠페인 코드 |
| `campaign.name` | 캠페인 이름 |
| `campaign.status` | 캠페인 상태 |
| `campaign_group.code` | 캠페인 그룹 코드 |
| `campaign_group.name` | 캠페인 그룹 이름 |
| `campaign.budget.daily` | 캠페인 일일 예산 상한 |
| `campaign.budget.total` | 캠페인 총예산 |
| `campaign.period.start` | 캠페인 시작 시각 |
| `campaign.period.end` | 캠페인 종료 시각 |

#### 값 일치: `:`

입력한 값과 일치하는 항목을 찾습니다. 영문 대소문자는 구분하지 않으며, 값에 공백이 있으면 큰따옴표로 감싸주세요.

```text
campaign.code: 18597463
campaign.name: "가을 프로모션"
```

#### 일부 일치와 값 존재 여부: `*`

`*`는 임의의 문자열을 뜻합니다. 단독으로 사용하면 값이 존재하는 항목을 찾습니다.

| 조건 | 의미 |
|---|---|
| `campaign.name: 가을*` | 이름이 “가을”로 시작 |
| `campaign.name: *프로모션` | 이름이 “프로모션”으로 끝남 |
| `campaign.name: *할인*` | 이름에 “할인”이 포함됨 |
| `campaign_group.code: *` | 캠페인 그룹 코드가 존재함 |

#### 조건 조합: `AND`, `OR`, `NOT`

| 연산자 | 의미 |
|---|---|
| `AND` | 모든 조건을 만족 |
| `OR` | 하나 이상의 조건을 만족 |
| `NOT` | 해당 조건을 제외 |

다음은 Google Ads 캠페인 중 일일 예산 상한이 100,000 이상인 항목을 찾습니다.

```text
platform: google_ads AND campaign.budget.daily >= 100000
```

같은 필드의 여러 값은 괄호 안에서 `OR`로 연결할 수 있습니다. 아래 두 표현은 같은 의미입니다.

```text
campaign.name: "가을 행사" OR campaign.name: "겨울 행사"
campaign.name: ("가을 행사" OR "겨울 행사")
```

다음은 이름에 “테스트”가 들어간 캠페인을 제외합니다.

```text
NOT campaign.name: *테스트*
```

#### 조건 묶기: 괄호

괄호 안의 조건을 먼저 판단합니다. 괄호가 없으면 **NOT → AND → OR** 순서로 처리합니다.

다음은 이름에 “가을” 또는 “겨울”이 포함된 Google Ads 캠페인을 찾습니다.

```text
(campaign.name: *가을* OR campaign.name: *겨울*) AND platform: google_ads
```

#### 숫자와 날짜 비교

| 연산자 | 숫자 비교 | 날짜 비교 |
|---|---|---|
| `>` | 기준값보다 큼 | 기준 시각 이후, 기준 제외 |
| `>=` | 기준값 이상 | 기준 시각 이후, 기준 포함 |
| `<` | 기준값보다 작음 | 기준 시각 이전, 기준 제외 |
| `<=` | 기준값 이하 | 기준 시각 이전, 기준 포함 |

숫자에는 쉼표나 통화 기호를 넣지 않습니다.

```text
campaign.budget.total >= 1000000 AND campaign.budget.total < 5000000
```

날짜와 시간은 큰따옴표로 감싸고 시간대를 지정합니다. 다음은 한국 시간 기준 2026년 9월 1일 0시부터 시작하는 캠페인을 찾습니다.

```text
campaign.period.start >= "2026-09-01T00:00:00+09:00"
```

#### 입력 시 주의사항

- 여러 값은 쉼표가 아닌 `OR`로 연결합니다. `IN`은 지원하지 않습니다.
- 일치 조건은 `=` 대신 `:`, 제외 조건은 `!=` 대신 `NOT`을 사용합니다.
- `AND`, `OR`, `NOT`은 소문자로 입력해도 됩니다.
- 검색창을 비우면 추가 필터 조건이 해제됩니다.

### 시각화 목록과 수정 권한

**Overview → Visualizations** 목록은 이름 · **Available in** · **Type** ·
**Last updated** 열로 이뤄지며, 각 열 머리글을 눌러 정렬할 수 있습니다.

**Available in**은 이 시각화를 어디에 올릴 수 있는지를 나타냅니다.

- **All dashboards** — 아무 대시보드에나 [Add widget]으로 올릴 수 있습니다.
- **Campaign restricted** — KPI 목표에 묶인 시각화입니다. 이름 아래에 묶인
  캠페인 이름이 함께 표시됩니다.

직접 고르는 항목이 아니라 **Compare with에 KPI target을 지정했는지**에 따라
자동으로 정해집니다.

:::tip
차트 설정을 고치려면 목록에서 **시각화 이름을 클릭**해 편집기로 들어갑니다.
행의 [Edit]는 이름만 바꾸는 창입니다. 수정은 만든 사람 또는 조직 수정 권한이
있는 사람만 할 수 있고, 화면에서 삭제하는 기능은 아직 제공하지 않습니다.
행의 [Export JSON]으로 시각화 정의를 내보낼 수 있고, 상단 ⋮ 메뉴의
[Import JSON]으로 가져옵니다. 가져오기는 시각화 작성 권한이 있어야 보입니다.
:::

## 캠페인·캠페인 그룹 대시보드

조직 공용 대시보드와 별개로, **캠페인 상세**와 **캠페인 그룹 상세**의 Dashboard
탭은 그 캠페인(그룹)만을 위한 대시보드입니다. 처음에는 KPI 카드와 성과 추이
차트가 기본 구성으로 보이고([성과 확인](/claire/performance#캠페인-대시보드--kpi와-성과-추이)),
캠페인은 우상단 메뉴(⋮)의 **Customize dashboard**, 그룹은 [Customize]를 누르면
기본 구성이 실제 위젯으로 저장되면서 편집 모드가 열립니다.

- 편집 모드의 [Add visualization]에서 **Visualization**(이 캠페인·그룹의 지표로
  새 차트 만들기) 또는 **KPI Metric**(설정된 KPI 목표를 현재·직전 값과 함께
  카드로 추가)을 고릅니다. 조직 공용 시각화 목록에서 골라 넣는 방식은 아닙니다.
- 이 대시보드의 시각화는 범위가 해당 캠페인·그룹으로 고정되어 편집기의 Filter
  칸이 읽기 전용입니다. 그룹 대시보드의 KPI 카드는 그 캠페인이 그룹에서 빠지면
  빈 값으로 표시됩니다.
- 캠페인(그룹)당 대시보드는 하나이며, 배치 편집에는 해당 캠페인(그룹)과
  대시보드의 수정 권한이, 시각화 추가에는 시각화 작성 권한이 추가로 필요합니다. 북마크·기본 대시보드 지정은 조직 공용 대시보드에만 있습니다.

