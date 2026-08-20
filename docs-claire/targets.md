---
sidebar_position: 6
title: 지표와 KPI 규칙
---

# 지표와 KPI 규칙

**Targets** 섹션은 Claire가 다루는 지표 체계를 관리합니다. 세 층으로 구성됩니다 —
수집하는 **기본 지표**(Metric Categories), 그로부터 계산되는 **공식**(Formulas),
공식에 조건을 붙인 **KPI 규칙**(KPI Rules).

## Metric Categories — 기본 지표

매체에서 수집하는 원천 지표입니다. 기본 제공:

| 지표 | 단위 |
|---|---|
| Impressions / Clicks / Conversions / Plays / Completions | count |
| Media cost / Spend / Revenue | KRW |

지표별로 어떤 매체(DV360 · Google Ads · Meta · SA360)에서 수집 가능한지 표시됩니다.

![Metric Categories](/img/claire/metric-categories.png)

## Formulas — 파생 공식

기본 지표에서 계산되는 공식입니다. CTR · CVR · CPC · CPM · CPV · VTR · ROAS ·
Margin · Margin rate가 시스템 기본으로 제공되며, [New]로 조직 커스텀 공식을 추가할 수 있습니다.

![Formulas](/img/claire/metric-formulas.png)

## KPI Rules — 목표 규칙

공식에 방향 조건을 붙인 규칙입니다. 예: **Minimum CTR**(CTR ≥ 목표),
**Maximum CPC**(CPC ≤ 목표). 시스템 기본으로 CTR·VTR·ROAS 하한과
CPM·CPC·CPV 상한 규칙이 제공됩니다.

![KPI Rules](/img/claire/kpi-rules.png)

이 규칙에 캠페인별 목표값을 입력하는 방법은 [성과 확인 → KPI 목표 설정](/claire/performance#kpi-목표-설정)을 보세요.
