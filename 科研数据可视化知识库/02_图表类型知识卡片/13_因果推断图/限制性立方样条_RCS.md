---
chart_name: 限制性立方样条剂量反应
chart_name_en: Restricted cubic spline (RCS) dose-response
chart_family: 因果推断图
data_type:
  - continuous_exposure
  - binary_or_survival_outcome
recommended_backend:
  r: ggplot2
  python: matplotlib
difficulty: advanced
priority: high
status: tested
tags:
  - dataviz
  - chart
  - rcs
  - spline
  - dose-response
  - nonlinear
  - causal-inference
  - epidemiology
  - r
  - python
---

# 限制性立方样条剂量反应 Restricted cubic spline (RCS)

> 用限制性立方样条把**连续暴露**与结局的关系画成**平滑曲线 + 95%CI 带**，不强行假设线性。回答“剂量–反应到底是什么形状”——J 形、U 形、阈值还是单调，是临床流行病学/RWD 关联分析的核心图。

## 1. 图表定位

回答“**暴露每变化一点，风险怎么变**，且这种变化是不是线性”。y 通常是相对某参考点的 OR/HR（参考点处=1），曲线偏离水平线即非线性效应。

## 2. 适用场景

- 连续暴露（BMI、血压、血糖、剂量、生物标志物）与二分类/生存结局的**非线性关联**。
- 检验/展示阈值效应、J/U 形（如 BMI 与死亡）。
- 确定“最优区间”或拐点，支持临床切点讨论。

## 3. 不适用场景

- 暴露本就分类/有序少水平 → 直接分组比较或 [[森林图_ForestPlot]]。
- 样本量很小 → 样条易过拟合，改用线性或分段。
- 只关心单一线性效应 → 线性项 + [[森林图_ForestPlot]] 足够。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| exposure | 连续 | 连续暴露/剂量 | 必需 |
| outcome | 二分类/生存 | 结局（logistic 用 0/1；Cox 用 time+event） | 必需 |
| covariates | 任意 | 需调整的混杂 | 推荐 |

节点(knots)惯例：4 个节点放在 5/35/65/95 百分位（Harrell）；3–5 个节点最常用。

## 5. 图表架构选择

### 5.1 基础架构
- x=暴露；y=OR/HR（相对参考点）；样条拟合线 + 95%CI 带。
- y=1 水平参考线；参考点处加竖线（该点 OR=1）。

### 5.2 高质量架构
- 底部叠加暴露的分布（rug/直方图），提示数据稀疏区（曲线两端 CI 宽要慎读）。
- 标注**非线性检验 p**（样条非线性项整体检验）与总体关联 p。
- x 轴裁到 1–99 百分位，避免极端值把曲线拉飞。

## 6. 配色选择

### 6.1 默认配色
拟合线用 `med_case_control` low 蓝，CI 带同色低透明；参考线灰。见 [[连续变量配色]]。

### 6.2 色盲友好配色
线/带单色 + 灰参考线即可（无需分类色）；多曲线对比才用 Okabe-Ito。

### 6.3 医学研究推荐配色
单暴露单色实线 + 半透明 CI 带；分组（如按性别）再用分类色。

## 7. R 实现方案

### 7.1 推荐包
`rms`（`rcs()` + `Predict()` 最标准）；本机无 rms → base `splines::ns()` + `glm`/`coxph`，相对参考点手算对比的 OR + CI。

### 7.2 关键参数
`glm(y ~ ns(x, knots=ik, Boundary.knots=bk))`；用 `model.matrix` 构造网格与参考点的对比，`vcov()` 求 CI。非线性检验 = 比较含/不含样条高阶项的模型。

### 7.3 可执行模板
**`templates/r/rcs.R`**（`ns` + `glm`，相对参考点求 OR）。换数据：`x/y` 改真实暴露/结局；Cox 把 `glm` 换 `coxph` 同法取 HR。

## 8. Python 实现方案

### 8.1 推荐包
`statsmodels` GLM + `patsy`（`cr()`）或自写 Harrell RCS 基；Cox 用 `lifelines`。

### 8.2 关键参数
自写 `rcs_basis(x, knots)`（k 节点→k−1 列）→ `sm.GLM(Binomial)`；网格设计矩阵减参考点设计矩阵得对比，`cov_params()` 经 delta 法求 CI。

### 8.3 可执行模板
**`templates/python/rcs.py`**（手写 RCS 基 + statsmodels，参考点 OR=1）。换真实数据改 `x/y` 与 `KNOT_Q`、`REF`。

## 9. 示例图像

### 9.1 网络优秀示例
参考 `rms`/`rcssci` 文档与心血管流行病学常见 J 形 BMI–死亡曲线。

### 9.2 本库模板 demo（合成数据，双后端对齐）
Python（matplotlib）：

![[tpl_rcs_py.png]]

R（ggplot2）：

![[tpl_rcs_r.png]]

> 合成的 J 形关系被还原：暴露低端 OR 高、中段最低（参考点附近 OR≈1）、高端回升；两端 CI 带变宽（数据稀疏）；双后端一致。

## 10. 常见错误
- 节点过多 → 过拟合、曲线抖动；3–5 个足够。
- 不设参考点或参考点随意 → OR 解读混乱（应取中位数或临床有意义值）。
- 忽视两端 CI 极宽（数据稀疏）仍下结论。
- 不报非线性检验 p，读者无法判断“样条是否必要”。
- x 不裁极端值，曲线被离群值主导。

## 11. 自动返修规则
- 节点数 >5 → 提示降到 3–5。
- 缺参考线/参考点竖线 → 自动补 y=1 与参考点。
- 两端 CI 过宽 → 自动裁 x 到 1–99 百分位 + 提示。
- 缺非线性检验 → 提示补整体非线性 p。

## 12. 与其他图表的关系
- 与 [[森林图_ForestPlot]] 互补：森林图给“整体一个 OR”，RCS 给“沿暴露变化的形状”。
- 与 [[散点图_Scatter]]：散点看原始联动，RCS 给调整后的模型化曲线。
- 因果场景里常在 PS 调整后人群上再做 RCS（先 [[协变量平衡图_LovePlot]] 证平衡）。

## 13. 质量检查清单
- [ ] 节点数与位置交代（3–5，分位）？
- [ ] 参考点明确且有 y=1 参考线？
- [ ] 报了非线性检验 p？
- [ ] x 裁到合理范围、提示稀疏端？
- [ ] 调整了关键混杂？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-14 | v0.1 | 建卡 + 双后端可执行模板（手写 RCS 基 / ns+glm，相对参考点 OR+CI）+ demo 图，状态 tested | 未叠加分布 rug、未输出非线性 p | 加底部 rug + 非线性检验 p 注释 + Cox(HR) 变体 |

相关：[[森林图_ForestPlot]] · [[协变量平衡图_LovePlot]] · [[散点图_Scatter]] · [[KM生存曲线_KaplanMeier]]
