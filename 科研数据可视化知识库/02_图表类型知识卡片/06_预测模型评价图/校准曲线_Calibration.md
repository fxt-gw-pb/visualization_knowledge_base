---
chart_name: 校准曲线
chart_name_en: Calibration curve
chart_family: 预测模型评价图
data_type:
  - predicted_probability
  - binary_outcome
recommended_backend:
  r: rms
  python: scikit-learn
difficulty: intermediate
priority: high
status: tested
tags:
  - dataviz
  - chart
  - calibration
  - model-evaluation
  - r
  - python
---

# 校准曲线 Calibration curve

> 检验“预测概率”与“实际发生频率”是否一致。ROC 看**区分**，校准看**概率准不准**——临床预测模型两者都要报。

## 1. 图表定位

回答“**模型说的 30% 风险，真实里是不是大约 30% 发生**”。x = 预测概率，y = 实际频率，理想是 45° 对角线。

## 2. 适用场景

- 临床/风险预测模型（输出概率而非仅排序）。
- 与 ROC 配套报告（判别 + 校准）。
- 比较多模型校准好坏。
- 报 Brier score、校准截距/斜率。

## 3. 不适用场景

- 只关心排序/判别 → [[ROC曲线_ROC]] 足够。
- 模型只输出类别不输出概率 → 无法校准评估。
- 样本太小 → 分箱/平滑都不稳。
- 概率未经验证集评估 → 别在训练集谈校准。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 必需 |
|---|---|---|---|
| y_true | binary | 真实标签 0/1 | 必需 |
| y_prob | continuous[0,1] | 预测概率 | 必需 |
| model | categorical | 多模型 | 可选 |

用 hold-out/CV 概率。

## 5. 图表架构选择

### 5.1 基础架构
- x = 预测概率，y = 观测频率；
- 对角参考线（完美校准）；
- 分箱点（等宽或等频）或平滑曲线；
- 底部叠预测概率的直方图/rug（显示分布密度）。

### 5.2 高质量架构
- **loess/样条平滑校准曲线**优于粗分箱（分箱抖动大）。
- 标 Brier score、校准截距(≈0)/斜率(≈1)。
- 多模型对比 + 图例。
- rug/hist 显示各区间样本量（尾部稀疏要谨慎）。

## 6. 配色选择
- 单模型单色 + 灰对角线；
- 多模型 Okabe-Ito + 线型（[[分类变量配色]]）。

## 7. R 实现方案

### 7.1 推荐包
rms（`val.prob`、`calibrate`）、CalibrationCurves、ggplot2

### 7.2 关键参数
`rms::val.prob(p, y)` 给校准图 + 统计量；`lrm(...) |> calibrate()` 用 bootstrap 校正。

### 7.3 基础代码模板
```r
library(rms)
val.prob(df$prob, df$DEATH)        # 校准曲线 + Brier + 截距/斜率
```

### 7.4 发表级代码模板（loess 平滑 + rug）
```r
library(ggplot2)
df$bin <- cut(df$prob, breaks = quantile(df$prob, 0:10/10), include.lowest = TRUE)
agg <- aggregate(cbind(prob, DEATH) ~ bin, df, mean)
ggplot(df, aes(prob, DEATH)) +
  geom_abline(slope = 1, intercept = 0, linetype = 2, color = "grey60") + # 完美校准
  geom_smooth(method = "loess", se = TRUE, color = "#0072B2") +           # 平滑校准
  geom_point(data = agg, aes(prob, DEATH), color = "#D55E00") +          # 分箱点
  geom_rug(sides = "b", alpha = .1) +                                     # 概率分布
  coord_equal(xlim = c(0,1), ylim = c(0,1)) +
  labs(x = "Predicted probability", y = "Observed frequency") +
  theme_pub()
```

## 8. Python 实现方案

### 8.1 推荐包
scikit-learn（`CalibrationDisplay`、`calibration_curve`、`brier_score_loss`）、matplotlib

