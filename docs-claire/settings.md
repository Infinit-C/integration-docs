---
sidebar_position: 7
title: 조직 설정과 알림
---

# 조직 설정과 알림

## Organization Settings

**Settings → Organization Settings**에서 조직 정보를 관리합니다.

![Organization Settings](/img/claire/organization-settings.png)

- **My Organization** — 조직 이름·설명
- **Chat Config** — Claire 대화 문맥의 공유 범위 (→ [대화 문맥 공유 범위](/claire/chat#대화-문맥-공유-범위))

## Platform Integrations — 매체 연동

조직에 연동된 매체 플랫폼을 한곳에서 관리합니다. [Connect]로 새 플랫폼을
연동하고, 연동된 플랫폼은 [Manage]에서 광고 계정·캠페인 불러오기를,
[Disconnect]로 연동 해제를 처리합니다. 연동 절차는
[캠페인 연결](/claire/campaigns#매체-연동--connect-위저드) 문서를 보세요.

![Platform Integrations](/img/claire/platform-integrations.png)

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

알아두면 좋은 동작:

- 평가는 몇 분 간격으로 자동 실행되고, 성과 수집 직후에도 즉시 평가됩니다.
- **평가값은 캠페인의 누적 합계 기준**입니다("최근 24시간" 같은 기간 창이
  아닙니다). 지출·노출처럼 계속 커지는 지표에 상한을 걸면 캠페인이 오래될수록
  언젠가 걸리게 되니, 소진 감시에는 원지표 상한보다 **일예산 대비 지출
  비율(budget ratio)** 소스가 적합합니다.
- 규칙을 **수정하면 위반·복구 카운트가 초기화**되어 처음부터 다시 셉니다.
- 규칙 삭제는 비활성화한 뒤에만 가능합니다.
- 예산 비율 알림은 캠페인에 일예산(Daily budget max)이 설정돼 있어야 만들 수 있습니다.

## Communication Groups — 알림 채널

알림을 받을 수신 그룹을 관리합니다. 알림 규칙에 연결해 두면 이벤트가
발생했을 때 이 그룹으로 알림이 갑니다. 채널은 두 종류입니다.

- **이메일** — 그룹을 만들면서 수신 주소를 등록합니다.
- **Slack** — [Add to Slack] 버튼으로 워크스페이스에 봇을 설치해서
  연결합니다. 공개 채널은 봇이 자동 참여하고, **비공개 채널은 봇을 먼저
  초대해야** 선택할 수 있습니다.

![Communication Groups](/img/claire/communication-groups.png)

## 사용자·권한 (관리자)

조직 사용자·그룹·권한 정책·API 키는 사이드바 **Security** 섹션에서 관리합니다.
→ [사용자·권한 관리](/claire/admin)
