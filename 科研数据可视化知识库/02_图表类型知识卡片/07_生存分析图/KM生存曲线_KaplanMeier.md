---
chart_name: Kaplan-Meier 生存曲线
chart_name_en: Kaplan-Meier curve
chart_family: 生存分析图
data_type:
  - time_to_event
  - event_indicator
  - categorical_group
recommended_backend:
  r: survminer
  python: lifelines
difficulty: intermediate
priority: high
status: tested
tags:
  - dataviz
  - chart
  - survival
  - kaplan-meier
  - r
  - python
---

# Kaplan-Meier 生存曲线 Kaplan-Meier curve

> 用阶梯曲线展示**生存概率随时间的变化**，处理右删失数据；配 risk table 与 log-rank p 值是医学论文标配。

## 1. 图表定位

回答“**各组随时间存活/未发生事件的概率如何，组间差异是否显著**”。处理删失（研究结束仍存活/失访）。

## 2. 适用场景

- 生存/事件时间数据（time + event 指示）。
- 比较组间生存（治疗/对照、危险分层、暴露/未暴露）。
- 配 risk table 展示各时点 at-risk 人数。
- Framingham：TIMEDTH（天）+ DEATH（1=死）按 PREVHYP/SEX/AGE_group 分组。

## 3. 不适用场景

- 无删失的简单时间趋势 → [[折线趋势图_Line]]。
- 有竞争风险（多种互斥事件）→ 累积发病函数（CIF）/ Fine-Gray，而非简单 KM。
- 想要协变量调整效应 → Cox 模型 + [[森林图_ForestPlot]]（KM 是单/分组未调整）。
- 末端样本极少 → 曲线抖动大，需截断。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 必需 |
|---|---|---|---|
| time | continuous | 到事件/删失时间（TIMEDTH，天）| 必需 |
| event | binary | 1=事件发生(DEATH=1)，0=删失 | 必需 |
| group | categorical | 分组 | 比较时必需 |

一行一个个体。**纵向数据需先取每人一条生存记录**（如基线 PERIOD==1，或按设计构造），见 [[Framingham数据集说明]]。

## 5. 图表架构选择

### 5.1 基础架构
- x = 时间，y = 生存概率（0–1）；阶梯曲线；
- 删失标记（+）；
- log-rank p 值；
- 可选置信带。

### 5.2 高质量架构（发表级）
- **risk table**（顶刊几乎必带）：各时点 at-risk 人数。
- 删失刻度清晰。
- 末端样本少 → `xlim` 截断到可靠区间。
- 组数 ≤ 4，颜色 + 线型冗余。
- y 轴可 0–1 或聚焦（如 0.5–1），但要诚实标注。

## 6. 配色选择
- 二分组 [[医学二分类配色]]（如高血压 Yes 朱红 / No 蓝）。
- 多组 Okabe-Ito + 线型（[[色盲友好与打印友好原则]]）。

## 7. R 实现方案

### 7.1 推荐包
survival、survminer

### 7.2 关键参数
见 [[survminer生存曲线模板]]：`survfit(Surv(time,event)~group)`、`ggsurvplot(risk.table=, pval=, conf.int=, censor=, xlim=, break.time.by=)`。

### 7.3 基础代码模板
```r
library(survival); library(survminer)
fit <- survfit(Surv(TIMEDTH, DEATH) ~ PREVHYP, data = base)   # base = 每人一条
ggsurvplot(fit, data = base, pval = TRUE, conf.int = TRUE,
           xlab = "Time (days)", ylab = "Survival probability")
```

### 7.4 发表级代码模板
```r
ggsurvplot(
  fit, data = base,
  pval = TRUE, conf.int = TRUE, risk.table = TRUE,
  risk.table.height = 0.25, censor = TRUE,
  break.time.by = 1000, xlim = c(0, 8000),          # 截断末端
  legend.title = "Hypertension", legend.labs = c("No","Yes"),
  palette = c("#0072B2","#D55E00"),                  # 医学二分类
  xlab = "Time (days)", ylab = "Survival probability",
  ggtheme = theme_minimal(base_size = 9))
```

## 8. Python 实现方案

### 8.1 推荐包
lifelines、matplotlib

### 8.2 关键参数
见 [[lifelines生存曲线模板]]：`KaplanMeierFitter.fit(durations, event_observed)`、`plot_survival_function(ci_show=)`、`add_at_risk_counts()`、`logrank_test()`。

### 8.3 基础代码模板
```python
from lifelines import KaplanMeierFitter
fig, ax = plt.subplots(figsize=(4,4))
for label,g in base.groupby("PREVHYP_label"):
    KaplanMeierFitter(label=label).fit(g.TIMEDTH, g.DEATH).plot_survival_function(ax=ax)
ax.set_xlabel("Time (days)"); ax.set_ylabel("Survival probability")
```

### 8.4 发表级代码模板
见 [[lifelines生存曲线模板]] 第 1 节（含 risk table + log-rank + 配色 + 截断）。

## 9. 示例图像

### 9.1 网络优秀示例
见 [[KM_优秀示例]]（含 survminer risk table 范式、NEJM 风 KM）。
本库自制范式图（合成数据，双组 KM + CI）：

![[demo_km.png]]

### 9.2 Framingham 数据测试示例
✅ 已跑通（按 PREVHYP 的 KM + risk table + log-rank；基线每人一条生存记录）。代码见 [[R测试记录]] / [[Python测试记录]]。

R（survminer ggsurvplot，risk table + p）：

![[fig_km_prevhyp_r.png]]

Python（lifelines + add_at_risk_counts）：

![[fig_km_prevhyp_py.png]]

> 结论：高血压组生存显著低于无高血压组（log-rank p < 0.0001）。两后端曲线与 risk table 一致；R 的 survminer 一步出 risk table 最省事，正是 [[R与Python后端选择规则]] 推荐 R 做生存图的原因。

## 10. 常见错误
- 不带 risk table。
- 末端样本极少仍画到底，抖动误导。
- 漏删失标记。
- 时间单位不清（天/月/年）。
- 直接用纵向多行数据（一人多行）建 KM → 必须先整理为生存记录。
- 有竞争风险仍用 KM 估计累积发病（高估）。

## 11. 自动返修规则
- 缺 risk table → 自动添加。
- 末端 at-risk 很少 → `xlim` 截断 + 说明。
- 组 > 4 → 限组或分面。
- 漏 p 值 → 加 log-rank。
- 竞争风险 → 提示改 CIF/Fine-Gray。

## 12. 与其他图表的关系
- vs 累积发病曲线：KM 画生存 S(t)，CIF 画 1−S(t) 或竞争风险下的累积发病。
- vs [[森林图_ForestPlot]]：Cox 森林图给调整后 HR，KM 给未调整分组曲线，二者互补。
- vs [[折线趋势图_Line]]：KM 处理删失 + 阶梯，普通折线不处理删失。

## 13. 质量检查清单
- [ ] 有 risk table？
- [ ] 删失标记在位？
- [ ] log-rank p 标注？
- [ ] 时间单位清楚？
- [ ] 末端是否需截断？
- [ ] 配色一致、色盲友好？
- [ ] 适合论文导出？

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建立初稿 | 需先把纵向数据整理为生存记录 | 构造 base，跑 PREVHYP KM |

相关：[[森林图_ForestPlot]] · [[折线趋势图_Line]] · [[survminer生存曲线模板]] · [[lifelines生存曲线模板]] · [[医学二分类配色]] · [[Framingham数据集说明]]
