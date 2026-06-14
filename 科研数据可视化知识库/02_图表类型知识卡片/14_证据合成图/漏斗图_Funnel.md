---
chart_name: 漏斗图
chart_name_en: Funnel plot
chart_family: 证据合成图
data_type:
  - study_effect
  - study_precision
recommended_backend:
  r: ggplot2
  python: matplotlib
difficulty: basic
priority: medium
status: tested
tags:
  - dataviz
  - chart
  - funnel-plot
  - publication-bias
  - small-study-effect
  - meta-analysis
  - evidence-synthesis
  - r
  - python
---

# 漏斗图 Funnel plot

> 把每项研究的**效应量**对其**精度(标准误)**散点，理论上应呈对称倒漏斗。**不对称**提示**发表偏倚 / 小研究效应**——小而结果“漂亮”的研究更容易被发表，会把合并效应往一边拉。

## 1. 图表定位

回答“**这堆证据有没有被选择性发表扭曲**”。大研究(小 SE)聚在顶端靠近合并线，小研究(大 SE)在底部散开；底部一侧空缺 = 不对称 = 警惕偏倚。

## 2. 适用场景

- 荟萃分析的**发表偏倚诊断**（研究数≥10 时推荐）。
- 配合 Egger/Begg 检验做定量不对称判断。
- 识别异常离群研究。

## 3. 不适用场景

- 研究数 <10 → 检验力太低，不宜下结论。
- 异质性极大 → 漏斗不对称可能是异质性而非偏倚，解释要谨慎。
- 只有合并结论需求 → 用 [[Meta森林图_MetaForest]]。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| effect | 数值 | 各研究效应量（通常 log OR/RR/HR） | 必需 |
| se | 数值>0 | 该效应的标准误 | 必需 |

y 轴用 SE（越小越精确，放顶部）；合并效应 `μ = Σ(w·y)/Σw`，`w=1/SE²`。

## 5. 图表架构选择

### 5.1 基础架构
- x=效应量(log)；y=SE（**反向**，0 在上）；散点=各研究。
- 合并效应竖线 + 伪 95% 置信漏斗（`μ ± 1.96·SE` 两条斜线）。

### 5.2 高质量架构
- 漏斗内外点区分（落在漏斗外=异常）。
- 角注报 Egger 检验 p。
- 可叠加 trim-and-fill 补充的“缺失研究”点。

## 6. 配色选择

### 6.1 默认配色
研究点用 `med_case_control` low 蓝；漏斗线/合并线灰。见 [[连续变量配色]]。

### 6.2 色盲友好配色
单色点 + 灰漏斗即可；trim-fill 补点用空心区分。

### 6.3 医学研究推荐配色
黑/蓝点 + 灰虚线漏斗，简洁为主。

## 7. R 实现方案

### 7.1 推荐包
`meta::funnel()` / `metafor::funnel()`（+ `regtest` 做 Egger）；本机无 → ggplot 手绘。

### 7.2 关键参数
`scale_y_reverse()`；漏斗线 `μ±1.96·se_grid`；`geom_point` 研究、`geom_vline(μ)`。

### 7.3 可执行模板
**`templates/r/funnel.R`**（手绘漏斗 + 合并线，免 meta/metafor）。换数据：`yi/sei` 改真实 log 效应与 SE。

## 8. Python 实现方案

### 8.1 推荐包
matplotlib（手绘）；不对称检验可用 `statsmodels` 做 Egger 回归。

### 8.2 关键参数
`ax.set_ylim(se_max, 0)`（反向）；两条 `μ±1.96·se_grid` 漏斗线 + `axvline(μ)`。

### 8.3 可执行模板
**`templates/python/funnel.py`**。换真实数据改 `yi/sei`。

## 9. 示例图像

### 9.1 网络优秀示例
参考 `metafor::funnel` 文档与 Cochrane Handbook 漏斗图章节。

### 9.2 本库模板 demo（合成数据，双后端对齐）
Python（matplotlib）：

![[tpl_funnel_py.png]]

R（ggplot2）：

![[tpl_funnel_r.png]]

> 各研究大致对称地散布在合并线两侧、落在伪 95% 漏斗内 → 无明显发表偏倚迹象（此为对称合成数据）；双后端一致。

## 10. 常见错误
- 研究数太少(<10)仍判“无偏倚”——检验力不足。
- 把异质性导致的不对称误读成发表偏倚。
- y 轴没反向（精确研究应在顶部）。
- 漏斗线用错（应以合并效应为中心，而非 0）。
- 只看图不做 Egger/Begg 定量检验。

## 11. 自动返修规则
- 研究数 <10 → 提示检验力不足、慎下结论。
- y 轴未反向 → 自动 `reverse`。
- 缺漏斗参考线/合并线 → 自动补。
- 检测到强异质性 → 提示不对称可能源于异质性。

## 12. 与其他图表的关系
- 与 [[Meta森林图_MetaForest]] 标配配套：森林给结论、漏斗查偏倚。
- 与 [[散点图_Scatter]] 同为散点，但坐标语义特殊(效应 vs 精度、y 反向)。

## 13. 质量检查清单
- [ ] 研究数≥10 再下偏倚结论？
- [ ] y 轴(SE)反向、精确研究在上？
- [ ] 合并线 + 伪 95% 漏斗都画了？
- [ ] 配了 Egger/Begg 定量检验？
- [ ] 区分了偏倚 vs 异质性的解释？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-14 | v0.1 | 建卡 + 双后端可执行模板（手绘漏斗 + 合并线）+ demo 图，状态 tested | 未叠加 Egger p / trim-fill | 加 Egger 回归注释 + trim-and-fill 补点 |

相关：[[Meta森林图_MetaForest]] · [[森林图_ForestPlot]] · [[散点图_Scatter]]
