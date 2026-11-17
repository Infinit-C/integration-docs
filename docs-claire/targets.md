---
sidebar_position: 7
title: 지표와 KPI 규칙
---

# 지표와 KPI 규칙

**목표** 섹션에서는 Claire가 다루는 지표 체계를 관리합니다. 지표 체계는
세 단계로 이루어집니다. 매체에서 수집하는 기본 지표(지표 분류),
그것으로 계산하는 수식(수식), 수식에 목표 조건을 붙인 KPI 규칙(KPI 규칙)입니다.

## 지표 분류 — 기본 지표

매체에서 수집하는 원천 지표입니다. 기본으로 제공되는 지표는 다음과 같습니다.

| 지표 | 단위 |
|---|---|
| Impressions / Clicks (link clicks) / Conversions / Plays / Completions | count |
| Media cost / Spend / Revenue | KRW |

지표마다 어떤 매체(DV360, Google Ads, Meta, SA360, Kakao Moment, 수동 업로드)에서
수집할 수 있는지 **플랫폼** 열에 함께 표시됩니다.

![지표 분류](/img/claire/metric-categories.png)

## 수식 — 파생 지표

기본 지표로 계산하는 수식입니다. CTR, CVR, CPC, CPM, CPV, VTR, ROAS,
Margin, Margin rate가 시스템 범위로 기본 제공되고, [새 수식]을 눌러 팀만의 수식을
추가할 수도 있습니다. 수식에는 사칙연산과 `round` · `round_up` · `round_down`
(자릿수 지정 반올림·올림·내림) 함수를 쓸 수 있습니다. 새 수식을 만들 때는
이름, 단위 템플릿(`{VALUE} %`처럼 `{VALUE}` 포함), 수식, 사용 가능한 플랫폼을 정합니다.

![수식](/img/claire/metric-formulas.png)

## KPI 규칙 — 목표 규칙

수식에 방향 조건을 붙인 규칙입니다. 예를 들어 **최소 CTR**은 CTR이 목표
이상이어야 하고(조건 GTE), **최대 CPC**는 CPC가 목표 이하여야 합니다(LTE). CTR·VTR·ROAS
하한과 CPM·CPC·CPV 상한 규칙이 기본으로 제공됩니다.

![KPI 규칙](/img/claire/kpi-rules.png)

[새 KPI 규칙]에서 범위·이름, 지표 종류(지표 분류 또는 수식)와 비교 방향
(실제 ≥ 목표 / 실제 ≤ 목표)을 정하고 [KPI 규칙 생성]을 누릅니다. 직접 만든
수식과 KPI 규칙은 목록 행 메뉴(⋮)에서 **수정 · 비활성화 · 삭제**할 수 있으며,
삭제는 비활성화한 뒤에만 가능합니다. 시스템 범위의 기본 항목은 지울 수 없습니다.

규칙에 캠페인별 목표값을 넣는 방법은 [성과 확인 → KPI 목표 설정](/claire/performance#kpi-목표-설정)에 있습니다.
