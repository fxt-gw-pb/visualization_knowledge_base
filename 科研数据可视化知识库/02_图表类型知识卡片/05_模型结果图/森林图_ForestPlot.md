---
chart_name: 森林图
chart_name_en: Forest plot
chart_family: 模型结果图
data_type:
  - estimate_ci
  - categorical_term
recommended_backend:
  r: forestploter
  python: matplotlib
difficulty: intermediate
priority: high
status: tested
tags:
  - dataviz
  - chart
  - forestplot
  - odds-ratio
  - hazard-ratio
  - model
  - r
  - python
---

# 森林图 Forest plot

> 把回归模型的多项效应（OR/HR/RR/β）连同 CI 排成一列，左侧配表（变量名/估计值/CI/p），右侧画点 + 区间 + 参考线。医学论文 Table 2/模型结果的标准呈现，也是 meta 分析主图。

## 1. 图表定位

回答“**模型里每个变量的效应有多大、方向如何、是否显著**”，并让多个效应在同一参考线下可比。

## 2. 适用场景

- logistic 回归 OR、Cox 回归 HR、线性回归 β 的多变量并列。
- 亚组分析（各亚组效应 + 交互）。
- meta 分析（各研究效应 + 合并效应菱形）。
- 需要“表 + 图”对齐呈现。

## 3. 不适用场景

- 只有一个效应 → 一句话/一个数即可。
- 想看预测性能 → [[ROC曲线_ROC]] / [[校准曲线_Calibration]]。
- 想看连续效应曲线（非线性）→ 边际效应图。
- 变量极多（几十项）→ 分组/分页/精选。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 必需 |
|---|---|---|---|
| term | categorical | 变量名/标签 | 必需 |
| estimate | continuous | 效应（OR/HR/RR/β）| 必需 |
| conf.low / conf.high | continuous | CI | 必需 |
| p.value | continuous | p 值（可选展示）| 可选 |
| group | categorical | 亚组/分块小标题 | 可选 |

由 `broom::tidy(model, exponentiate=TRUE, conf.int=TRUE)`（R）或 statsmodels/lifelines 汇总得到。

## 5. 图表架构选择

### 5.1 基础架构
- 行 = 变量；x = 效应值；
- 几何 = point（方块大小可∝权重/精度）+ CI 横线；
- **参考线**：比值类（OR/HR/RR）= 1，差值/β = 0；
- 比值类用 **log 轴**（视觉对称）。

### 5.2 高质量架构
- 左表对齐：term | OR (95% CI) | p；右侧图区。
- 按方向/显著性着色（[[模型效应方向配色]]）。
- 亚组用小标题分块。
- meta：合并效应用菱形，异质性 I² 标注。
- 极宽 CI → 截断轴并标注真实值。

## 6. 配色选择
- 默认单色（黑/深灰）即可；
- 方向语义着色：有害红、保护蓝、跨参考线灰（[[模型效应方向配色]]）。
- 方块大小编码精度时，避免颜色再叠义过载。

## 7. R 实现方案

### 7.1 推荐包
forestploter（推荐）、forestplot、survminer::ggforest（Cox 快速）、broom

### 7.2 关键参数
见 [[forestplot森林图模板]]：`est/lower/upper`、`ref_line`、`x_trans="log"`、`ci_column`、`xlim/ticks_at`。

### 7.3 基础代码模板（Cox 快速）
```r
library(survival); library(survminer)
cox <- coxph(Surv(TIMEDTH, DEATH) ~ AGE_group + SEX + BMI + CURSMOKE + PREVHYP, data = df)
ggforest(cox, data = df)        # HR + CI + p 自动森林图
```

### 7.4 发表级代码模板（forestploter）
```r
library(forestploter); library(broom)
res <- tidy(glm(DEATH ~ AGE_group + SEX + BMI + CURSMOKE + PREVHYP,
                data = df, family = binomial),
            conf.int = TRUE, exponentiate = TRUE)
res <- subset(res, term != "(Intercept)")
res$`OR (95% CI)` <- sprintf("%.2f (%.2f–%.2f)", res$estimate, res$conf.low, res$conf.high)
res$p <- ifelse(res$p.value < .001, "<0.001", sprintf("%.3f", res$p.value))
res$` ` <- paste(rep(" ", 18), collapse = " ")
p <- forest(res[, c("term","OR (95% CI)","p"," ")],
            est = res$estimate, lower = res$conf.low, upper = res$conf.high,
            ci_column = 4, ref_line = 1, xlim = c(.5, 3),
            ticks_at = c(.5, 1, 2, 3))
plot(p)
```

