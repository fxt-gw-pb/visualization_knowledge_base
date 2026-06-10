---
title: survminer 生存曲线模板
type: code-template
status: active
backend: r
updated: 2026-06-10
tags:
  - dataviz
  - r
  - survminer
  - survival
  - kaplan-meier
  - template
---

# survminer 生存曲线模板

> R 端生存可视化主力。`survfit` 建模 → `ggsurvplot` 出 KM 曲线 + risk table + p 值。配合 [[KM生存曲线_KaplanMeier]]。

## 1. KM 曲线 + risk table（标准发表版）

```r
library(survival); library(survminer)

# 1) 建模：time = TIMEDTH(天), event = DEATH(1=死亡)
fit <- survfit(Surv(TIMEDTH, DEATH) ~ PREVHYP, data = df)  # >>> PARAM 分组变量

# 2) 出图
p <- ggsurvplot(
  fit, data = df,
  fun = NULL,                      # NULL=生存概率；"event"=累积发病；"cumhaz"=累积风险
  conf.int = TRUE,                 # 置信带
  pval = TRUE,                     # log-rank p 值
  risk.table = TRUE,               # 风险表（at-risk 人数）
  risk.table.height = 0.25,
  censor = TRUE,                   # 删失标记
  xlab = "Time (days)", ylab = "Survival probability",
  legend.title = "Hypertension",
  legend.labs = c("No", "Yes"),
  palette = c("#0072B2", "#D55E00"),   # 医学二分类配色
  break.time.by = 1000,                # x 轴刻度间隔
  ggtheme = theme_minimal(base_size = 9)
)
p
```

## 2. Cox 模型森林图（survminer::ggforest）

```r
cox <- coxph(Surv(TIMEDTH, DEATH) ~ AGE_group + SEX + BMI + CURSMOKE, data = df)
ggforest(cox, data = df)          # HR + CI + p，自动森林图
summary(cox)                      # 看 HR / CI / PH 假设需另查 cox.zph()
```

## 3. 关键参数（旋钮）

| 参数 | 作用 |
|---|---|
| `Surv(time, event)` | 生存对象；event 1=事件 0=删失 |
| `fun` | 生存 / 累积发病("event") / 累积风险("cumhaz") |
| `conf.int` | 置信带 |
| `pval` | log-rank p |
| `risk.table` | 风险表（顶刊标配）|
| `break.time.by` | 时间轴刻度 |
| `palette` | 配色（接 [[医学二分类配色]]）|
| `xlim` | 截断随访末端（末端样本少抖动大时）|

## 4. 统计前置检查（先建对模型再画）

- 时间单位一致（本数据 TIMEDTH 是**天**）。
- event 编码：DEATH 1=死亡=事件，0=删失。
- 组数别太多（>4 曲线挤，限组或分面）。
- Cox 需查 PH 假设：`cox.zph(cox)`。

## 5. 常见错误（→ 返修，见 [[KM生存曲线_KaplanMeier]]）

- ❌ 不带 risk table → 顶刊基本必带。
- ❌ 末端样本极少仍画到底，抖动误导 → `xlim` 截断 + risk table 说明。
- ❌ 漏删失标记。
- ❌ 时间单位/标签不清（天？月？年？）。

## 6. 导出

```r
# ggsurvplot 返回的是含多个 ggplot 的列表，用 print 或 arrange 导出
ggsave("km.pdf", print(p), width = 120, height = 130, units = "mm", device = cairo_pdf)
```
见 [[R导出规范]]。

相关：[[KM生存曲线_KaplanMeier]] · [[森林图_ForestPlot]] · [[医学二分类配色]] · [[R导出规范]]
