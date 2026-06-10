---
title: Scatter 优秀示例
type: example
status: active
updated: 2026-06-10
tags: [dataviz, example, scatter]
---

# 示例图：散点图 Scatter

> 关联：[[散点图_Scatter]]。只记链接 + 设计点。

## 示例 1：seaborn — jointplot（散点 + 边缘分布）

### 图像来源
- 原始链接：https://seaborn.pydata.org/examples/scatterplot_matrix.html ；jointplot：https://seaborn.pydata.org/generated/seaborn.jointplot.html
- 来源：seaborn 官方 gallery
- license：BSD-3（代码可用）
- 是否可下载保存：示例图可（开源），但默认按参考链接
- 是否仅作参考：可下载/参考皆可

### 图像特点
- 架构：中心散点 + 上/右边缘分布（hist/kde）
- 配色：分组 hue，半透明点防重叠
- 坐标轴：带量纲
- 值得学习：**边缘分布**让散点同时显示二维关系与各自一维分布

### 可迁移规则
- 重叠不严重时加 marginal hist/density（`ggMarginal` / `jointplot`）。
- 重叠严重改 `kind="hex"`。

### 不建议照搬
- 默认 tab10 配色非全色盲安全，换 Okabe-Ito。

## 示例 2：Python Graph Gallery — Hexbin / 2D density

### 图像来源
- 原始链接：https://python-graph-gallery.com/2d-density-plot/
- 来源：Python Graph Gallery
- license：参考链接
- 是否仅作参考：是

### 图像特点
- 用 hexbin / 2D KDE 解决大数据散点 overplotting。
- 值得学习：**点很多时用密度而非散点**。

### 可迁移规则
- overplotting → alpha/hexbin/2D density（写入 [[散点图_Scatter]] 返修）。

### 不建议照搬
- 小样本用 hexbin 反而丢信息，仍用散点。

## 已下载参考图（开源许可，可本地查看）

> 下载 2026-06-10，存 `参考图例_开源/`，均 seaborn BSD-3-Clause。

**散点 + 边缘回归分布**（源 https://seaborn.pydata.org/examples/regression_marginals.html ）

![[ref_seaborn_scatter_marginals.png]]
- 学习点：中心散点 + 上/右**边缘分布**，同时显示二维关系与各自一维分布。

**散点矩阵 pairplot**（源 https://seaborn.pydata.org/examples/scatterplot_matrix.html ）

![[ref_seaborn_scatter_matrix.png]]
- 学习点：多变量两两关系一屏看尽，对角线放单变量分布。

相关：[[散点图_Scatter]] · [[热图_Heatmap]] · [[图表示例图库索引]]
