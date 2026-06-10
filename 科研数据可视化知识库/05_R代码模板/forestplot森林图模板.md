---
title: forestplot 森林图模板
type: code-template
status: active
backend: r
updated: 2026-06-10
tags:
  - dataviz
  - r
  - forestplot
  - forestploter
  - template
---

# forestplot 森林图模板

> 森林图 = 左表（变量/估计值/CI/p）+ 右图（点 + 区间 + 参考线）。推荐 **forestploter**（表图对齐更灵活）。配合 [[森林图_ForestPlot]]。

## 1. 从模型取效应值

```r
# logistic → OR
m <- glm(DEATH ~ AGE_group + SEX + BMI + CURSMOKE + PREVHYP,
         data = df, family = binomial)
res <- broom::tidy(m, conf.int = TRUE, exponentiate = TRUE)  # OR + 95%CI
# Cox → HR：broom::tidy(coxph(...), exponentiate = TRUE)
res <- subset(res, term != "(Intercept)")
res$`OR (95% CI)` <- sprintf("%.2f (%.2f–%.2f)", res$estimate, res$conf.low, res$conf.high)
res$p <- ifelse(res$p.value < .001, "<0.001", sprintf("%.3f", res$p.value))
```

## 2. forestploter 出图

```r
library(forestploter); library(grid)

res$` ` <- paste(rep(" ", 20), collapse = " ")   # 占位列 → 画图区
tm <- forest_theme(base_size = 9,
                   ci_pch = 16, ci_col = "#B2182B",
                   refline_col = "grey50")

p <- forest(
  res[, c("term", "OR (95% CI)", "p", " ")],
  est = res$estimate, lower = res$conf.low, upper = res$conf.high,
  ci_column = 4,            # 第 4 列画 CI
  ref_line = 1,             # >>> PARAM 比值类参考线=1（差值类=0）
  xlim = c(0.25, 4),
  ticks_at = c(0.25, 0.5, 1, 2, 4),
  theme = tm
)
plot(p)
```

> 比值类（OR/HR/RR）建议 **log 轴**视觉对称：`forestploter` 用 `x_trans = "log"`（或在 xlim/ticks 上用 log 间隔）。

## 3. 基础 forestplot 包写法（备选）

```r
library(forestplot)
forestplot(labeltext = cbind(res$term, res$`OR (95% CI)`, res$p),
           mean = res$estimate, lower = res$conf.low, upper = res$conf.high,
           xlog = TRUE, zero = 1,                 # log 轴 + 参考线 1
           col = fpColors(box = "#B2182B", line = "grey40"))
```

## 4. 关键参数（旋钮）

| 参数 | 作用 |
|---|---|
| `est/lower/upper` | 点估计与 CI |
| `ref_line` / `zero` | 参考线（OR/HR=1，差值=0）|
| `xlog` / `x_trans="log"` | 比值类对数轴 |
| `ci_column` | CI 画在第几列 |
| `xlim`/`ticks_at` | 轴范围与刻度（处理极宽 CI）|
| 颜色 | 按方向（[[模型效应方向配色]]）|

## 5. 常见错误（→ 返修，见 [[森林图_ForestPlot]]）

- ❌ 比值类用线性轴 → OR=0.5 与 2 不对称，改 log。
- ❌ 缺参考线（1 或 0）。
- ❌ 个别极宽 CI 压扁主体 → 截断坐标轴并标注。
- ❌ 表与图未对齐 → forestploter 占位列对齐。
- ❌ OR/HR/CI 文本与图不一致。

## 6. 导出

```r
ggsave("forest.pdf", plot = p, width = 180, height = 100, units = "mm", device = cairo_pdf)
# forestplot 包：用 grDevices::pdf(...) 包裹 print(p)
```

相关：[[森林图_ForestPlot]] · [[模型效应方向配色]] · [[坐标轴设计]] · [[R导出规范]]
