---
chart_name: 倾向评分重叠图
chart_name_en: Propensity score overlap
chart_family: 因果推断图
data_type:
  - propensity_score
  - treatment_group
recommended_backend:
  r: ggplot2
  python: matplotlib
difficulty: basic
priority: high
status: tested
tags:
  - dataviz
  - chart
  - propensity-score
  - overlap
  - positivity
  - common-support
  - causal-inference
  - rwd
  - r
  - python
---

# 倾向评分重叠图 Propensity score overlap

> 把处理组与对照组的**倾向评分(PS)分布**上下镜像画出来，看两组在多大范围内**有共同支持(common support)**。这是因果推断**正性假设(positivity)**的可视化体检——没有重叠的区域，任何效应估计都是外推。

## 1. 图表定位

回答“**两组的可比个体到底有没有**”。镜像密度（上=treated，下=control）重叠越多越好；某段只有一组 = 该处无反事实，需裁剪或加权处理。

## 2. 适用场景

- PSM/IPTW 前的**正性诊断**（建权重/匹配之前先看这张）。
- 决定共同支持域裁剪范围（trim）。
- 解释为什么某些极端 PS 个体被排除/降权。

## 3. 不适用场景

- 还没估计倾向评分 → 先建 PS 模型。
- 连续处理（非二分类）→ 用广义倾向评分的其他诊断。
- 想看“调整后是否平衡”→ 那是 [[协变量平衡图_LovePlot]] 的事。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| ps | 数值 0–1 | 倾向评分（处理的预测概率） | 必需 |
| treat | 二分类 | 处理(1)/对照(0) | 必需 |

PS 由 `treat ~ 协变量` 的 logistic（或机器学习）模型预测得到。

## 5. 图表架构选择

### 5.1 基础架构
- x=PS（0–1）；上半=treated 密度，下半=control 镜像密度；中线 y=0。
- 也可用背靠背直方图（mirror histogram）。

### 5.2 高质量架构
- 标出共同支持域边界（两组都非零的区间），阴影非重叠区。
- IPTW 场景可叠加“加权后”分布看是否拉近。
- y 轴无实际刻度意义（密度对称），可隐藏。

## 6. 配色选择

### 6.1 默认配色
treated 用 `med_treat_control` 的 treat 绿，control 用 control 灰；见 [[医学二分类配色]]。

### 6.2 色盲友好配色
两组用 Okabe-Ito 蓝/橙 + 透明度；中线黑。

### 6.3 医学研究推荐配色
全文统一“处理彩、对照灰”，与 KM/森林图同一套组别色。

## 7. R 实现方案

### 7.1 推荐包
`cobalt::bal.plot(..., var.name="distance")` 或 ggplot 手绘 `density()`。

### 7.2 关键参数
`density(ps, from=0, to=1)` 取两组，control 的 y 取负 → `geom_area(aes(fill=grp))` + `geom_hline(0)`。

### 7.3 可执行模板
**`templates/r/psoverlap.R`**。换数据：`ps_t/ps_c` 改为 `predict(ps_model, type="response")` 按组拆分。

## 8. Python 实现方案

### 8.1 推荐包
matplotlib + `scipy.stats.gaussian_kde`（或 seaborn kdeplot）。

### 8.2 关键参数
`gaussian_kde` 在 0–1 网格求密度；`fill_between(grid, 0, dt)` 与 `fill_between(grid, 0, -dc)`。

### 8.3 可执行模板
**`templates/python/psoverlap.py`**。换真实数据：`ps = model.predict_proba(X)[:,1]`，按 `treat` 拆分。

## 9. 示例图像

### 9.1 网络优秀示例
参考 `cobalt::bal.plot` 与 `twang` 文档的 PS 重叠图。

### 9.2 本库模板 demo（合成数据，双后端对齐）
Python（matplotlib）：

![[tpl_psoverlap_py.png]]

R（ggplot2）：

![[tpl_psoverlap_r.png]]

> 两组在中段(0.3–0.8)重叠充分；两端略偏（treated 偏高、control 偏低）属正常——共同支持域覆盖了主体，正性基本满足；双后端一致。

## 10. 常见错误
- 不看重叠就直接匹配/加权——非重叠区会产生巨大权重/外推。
- 把“分布不同”误当“没有重叠”：两组分布本就该不同（否则无混杂），关键看**有没有共同区间**。
- IPTW 时忽略极端 PS（→极端权重），不做 trim/truncation。
- y 轴标出密度数值，误导读者去比较高度。

## 11. 自动返修规则
- 检测到某段仅单组非零 → 标注非重叠区并提示 trim。
- PS 接近 0/1 堆积 → 提示正性风险 + 权重截断。
- 未画中线 → 自动补 y=0 分隔线。

## 12. 与其他图表的关系
- 与 [[协变量平衡图_LovePlot]] 组成因果前置“正性 + 可比性”双证：先这张证重叠，再 Love plot 证平衡。
- 与 [[缺失数据图_Missingness]]：PS 模型协变量缺失会扭曲评分，先处理缺失。
- 后续效应见 [[森林图_ForestPlot]] / 加权 [[KM生存曲线_KaplanMeier]]。

## 13. 质量检查清单
- [ ] 两组 PS 分布都画了？
- [ ] 标出/说明了共同支持域？
- [ ] 处理了极端 PS（trim/截断）并说明？
- [ ] 组别配色与全文一致？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-14 | v0.1 | 建卡 + 双后端可执行模板（KDE 镜像密度）+ demo 图，状态 tested | 未叠加加权后分布 | 加 IPTW 前后对比 + 共同支持域阴影 |

相关：[[协变量平衡图_LovePlot]] · [[限制性立方样条_RCS]] · [[森林图_ForestPlot]] · [[密度图_Density]]