## 8. Python 实现方案

### 8.1 推荐包
matplotlib（手搓最可控）、statsmodels/lifelines（取效应）、forestplot（PyPI 包，可选）

### 8.2 关键参数
`ax.errorbar(est, y, xerr=, fmt="s")`、`ax.axvline(1)`、`ax.set_xscale("log")`、左侧用 `ax.text`/twin 表。

### 8.3 / 8.4 代码模板（手搓发表级）
```python
import numpy as np, matplotlib.pyplot as plt
# res: DataFrame[term, OR, lo, hi, p]
res = res.iloc[::-1].reset_index(drop=True)        # 顶部为第一个变量
y = np.arange(len(res))
fig, ax = plt.subplots(figsize=(5, .4*len(res)+1))
ax.errorbar(res.OR, y, xerr=[res.OR-res.lo, res.hi-res.OR],
            fmt="s", color="#B2182B", capsize=3, ms=5)
ax.axvline(1, ls="--", c="grey")                   # 参考线
ax.set_xscale("log"); ax.set_xticks([.5,1,2,3]); ax.set_xticklabels([.5,1,2,3])
ax.set_yticks(y); ax.set_yticklabels(res.term)
ax.set_xlabel("Odds ratio (95% CI)")
for i,r in res.iterrows():                          # 右侧标注文本
    ax.text(ax.get_xlim()[1]*1.05, i,
            f"{r.OR:.2f} ({r.lo:.2f}–{r.hi:.2f})", va="center", fontsize=7)
fig.savefig("forest.pdf", bbox_inches="tight")
```

## 9. 示例图像

### 9.1 网络优秀示例
见 [[ForestPlot_优秀示例]]（含医学多变量 OR 森林、meta 森林范式）。
本库自制范式图（合成数据，log 轴 + 参考线 1 + 方向着色）：

![[demo_forest.png]]

### 9.2 Framingham 数据测试示例
✅ 已跑通（logistic 预测 DEATH 的多变量 OR 森林图）。代码见 [[R测试记录]] / [[Python测试记录]] 与 [[forestplot森林图模板]]。

R（forestploter，左表右图对齐 + log 轴）：

![[fig_forest_death_or_r.png]]

Python（matplotlib 手搓）：

![[fig_forest_death_or_py.png]]

> 结论：年龄组、高血压、当前吸烟显著**升高**死亡风险；**女性（Female vs male，OR≈0.50）为保护因素**（SEX 编码已确认 0=男/1=女，见 [[变量字典]]）。Age grp 3 的 OR=25.74、CI 极宽超出坐标范围 → 森林图截断 + 表中标真实值，正是本卡片第 11 节返修规则的真实演示。

## 10. 常见错误
- 比值类用线性轴 → OR=0.5 与 2 视觉不对称。
- 缺参考线（1 或 0）。
- 表与图数值不一致。
- 个别极宽 CI 把主体压成一条缝。
- 把 OR 当 RR 解释（罕见结局才近似）。

## 11. 自动返修规则
- 比值类 → log 轴 + 参考线 1。
- 极宽 CI → 截断轴 + 文本标真实区间。
- 变量多 → 亚组分块 / 分页 / 精选。
- 表图错位 → forestploter 占位列对齐 / matplotlib twin 表。
- 方向不直观 → 按 [[模型效应方向配色]] 着色。

## 12. 与其他图表的关系
- vs [[点估计置信区间图_PointRange]]：森林图 = 模型效应版 point-range + 左表 + 参考线。
- vs 系数图（coefficient plot）：本质同类，β 用线性轴 + 参考线 0。
- Cox 森林图与 [[KM生存曲线_KaplanMeier]] 配套呈现生存结果。

## 13. 质量检查清单
- [ ] 比值类 log 轴？
- [ ] 参考线在位？
- [ ] 表与图一致？
- [ ] CI 含义/置信水平注明？
- [ ] 方向着色正确？
- [ ] 适合论文导出？

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建立初稿 | 缺实测图 | 跑 DEATH~多变量 OR/HR 森林 |

相关：[[点估计置信区间图_PointRange]] · [[KM生存曲线_KaplanMeier]] · [[模型效应方向配色]] · [[forestplot森林图模板]] · [[坐标轴设计]]
