---
title: lifelines 生存曲线模板
type: code-template
status: active
backend: python
updated: 2026-06-10
tags:
  - dataviz
  - python
  - lifelines
  - survival
  - kaplan-meier
  - template
---

# lifelines 生存曲线模板

> Python 端生存分析主力。`KaplanMeierFitter` 出 KM 曲线，`add_at_risk_counts` 出 risk table，`CoxPHFitter` 出 HR。对应 R 的 [[survminer生存曲线模板]]。

## 1. KM 曲线 + risk table + log-rank

```python
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
from lifelines.plotting import add_at_risk_counts
import matplotlib.pyplot as plt
set_pub_style()

fig, ax = plt.subplots(figsize=(4, 4))
kmfs = []
colors = {"No": "#0072B2", "Yes": "#D55E00"}      # 医学二分类配色
for label, g in df.groupby("PREVHYP_label"):       # >>> PARAM 分组变量
    kmf = KaplanMeierFitter(label=label)
    kmf.fit(g["TIMEDTH"], event_observed=g["DEATH"])  # time=天, event=DEATH
    kmf.plot_survival_function(ax=ax, ci_show=True, color=colors[label])
    kmfs.append(kmf)

add_at_risk_counts(*kmfs, ax=ax)                  # risk table
ax.set_xlabel("Time (days)"); ax.set_ylabel("Survival probability")

# log-rank p 值
m = df["PREVHYP_label"]=="Yes"
res = logrank_test(df.TIMEDTH[m], df.TIMEDTH[~m],
                   df.DEATH[m], df.DEATH[~m])
ax.text(.05, .05, f"log-rank p = {res.p_value:.3g}", transform=ax.transAxes)
fig.savefig("km.pdf", bbox_inches="tight")
```

## 2. Cox 模型 → HR

```python
from lifelines import CoxPHFitter
cph = CoxPHFitter()
cph.fit(df[["TIMEDTH","DEATH","AGE_group","SEX","BMI","CURSMOKE"]],
        duration_col="TIMEDTH", event_col="DEATH")
cph.print_summary()          # HR=exp(coef), CI, p
cph.plot()                   # 系数(log HR)森林图；exp 后即 HR（见 森林图_ForestPlot）
# PH 假设检查： cph.check_assumptions(df)
```

## 3. 累积发病（competing-risk 之外的简单版）

```python
kmf.plot_cumulative_density(ax=ax)   # 1 - S(t)，累积事件概率
```

## 4. 关键参数（旋钮）

| 参数 | 作用 |
|---|---|
| `fit(durations, event_observed)` | time + 事件指示(1=事件,0=删失)|
| `ci_show` | 置信带 |
| `add_at_risk_counts` | risk table（顶刊标配）|
| `plot_survival_function` / `plot_cumulative_density` | 生存 / 累积发病 |
| `xlim`（ax）| 截断随访末端 |

## 5. 统计前置（先建对再画）

- 时间单位一致（TIMEDTH = 天）。
- event：DEATH 1=死亡=事件，0=删失。
- 组数别多（>4 曲线挤 → 限组/分面）。
- Cox 查 PH 假设 `check_assumptions`。

## 6. 常见错误（→ 返修，见 [[KM生存曲线_KaplanMeier]]）

- ❌ 没 risk table。
- ❌ 末端样本极少画到底 → `set_xlim` 截断。
- ❌ 漏删失/漏 log-rank p。
- ❌ 时间单位不清。
- ❌ 配色不一致（病例/对照换色）。

相关：[[KM生存曲线_KaplanMeier]] · [[survminer生存曲线模板]]（R 对应）· [[医学二分类配色]] · [[Python导出规范]]
