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
위저드가 열립니다. DV360, Google Ads, Meta, SA360을 지원합니다.

![플랫폼 연동 위저드](/img/claire/platform-connect.png)

1. **Select platform** — 연동할 매체를 고릅니다. 이미 연동된 매체는 목록에서 숨겨집니다.
2. **Authentication** — [Authorize]를 누르면 해당 매체의 로그인 화면으로 이동합니다.
   연동은 OAuth 방식이라 비밀번호나 토큰을 Claire에 직접 입력하지 않으며,
   인증이 끝나면 자동으로 다음 단계로 돌아옵니다.
3. **Select accounts** — 그 매체의 광고 계정 목록에서 가져올 계정을 골라 [Import accounts].
4. **Select campaigns** — 계정의 캠페인 중 등록할 것을 골라 [Finish setup].
   예전에 삭제했던 캠페인을 다시 고르면 복원 여부를 확인합니다.

연동을 마친 뒤에도 플랫폼의 [Manage]에서 언제든 계정을 더 가져오거나
캠페인을 추가로 등록할 수 있습니다.

![플랫폼 계정 관리](/img/claire/platform-accounts.png)

:::caution 연동 해제 시 주의
플랫폼을 [Disconnect]하면 그 계정으로 등록된 캠페인이 모두 비활성화되고
`Disconnected` 상태가 됩니다. 다시 쓰려면 재연동이 필요합니다.
:::

## 캠페인 관리

등록된 캠페인은 캠페인 그룹 상세의 **Campaigns 탭**과 **Operations →
Campaigns**(전체 목록)에서 관리합니다. 전체 목록에서는 코드·이름 검색과
상태·캠페인 그룹 필터를 쓸 수 있습니다.

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
