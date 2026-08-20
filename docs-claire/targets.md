---
sidebar_position: 6
title: 지표와 KPI 규칙
---

# 지표와 KPI 규칙

**Targets** 섹션에서는 Claire가 다루는 지표 체계를 관리합니다. 지표 체계는
세 단계로 이루어집니다. 매체에서 수집하는 기본 지표(Metric Categories),
그것으로 계산하는 공식(Formulas), 공식에 목표 조건을 붙인 KPI 규칙(KPI Rules)입니다.

## Metric Categories — 기본 지표

매체에서 수집하는 원천 지표입니다. 기본으로 제공되는 지표는 다음과 같습니다.

| 지표 | 단위 |
|---|---|
| Impressions / Clicks / Conversions / Plays / Completions | count |
| Media cost / Spend / Revenue | KRW |

지표마다 어떤 매체(DV360, Google Ads, Meta, SA360)에서 수집할 수 있는지 함께 표시됩니다.

![Metric Categories](/img/claire/metric-categories.png)

## Formulas — 파생 공식

기본 지표로 계산하는 공식입니다. CTR, CVR, CPC, CPM, CPV, VTR, ROAS,
Margin, Margin rate가 기본으로 제공되고, [New]를 눌러 조직만의 공식을
추가할 수도 있습니다.

![Formulas](/img/claire/metric-formulas.png)

## KPI Rules — 목표 규칙

공식에 방향 조건을 붙인 규칙입니다. 예를 들어 **Minimum CTR**은 CTR이 목표
이상이어야 하고, **Maximum CPC**는 CPC가 목표 이하여야 합니다. CTR·VTR·ROAS
하한과 CPM·CPC·CPV 상한 규칙이 기본으로 제공됩니다.

![KPI Rules](/img/claire/kpi-rules.png)

규칙에 캠페인별 목표값을 넣는 방법은 [성과 확인 → KPI 목표 설정](/claire/performance#kpi-목표-설정)에 있습니다.
