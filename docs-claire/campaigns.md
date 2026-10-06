---
title: 캠페인 연결
sidebar_position: 3
---
# 캠페인 연결

Claire의 모든 기능은 캠페인이 연결돼 있어야 동작합니다. 캠페인은 두 단계
구조로 관리합니다. 광고주·브랜드 단위 묶음인 **Campaign Group** 아래에
매체의 실제 캠페인인 **Campaign**이 속하는 구조입니다.

## 캠페인 그룹 만들기

**Operations → Campaign Groups**에서 [Create campaign group]을 눌러 광고주나 브랜드 단위
그룹을 만듭니다.

![캠페인 그룹 목록](/img/claire/campaign-groups.png)

그룹 상세에는 탭이 세 개 있습니다.

- **Dashboard** — 그룹 캠페인들의 KPI 카드와 캠페인별 성과 추이 차트.
  [Customize]로 위젯을 직접 구성할 수 있습니다 (→ [캠페인·그룹 대시보드](/claire/dashboards#캠페인캠페인-그룹-대시보드))
- **Campaigns** — 이 그룹에 속한 캠페인 목록 (기간 · 수집 단위 · 상태).
  [Import campaigns]로 매체 연동 화면으로 이동해 캠페인을 더 불러옵니다.
- **History** — 변경 이력

그룹에 어떤 캠페인을 넣을지는 그룹 [Edit] 화면에서 정합니다. **Campaigns**
칸의 [Add campaigns]를 누르면 아직 그룹이 없는 캠페인 목록이 열리고 [Add]로
담을 수 있습니다. 이미 속한 캠페인은 각 행의 [Remove]로 뺍니다. 추가·제거는
[Save]를 눌러야 반영되며, 캠페인 편집 화면의 **Campaign group** 선택으로 다른
그룹에 옮길 수도 있습니다.

## 매체 연동 — Connect 위저드

**Settings → Platform Integrations**에서 [Connect]를 누르면 4단계 안내
위저드가 열립니다. DV360, Google Ads, Meta, SA360, Kakao Moment를 지원합니다.
Naver GFA는 목록에 보이지만 아직 `Not available`로 표시되어 선택할 수 없습니다.

![플랫폼 연동 위저드](/img/claire/platform-connect.png)

1. **Select platform** — 연동할 매체를 고릅니다. 이미 연동된 매체는 목록에서 숨겨지고, 연동 미지원 매체는 흐리게 표시됩니다.
2. **Authentication** — [Authorize]를 누르면 해당 매체의 로그인 화면으로 이동합니다.
   연동은 OAuth 방식이라 비밀번호나 토큰을 Claire에 직접 입력하지 않으며,
   인증이 끝나면 자동으로 다음 단계로 돌아옵니다.
3. **Select accounts** — 그 매체의 광고 계정 목록에서 가져올 계정을 골라 [Import accounts].
4. **Select campaigns** — 계정의 캠페인 중 등록할 것을 골라 [Finish setup].
   예전에 삭제했던 캠페인을 다시 고르면 복원 여부를 확인합니다.

Kakao Moment는 카카오 비즈니스 계정으로 인증하며, 광고 계정과 캠페인은 불러오지만
예산·기간 정보는 매체에서 제공하지 않아 비어 있습니다. 예산은 캠페인 편집에서
직접 입력할 수 있습니다.

Kakao Moment는 **광고 계정마다 인증 정보를 따로 보관**합니다. 계정 관리 화면의
[Import accounts]를 누르면 다른 매체와 달리 카카오 인증을 먼저 거친 뒤 계정
선택 화면으로 돌아오고, 거기서 고른 계정에 그 인증 정보가 저장됩니다. 그래서
나중에 다른 광고 계정을 인증해도 앞서 붙여 둔 계정의 수집은 끊기지 않습니다.
연동을 마친 뒤 광고 계정을 더 붙이려면 [Connect]가 아니라 해당 매체의
[Manage] → [Import accounts]로 들어가세요.

연동을 마친 뒤에도 플랫폼의 [Manage]에서 언제든 계정을 더 가져오거나
캠페인을 추가로 등록할 수 있습니다.

![플랫폼 계정 관리](/img/claire/platform-accounts.png)

:::caution 연동 해제 시 주의
플랫폼을 [Disconnect]하면 그 계정으로 등록된 캠페인이 모두 비활성화되고
`Disconnected` 상태가 됩니다. 다시 쓰려면 재연동이 필요합니다.
:::

## 캠페인 관리

등록된 캠페인은 캠페인 그룹 상세의 **Campaigns 탭**과 **Operations →
Campaigns**(전체 목록)에서 관리합니다. 전체 목록 상단의 필터 칸에 조건식을
쓰고 [Apply]를 누르면 목록이 좁혀집니다. 입력 중에 필드와 값이 자동 완성되고,
표의 캠페인 그룹·플랫폼·상태 칸에 마우스를 올리면 그 값을 필터로 바로 추가할
수 있습니다. 필터는 주소(URL)에 담기므로 링크를 복사해 공유할 수 있습니다.

```
campaign.status: enabled AND platform: meta
campaign_group.name: "브랜드A" AND NOT campaign.name: *테스트*
campaign.budget.daily >= 100000
```

값은 정확히 일치해야 하며, 부분 일치는 `*브랜드*`처럼 별표를 씁니다. 쓸 수 있는
필드는 `campaign.name` / `.code` / `.status`(enabled · disabled · disconnected), `campaign_group.name` / `.code`(`none`이면 그룹 없음), `platform`,
`campaign.budget.daily` / `.total`, `campaign.period.start` / `.end`이며,
`AND` `OR` `NOT`과 괄호로 조합합니다. 캠페인 그룹 목록에도 같은 필터 칸이 있습니다.

![전체 캠페인 목록](/img/claire/campaigns-list.png)

목록 상단 [Import campaigns]를 누르면 연동된 매체를 골라 캠페인을 더 불러올
수 있습니다. 재인증이 필요한 매체는 여기에서도 [Reauthorize]로 표시됩니다.

### 여러 캠페인 한꺼번에 처리하기

목록 맨 왼쪽 체크박스로 캠페인을 고르고 상단 **Actions (N)** 메뉴를 열면
선택한 캠페인에 한꺼번에 적용할 수 있습니다. 머리글 체크박스는 현재 페이지에서
고를 수 있는 캠페인을 모두 선택하며, 페이지를 넘겨도 선택은 유지됩니다.

| 메뉴 | 하는 일 |
|---|---|
| **Recollect selected campaigns** | 선택한 캠페인의 성과를 지정한 기간으로 다시 수집 (→ [성과 확인](/claire/performance#성과-데이터-수집)) |
| **Enable** / **Disable** | 캠페인 활성화 / 비활성화 |
| **Disconnect** | 매체 연결 해제 |

- 캠페인 수정 권한이 없으면 체크박스가 잠깁니다. Enable은 비활성 캠페인만,
  Disable은 활성 캠페인만 고른 경우에 눌립니다.
- Enable · Disable · Disconnect는 처리 후 **실패한 캠페인만 선택 상태로 남아**
  바로 다시 시도할 수 있습니다. Recollect는 창 안에서 재시도하며, 창을 닫으면
  선택이 모두 풀립니다.

캠페인 상세에는 **Dashboard · Details · Alerts · History** 탭이 있습니다
(DV360은 **Insertion orders** 탭 추가). Dashboard 탭은 KPI 카드와 성과 추이
차트를 보여주고([성과 확인](/claire/performance)), Details 탭은 매체 연결
정보(URN, 연결 계정, 플랫폼 캠페인 ID, 예산, 기간, 수집 주기와 다음 수집
시각)를 보여줍니다. 캠페인 기간(시작일·종료일)은 매체에서 가져온 값이라
Claire에서 고칠 수 없습니다. URN 옆 복사 버튼으로 식별자를 복사할 수 있고,
열려 있는 탭은 주소(URL)에 저장되므로 특정 탭을 바로 가리키는 링크를 동료에게
공유할 수 있습니다.

우상단 메뉴(⋮)에 **Edit · Disable/Enable · Delete · KPI Target Settings ·
Collect now**가 모여 있습니다.

![캠페인 상세](/img/claire/campaign-detail.png)

캠페인과 캠페인 그룹은 **비활성화(Disable) → 삭제(Delete)** 순서로만 지울
수 있습니다. 활성 상태에서는 삭제 버튼이 노출되지 않으니, 정리할 때는
먼저 비활성화하세요.

:::tip
캠페인 상세 우하단의 채팅 버튼을 누르면, 이 캠페인의 데이터를 기준으로
Claire에게 바로 질문할 수 있습니다. → [Claire와 대화하기](/claire/chat)
:::
