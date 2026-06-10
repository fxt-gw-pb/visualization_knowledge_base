---
title: Line 优秀示例
type: example
status: active
updated: 2026-06-10
tags: [dataviz, example, line, spaghetti]
---

# 示例图：折线趋势图 Line

> 关联：[[折线趋势图_Line]]。

## 示例 1：R Graph Gallery — Spaghetti + 高亮

### 图像来源
- 原始链接：https://r-graph-gallery.com/web-lineplots-and-area-chart-the-economist.html ；spaghetti：https://r-graph-gallery.com/web-line-chart-small-multiple.html
- 来源：R Graph Gallery
- license：参考链接
- 是否仅作参考：是

### 图像特点
- 架构：众多个体线灰化，高亮 1–2 条重点；或 small multiples 分面
- 配色：灰 + 强调色
- 值得学习：**意大利面团 → 高亮 + 灰化 / 分面** 的解法

### 可迁移规则
- 线 > ~8 → 高亮重点 + 灰化其余 / 分面（写入 [[折线趋势图_Line]] 返修）。

### 不建议照搬
- Economist 风主题不适合论文。

## 示例 2：seaborn — lineplot with CI band

### 图像来源
- 原始链接：https://seaborn.pydata.org/generated/seaborn.lineplot.html
- 来源：seaborn 官方
- license：BSD-3
- 是否可下载保存：可（开源）
- 是否仅作参考：可参考/下载

### 图像特点
- 架构：均值线 + 自动 95% CI 带（bootstrap）
- 值得学习：**趋势必带不确定性带**，而非只画均值线

### 可迁移规则
- 组趋势用 `errorbar=("ci",95)` / `mean_cl_normal` ribbon（[[折线趋势图_Line]]）。

### 不建议照搬
- 默认配色换 Okabe-Ito。

## 已下载参考图（开源许可，可本地查看）

> 下载 2026-06-10，存 `参考图例_开源/`，seaborn BSD-3-Clause。

**多组折线 + 误差带**（源 https://seaborn.pydata.org/examples/errorband_lineplots.html ）

![[ref_seaborn_line.png]]
- 学习点：每组均值线 + 半透明 95% CI 误差带，正是“趋势必带不确定性带”的范式。

相关：[[折线趋势图_Line]] · [[点估计置信区间图_PointRange]] · [[图表示例图库索引]]
