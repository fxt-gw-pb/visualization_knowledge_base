---
chart_name: 列线图
chart_name_en: Nomogram
chart_family: 模型结果图
data_type:
  - model_coefficients
  - predictor_ranges
recommended_backend:
  r: ggplot2
  python: matplotlib
difficulty: advanced
priority: high
status: tested
tags:
  - dataviz
  - chart
  - nomogram
  - prediction-model
  - risk-score
  - clinical-prediction
  - r
  - python
---

# 列线图 Nomogram

> 把一个**多变量预测模型**（logistic/Cox）变成可手算的图形评分尺：每个预测因子一条标尺→读出“点数”→所有点数相加→在“总点数”尺对到“预测风险”。临床预测模型论文（尤其中文临床研究）的高频呈现方式。

## 1. 图表定位

回答“**给定这个病人的各项指标，他的预测风险是多少**”——把回归方程翻译成临床医生不用计算器也能用的评分工具。本质是模型系数的图形化。

## 2. 适用场景

- 已建好的临床预测/预后模型(logistic/Cox)的**结果呈现**。
- 个体化风险沟通、床旁决策辅助。
- 与校准/区分度评价一起报（模型“准不准”另说）。

## 3. 不适用场景

- 模型未经验证（区分/校准差）→ 先别做漂亮 nomogram。
- 预测因子过多(>8–10) → 图过宽难用，考虑简化或在线计算器。
- 纯机器学习黑箱模型 → 无线性可加结构，用 [[特征重要性图_FeatureImportance]]/SHAP。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| predictor | 文本 | 预测因子名 | 必需 |
| beta | 数值 | 该因子的模型系数(log OR/HR) | 必需 |
| range | 数值区间 | 因子取值范围(定刻度) | 必需 |
| intercept | 数值 | 模型截距(算风险尺) | 必需 |

点数标度：贡献范围(|β|×range)最大的因子映射到 0–100 分；总点数→线性预测子→`risk = 1/(1+e^−lp)`。

## 5. 图表架构选择

### 5.1 基础架构
- 顶部“Points 0–100”标尺；每个因子一条标尺(刻度=因子取值，位置=对应点数)；底部“Total Points”与“Predicted risk”两条标尺。

### 5.2 高质量架构
- 风险尺只标可达区间的概率(如 0.1–0.9)；点数刻度对齐、字号统一。
- Cox 版可加多个时间点风险尺(1 年/3 年生存)。
- 各因子按贡献大小排序，重要的在上。

## 6. 配色选择

### 6.1 默认配色
预测因子标尺用 `med_case_control` low 蓝(突出可调输入)，Points/Total/Risk 标尺用黑(框架)。见 [[模型效应方向配色]]。

### 6.2 色盲友好配色
靠“蓝=输入因子、黑=刻度框架”的明度区分即可，不依赖红绿。

### 6.3 医学研究推荐配色
传统 nomogram 多为纯黑；本库用蓝标输入轴增强可读，投稿可改黑。

## 7. R 实现方案

### 7.1 推荐包
`rms`（`lrm/cph` + `nomogram()` + `plot()` 最标准）；本机无 rms → 由系数手算点数标度 + ggplot `geom_segment/geom_text` 手绘。

### 7.2 关键参数
`scale=100/max(|β|×range)`；各因子刻度位置 `=scale×(β×x−min)`；风险尺 `total=scale×(logit(r)−intercept−Σlo)`。

### 7.3 可执行模板
**`templates/r/nomogram.R`**（手绘，免 rms）。换数据：`preds`(name/beta/xmin/xmax/ticks) + `INTERCEPT`，由 `glm` 系数填入。

## 8. Python 实现方案

### 8.1 推荐包
matplotlib（手绘多标尺）；`PyNomogram` 等小众包可选。

### 8.2 关键参数
同标度公式；归一化到 [0,1] 画各标尺；风险尺把目标概率反解为总点数定位。

### 8.3 可执行模板
**`templates/python/nomogram.py`**。换真实数据改 `preds` 与 `INTERCEPT`（来自 `statsmodels`/`sklearn` logistic 系数）。

## 9. 示例图像

### 9.1 网络优秀示例
参考 `rms::nomogram` 文档与肿瘤/心血管预测模型论文常见 nomogram。

### 9.2 本库模板 demo（合成模型，双后端对齐）
Python（matplotlib）：

![[tpl_nomogram_py.png]]

R（ggplot2）：

![[tpl_nomogram_r.png]]

> 4 因子 logistic 模型：年龄贡献范围最大(0–100 分)，吸烟/高血压各约 13/12 分；总点数 0–254 对应风险约 0.1–0.9；双后端刻度一致。

## 10. 常见错误
- 未经验证就出 nomogram（区分/校准没报）。
- 连续变量未按真实非线性(若模型含样条)定刻度，导致读数错。
- 点数标度算错(没把最大贡献因子定为 100)。
- 风险尺标到不可达区间，误导。
- 把 nomogram 当“模型很好”的证据——它只是呈现，不是评价。

## 11. 自动返修规则
- 缺校准/区分度引用 → 提示先报模型评价(见 06 族)。
- 风险尺超出可达范围 → 自动裁到实际区间。
- 因子过多 → 提示简化或改在线计算器。
- 点数标度异常 → 重算 `scale=100/max(贡献范围)`。

## 12. 与其他图表的关系
- 必须搭配 [[校准曲线_Calibration]] + [[ROC曲线_ROC]] + [[决策曲线_DCA]]（呈现 vs 评价）。
- 是 [[森林图_ForestPlot]]/系数的另一种呈现(图形评分而非 OR 并列)。
- 黑箱模型用 [[特征重要性图_FeatureImportance]] 替代。

## 13. 质量检查清单
- [ ] 模型已验证(区分/校准已报)？
- [ ] 点数标度正确(最大贡献=100)？
- [ ] 风险尺只在可达区间标刻度？
- [ ] 连续变量刻度与模型形式一致(线性/样条)？
- [ ] 注明这是“呈现”而非性能证据？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-14 | v0.1 | 建卡 + 双后端可执行模板（手算点数标度，免 rms）+ demo 图，状态 tested | 仅线性项、单风险尺 | 加样条因子刻度 + Cox 多时间点(1/3 年)风险尺 |

相关：[[校准曲线_Calibration]] · [[ROC曲线_ROC]] · [[决策曲线_DCA]] · [[森林图_ForestPlot]] · [[特征重要性图_FeatureImportance]]
