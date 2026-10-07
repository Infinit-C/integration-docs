---
sidebar_position: 10
title: 조직 설정과 알림
---

# 조직 설정과 알림

## Organization Settings

**Settings → Organization Settings**에서 조직 정보를 관리합니다. 우측 상단
계정 메뉴의 **Organization Settings**로도 같은 화면이 열립니다.

![Organization Settings](/img/claire/organization-settings.png)

탭이 두 개입니다.

- **My Organization** — 조직 이름·설명
- **Chat Config** — Claire 대화 문맥의 공유 범위 (→ [대화 문맥 공유 범위](/claire/chat#대화-문맥-공유-범위))

{/* 임시 블라인드 — Payment methods 탭 (운영 미배포)
- **Payment methods** — 구독 결제에 쓸 카드 (아래 참고)
*/}

{/* 임시 블라인드 — Payment methods 섹션 (운영 미배포)
### Payment methods — 결제 수단

구독 결제에 사용할 카드를 등록해 두는 곳입니다. **카드를 등록해도 그 자리에서
결제가 일어나지는 않습니다.**

- [Add]를 누르면 토스페이먼츠 카드 등록 화면으로 이동합니다. **카드 번호와
  인증 정보는 토스페이먼츠 화면에서 입력**하며 Claire는 카드 번호를 받지
  않습니다. 등록이 끝나면 자동으로 결제 수단 화면으로 돌아옵니다.
- 등록된 카드는 **Card**(카드사)와 **Card number**(끝 4자리만 남긴 마스킹
  번호)로 표시됩니다. 등록된 카드가 없으면 "No payment methods registered."가
  보입니다.
- 목록 조회는 조직 읽기 권한이면 되지만, [Add]는 **조직 수정 권한**이 있어야
  보입니다. 등록 화면을 열어 둔 채 15분이 지나면 세션이 만료되어 처음부터
  다시 해야 합니다.
- 카드 삭제나 기본 카드 지정은 아직 화면에서 지원하지 않습니다. 요금제 선택·
  청구서 조회 화면도 아직 없습니다.

:::note
카드 등록을 취소하면 "Card registration was canceled.", 중간에 실패하면
"Card registration could not be completed."가 표시됩니다. 다른 계정으로
로그인한 뒤 등록을 이어가면 세션이 맞지 않아 처음부터 다시 시작해야 합니다.
:::
*/}

## Platform Integrations — 매체 연동

조직에 연동된 매체 플랫폼을 한곳에서 관리합니다. [Connect]로 새 플랫폼을
연동합니다(DV360 · Google Ads · Meta · SA360 · Kakao Moment). 연동된 플랫폼은
[Manage]에서 광고 계정·캠페인을 불러오고, [Disconnect]로 연동을 해제합니다. 연동 절차는
[캠페인 연결](/claire/campaigns#매체-연동--connect-위저드) 문서를 보세요.

![Platform Integrations](/img/claire/platform-integrations.png)

:::caution Reauthorization required
매체 쪽에서 인증이 만료되거나 취소되면(현재 Meta 토큰 만료 시) 상태가
`Connected` 대신 **Reauthorization required**로 바뀌고, 그동안 이 매체의
캠페인은 수집과 불러오기가 멈춥니다. [Reauthorize]를 눌러 Connect 위저드에서
다시 인증하면 기존 계정·캠페인 그대로 수집이 재개됩니다. [Manage]는 재인증
전까지 숨겨집니다.
:::

## Alerts — 알림 규칙

**Monitor → Alerts**에서 알림 규칙을 만듭니다. 조건을 벗어나면 지정한
채널(이메일·Slack)로 알림이 가고, 발생 이력은 **Alert History**에 쌓입니다.

![Alerts](/img/claire/alerts.png)

규칙을 만들 때 정하는 것들:

- **감시 대상** — 캠페인 그룹 전체, 특정 캠페인, 또는 (DV360) 게재 항목 단위
- **감시 값(Source)** — 캠페인의 KPI 목표, 일예산 대비 지출 비율, 원지표,
  공식, 또는 여러 값을 조합한 수식 중 선택
- **조건** — 비교 연산자와 임계값. 여러 조건을 AND/OR로 묶을 수 있습니다
- **심각도** — Info · Warning · Critical
- **트리거/복구 횟수** — 연속 N회 위반 시 발생, 연속 M회 정상이면 복구
  알림. 일시적 튐에 반응하지 않게 하려면 횟수를 올리세요
- **쿨다운·반복** — 위반이 지속될 때 재알림 간격(기본 1시간)
- **평가 기간(Evaluation window)** — 어느 구간의 데이터로 값을 계산할지 (아래 참고)

### 평가 기간과 데이터 없음

규칙의 **3. Set the period** 단계에서 평가값을 계산할 구간을 정합니다.
규칙 안의 모든 감시 값이 같은 구간을 씁니다.

| 항목 | 선택지 | 설명 |
|---|---|---|
| **Period** | Last N hours · Today so far · Month to date · All time | 평가 시점에서 N시간 거슬러 보기 / 오늘 0시부터 / 이달 1일부터 / 수집된 전체 |
| **Hours to look back** | 1~2160시간 | Last N hours일 때만 입력 (기본 24시간) |
| **Aggregation** | Sum · Average · Minimum · Maximum over the period | Sum은 구간의 원지표를 합친 뒤 공식을 계산(CTR은 총 클릭/총 노출), 나머지는 수집 시점별 값의 평균·최소·최대 |
| **Evaluate every (minutes)** | 30~1440분 | 최소 평가 간격 (기본 30분). 수집 주기를 바꾸지는 않습니다 |
| **Evaluation delay (minutes)** | 0~10080분 | 매체 데이터 반영 지연을 감안해 구간 끝을 뒤로 미룸 (기본 60분) |
| **Timezone** | IANA 이름 | Today so far · Month to date의 날짜 경계 기준 |
| **When data is missing** | Keep state without notification · Keep state and notify No data | 구간에 데이터가 없을 때의 동작 (기본은 알림 없음) |

- **새로 만드는 규칙의 기본값은 "최근 24시간 합계, 60분 지연"**입니다. 예를 들어
  13:00 평가는 어제 12:00부터 오늘 12:00 직전까지의 데이터로 계산합니다.
- 이 기능이 생기기 **전에 만든 규칙은 All time(캠페인 누적 합계)**로
  유지됩니다. 지출·노출처럼 계속 커지는 지표에 상한을 건 규칙은 캠페인이
  오래될수록 언젠가 걸리게 되니, Last N hours로 바꾸거나 **일예산 대비 지출
  비율(budget ratio)** 소스를 쓰세요.
- 구간에 데이터가 없으면 0으로 보지 않고 **No data**로 기록합니다. 상태는 그대로
  유지되고 위반·복구 연속 횟수만 초기화되며, 복구로 치지도 않습니다. 목록의
  State에 주황색 **No data** 배지가 뜹니다. "Keep state and notify No data"를
  고르면 채널로 No data 알림도 갑니다. 측정값이 0인 것은 정상 데이터입니다.
- 규칙 편집 화면의 [Run evaluation preview]로 지금 설정이 실제로 어떤 구간과
  값으로 계산되는지 저장 전에 확인할 수 있습니다.
- 목록의 [Evaluations]를 누르면 **Evaluation history**가 열려 평가 시각, 구간,
  결과(normal · triggered · No data), 값별 수치를 확인할 수 있습니다.

알아두면 좋은 동작:

- 평가는 5분마다 도는 정기 평가와 자동 성과 수집 직후에 실행되며, 규칙마다
  Evaluate every 간격이 지났을 때만 실제로 계산합니다. [Collect now]로 수동
  수집한 데이터는 그 자리에서 평가되지 않고 다음 정기 평가에 반영됩니다.
- 규칙을 **수정하면 위반·복구 카운트가 초기화**되어 처음부터 다시 셉니다.
- 규칙 삭제는 비활성화한 뒤에만 가능합니다.
- 예산 비율 알림은 캠페인에 일예산(Daily budget max)이 설정돼 있어야 만들 수 있고,
  기준값은 0~100%만 입력할 수 있습니다. 지출은 Meta · Kakao Moment는 Spend,
  그 외 매체는 Media cost 지표로 계산합니다.
- 기준값(Threshold) 칸은 천 단위 쉼표가 붙어 표시되고, 화면의 지표 값은 소수점
  둘째 자리까지만 보여줍니다.
- **Alert History**의 이벤트 종류는 Triggered(발생) · Recovered(복구) ·
  Repeated(반복 알림) · No data(데이터 없음)입니다.

## Communication Groups — 알림 채널

알림을 받을 수신 그룹을 관리합니다. 알림 규칙이나 [정기 요약](/claire/custom-summaries)에
연결해 두면 이 그룹의 채널로 발송됩니다. 채널은 두 종류입니다.

- **이메일** — 그룹을 만들면서 수신 주소를 등록합니다.
- **Slack** — [Add to Slack] 버튼으로 워크스페이스에 봇을 설치해서
  연결합니다. 공개 채널은 봇이 자동 참여하고, **비공개 채널은 봇을 먼저
  초대해야** 선택할 수 있습니다.

![Communication Groups](/img/claire/communication-groups.png)

## 사용자·권한 (관리자)

조직 사용자·그룹·권한 정책은 사이드바 **Security** 섹션에서 관리합니다.
→ [사용자·권한 관리](/claire/admin)