### 8.2 关键参数
见 [[sklearn模型评价图模板]]：`CalibrationDisplay.from_predictions(n_bins=, strategy="quantile")`、`calibration_curve()`、`brier_score_loss()`。

### 8.3 基础代码模板
```python
from sklearn.calibration import CalibrationDisplay
fig, ax = plt.subplots(figsize=(3.5,3.5))
CalibrationDisplay.from_predictions(df.DEATH, df.prob, n_bins=10,
                                    strategy="quantile", ax=ax)
ax.plot([0,1],[0,1], ls="--", c="grey"); ax.set_aspect("equal")
```

### 8.4 发表级代码模板（loess + rug + Brier）
```python
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss
import statsmodels.api as sm, numpy as np
prob_true, prob_pred = calibration_curve(df.DEATH, df.prob, n_bins=10, strategy="quantile")
lo = sm.nonparametric.lowess(df.DEATH, df.prob, frac=.6)         # loess 平滑
fig, ax = plt.subplots(figsize=(3.6,3.6))
ax.plot([0,1],[0,1], ls="--", c="grey")
ax.plot(lo[:,0], lo[:,1], color="#0072B2", label="loess")
ax.scatter(prob_pred, prob_true, color="#D55E00", s=15, label="binned")
ax.plot(df.prob, np.full(len(df), -0.02), "|", color="k", alpha=.05)  # rug
ax.set_xlim(0,1); ax.set_ylim(-0.03,1); ax.set_aspect("equal")
ax.set_xlabel("Predicted probability"); ax.set_ylabel("Observed frequency")
ax.text(.05,.9, f"Brier = {brier_score_loss(df.DEATH, df.prob):.3f}", transform=ax.transAxes)
ax.legend(frameon=False)
```

## 9. 示例图像

### 9.1 网络优秀示例
见 [[Calibration_优秀示例]]（含 rms val.prob 范式、带分布直方的校准图）。
本库自制范式图（合成数据，对角线 + 分箱点）：

![[demo_calibration.png]]

### 9.2 Framingham 数据测试示例
✅ 已跑通（logistic 预测 DEATH 的校准曲线：loess + 分箱点 + Brier + 底部概率 rug）。代码见 [[Python测试记录]]。

R（loess + 分箱点 + Brier + rug）：

![[fig_calibration_death_r.png]]

Python（sklearn calibration_curve + statsmodels loess）：

![[fig_calibration_death_py.png]]

> 结论：分箱点贴近对角线、Brier≈0.175，校准尚可。底部 rug 显示预测概率多集中在低区间，高概率端稀疏需谨慎解读。R 与 Python 一致。⚠️ 同数据自评，正式须 hold-out。

## 10. 常见错误
- 只报 ROC 不报校准（判别好≠概率准）。
- 粗分箱导致抖动被当“校准差”。
- 不显示概率分布（尾部稀疏处过度解读）。
- 训练集自评。
- 非正方形坐标。

## 11. 自动返修规则
- 分箱抖动 → 改 loess/样条平滑校准。
- 尾部稀疏 → 加 rug/hist 显示样本量，谨慎解读。
- 缺统计量 → 补 Brier、截距/斜率。
- 校准差 → 提示 Platt scaling / isotonic 重校准。
- 非方形 → `coord_equal`/`set_aspect("equal")`。

## 12. 与其他图表的关系
- vs [[ROC曲线_ROC]]：判别 vs 校准，互补，临床模型两者都报。
- vs 决策曲线（DCA）：DCA 给临床净获益，校准给概率准确性。
- 与混淆矩阵：某阈值下的分类表现。

## 13. 质量检查清单
- [ ] 测试集/CV 概率？
- [ ] 对角参考线 + 正方形？
- [ ] 平滑优于粗分箱（或两者都给）？
- [ ] 显示概率分布（rug/hist）？
- [ ] 报 Brier/截距/斜率？
- [ ] 适合论文导出？

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建立初稿 | 缺实测图 | 跑 DEATH logistic 校准 + Brier |

相关：[[ROC曲线_ROC]] · [[sklearn模型评价图模板]] · [[坐标轴设计]] · [[分类变量配色]]
