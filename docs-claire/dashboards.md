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

### 시각화 수정 권한

:::tip
시각화는 만든 사람 또는 조직 관리자만 수정할 수 있습니다. 목록의 톱니 아이콘에서 제목과 설정을 변경할 수 있으며, 화면에서 삭제하는 기능은 아직 제공하지 않습니다.
:::
