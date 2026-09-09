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
- **Trends** — 그룹 캠페인들의 성과 추이 (캠페인별 시리즈로 비교)
- **Campaigns** — 이 그룹에 연결된 캠페인 목록
- **History** — 변경 이력

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

캠페인 상세로 들어가면 매체 연결 정보(URN, 연결 계정, 플랫폼 캠페인 ID,
예산, 수집 주기)와 함께 KPI, Trends, Alerts, History 탭이 있습니다.
URN 옆 복사 버튼으로 식별자를 복사할 수 있고, 열려 있는 탭은 주소(URL)에
저장되므로 특정 탭을 바로 가리키는 링크를 동료에게 공유할 수 있습니다.

![캠페인 상세](/img/claire/campaign-detail.png)

캠페인과 캠페인 그룹은 **비활성화(Disable) → 삭제(Delete)** 순서로만 지울
수 있습니다. 활성 상태에서는 삭제 버튼이 노출되지 않으니, 정리할 때는
먼저 비활성화하세요.

:::tip
캠페인 상세 우하단의 채팅 버튼을 누르면, 이 캠페인의 데이터를 기준으로
Claire에게 바로 질문할 수 있습니다. → [Claire와 대화하기](/claire/chat)
:::
