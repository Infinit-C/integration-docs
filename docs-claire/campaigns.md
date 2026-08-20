---
title: 캠페인 연결
sidebar_position: 3
---
# 캠페인 연결

Claire의 모든 기능은 캠페인이 연결돼 있어야 동작합니다. 캠페인은 두 단계
구조로 관리합니다. 광고주·브랜드 단위 묶음인 **Campaign Group** 아래에
매체의 실제 캠페인인 **Campaign**이 속하는 구조입니다.

## 캠페인 그룹 만들기

**Operations → Campaign Groups**에서 [New]를 눌러 광고주나 브랜드 단위
그룹을 만듭니다.

![캠페인 그룹 목록](/img/claire/campaign-groups.png)

그룹 상세에는 탭이 네 개 있습니다.

- **KPI** — 이 그룹의 KPI 목표 현황
- **Trends** — 그룹 단위 성과 추이
- **Campaigns** — 이 그룹에 연결된 캠페인 목록
- **History** — 변경 이력

## 매체 연동과 캠페인 불러오기

캠페인은 **Settings → Platform Integrations**를 거쳐 세 단계로 불러옵니다.

1. **플랫폼 연동** — Platform Integrations에서 [Connect]를 눌러 매체 플랫폼
   (Meta, DV360, Google Ads, SA360)을 조직에 연동합니다.
2. **광고 계정 불러오기** — 연동한 플랫폼의 [Manage]로 들어가 [Import accounts]를
   누르면 그 플랫폼의 광고 계정을 불러와 저장할 수 있습니다.

   ![플랫폼 계정 관리](/img/claire/platform-accounts.png)

3. **캠페인 저장** — 계정의 [Manage]에서 가져올 캠페인을 선택하고
   [Save selected]를 누르면 Claire에 캠페인이 저장됩니다.

저장된 캠페인은 캠페인 그룹 상세의 **Campaigns 탭**에서 확인하고 관리합니다.
탭 상단의 [Import campaigns]를 눌러도 같은 불러오기 화면으로 이동합니다.

![캠페인 목록](/img/claire/campaign-group-campaigns.png)

목록에는 캠페인마다 Claire 내부 코드(Code), 매체(Platform), 수집 단위(Metric
aggregation), 상태(Status)가 표시됩니다.

## 캠페인 상세

캠페인의 [View details]로 들어가면 매체 연결 정보(URN, 연결 계정, 플랫폼
캠페인 ID, 예산)와 함께 KPI, Trends, Alerts, History 탭이 있습니다.

![캠페인 상세](/img/claire/campaign-detail.png)

:::tip
캠페인 상세 우하단의 채팅 버튼을 누르면, 이 캠페인의 데이터를 기준으로
Claire에게 바로 질문할 수 있습니다. → [Claire와 대화하기](/claire/chat)
:::

## 전체 캠페인 목록

그룹과 상관없이 조직의 모든 캠페인을 보려면 **Operations → Campaigns**를
여세요. 검색창과 상태·캠페인 그룹 필터로 원하는 캠페인을 빠르게 찾을 수 있습니다.

![전체 캠페인 목록](/img/claire/campaigns-list.png)
