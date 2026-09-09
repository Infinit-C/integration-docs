---
sidebar_position: 9
title: 정기 요약 보내기
---

# 정기 요약 보내기

**Monitor → Custom Summaries**는 캠페인 성과를 정해진 시각에 Slack 채널이나
이메일로 자동 발송하는 기능입니다. "매주 월요일 9시에 지난 7일 지출·CTR을
팀 채널로"처럼 한 번 만들어 두면 이후엔 손이 가지 않습니다. 발송 내용은
직접 쓴 마크다운 서식이며, AI가 문장을 생성하지는 않습니다.

![Custom Summaries](/img/claire/custom-summaries.png)

## 요약 만들기

[New]를 누르면 네 단계로 나뉜 입력 화면이 열립니다.

![새 요약 만들기](/img/claire/custom-summary-new.png)

1. **Custom Summary target** — 캠페인 그룹 전체(Entire campaign group) 또는
   캠페인 하나를 고릅니다. 그룹에 속하지 않은 캠페인은 Campaign group을
   "No campaign group"으로 두고 캠페인만 고릅니다.
2. **Summary document** — 발송할 본문입니다 (아래 참고, 최대 10,000자).
3. **Schedule** — 요약 이름, 주기(Daily · Weekly · Monthly), 요일 또는 일자,
   발송 시각, 시간대(기본 Asia/Seoul).
4. **Delivery channels** — 받을 채널을 하나 이상 체크합니다. 채널은
   [Communication Groups](/claire/settings#communication-groups--알림-채널)에
   미리 등록돼 있어야 합니다.

## 본문 작성법

본문 맨 위에 `@metric` 줄로 쓸 지표를 선언하고, 빈 줄 하나를 띄운 뒤
마크다운으로 메시지를 씁니다. 편집기의 [Raw metric] [Formula] [KPI target]
[Budget utilization] 버튼이나 `/metric` 명령으로 선언 줄을 넣을 수 있고,
Preview 탭에서 결과를 미리 봅니다.

```markdown
@metric spend = raw("spend", period="last_7_days")
@metric ctr = formula("ctr", period="last_7_days")
@metric clicks = raw("clicks", period="last_7_days")
@metric cpc = expression("${spend} / ${clicks}", period="last_7_days")

# {{summary.name}} — {{campaignGroup.name}}

지난 7일 지출은 {{spend.current}}로 직전 주 대비 {{spend.change}}입니다.
CTR {{ctr}} · 클릭 {{clicks}} · CPC {{cpc}}

{{metrics}}
```

- **기간**은 `all_time` · `last_24_hours` · `last_7_days` · `last_30_days` 중
  하나입니다. `all_time`은 비교 대상이 없어 변화율이 N/A로 나옵니다.
- 지표 토큰은 `{{별칭}}`(현재값), `{{별칭.previous}}`(직전 같은 길이 구간),
  `{{별칭.change}}`(변화율), `{{별칭.period}}`가 있고, `{{metrics}}`는 선언한
  지표를 모두 목록으로 펼칩니다. 이름 토큰은 `{{summary.name}}`,
  `{{campaignGroup.name}}`, `{{campaign.name}}`입니다.
- `expression("${spend} / ${clicks}", period="last_7_days")`처럼 앞서 선언한
  별칭으로 계산식을 만들 수 있습니다. 첫 번째 선언으로는 쓸 수 없고, `period`는
  필수입니다. 다른 선언 함수도 `period`를 항상 적어야 합니다.
- 데이터가 없는 지표는 `No data`로 표시됩니다.

## 발송 확인

요약 상세에서 다음 발송 시각과 마지막 발송, 채널, 선언된 지표 표, 렌더링된
본문을 확인할 수 있습니다. [Send now]를 누르면 예약과 무관하게 즉시
생성·발송되며, 결과는 하단 **Delivery history**에 실행별·채널별로 남습니다
(상태 pending · sent · failed, 실패 시 오류 메시지).

:::note
Slack 비공개 채널은 봇을 먼저 초대해야 발송됩니다. 이메일은 요약 이름이
제목이 되고 본문은 마크다운이 HTML로 변환돼 갑니다.
:::
