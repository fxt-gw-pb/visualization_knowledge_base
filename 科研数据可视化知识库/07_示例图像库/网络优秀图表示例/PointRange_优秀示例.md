---
title: PointRange 优秀示例
type: example
status: active
updated: 2026-06-10
tags: [dataviz, example, pointrange, coefficient]
---

# 示例图：点估计 + CI / 系数图

> 关联：[[点估计置信区间图_PointRange]] · [[森林图_ForestPlot]]。

## 示例 1：dotwhisker — 回归系数 dot-and-whisker

### 图像来源
- 原始链接：https://cran.r-project.org/web/packages/dotwhisker/vignettes/dotwhisker-vignette.html
- 来源：dotwhisker 包 vignette（Solt & Hu）
- license：参考链接（代码 MIT）
- 是否仅作参考：是

### 图像特点
- 架构：横向 point-range，点=系数，线=CI，参考线 0，按效应排序
- 配色：单色或按模型
- 值得学习：**多模型系数并列 + 参考线 + 排序** 的清晰表达

### 可迁移规则
- 系数图横向 + 参考线 0 + 排序（[[点估计置信区间图_PointRange]] 发表级模板）。

### 不建议照搬
- 变量极多时需分组/分页。

## 示例 2：from Data to Viz — error bar 反模式提醒

### 图像来源
- 原始链接：https://www.data-to-viz.com/caveat/error_bar.html
- 来源：from Data to Viz
- license：参考链接
- 是否仅作参考：是

### 图像特点
- 提醒误差棒须注明是 SD/SE/CI，否则误导。
- 值得学习：**误差度量必须声明**。

### 可迁移规则
- 图注注明误差类型（[[标签与注释设计]] / [[术语表]]）。

### 不建议照搬
- —

相关：[[点估计置信区间图_PointRange]] · [[森林图_ForestPlot]] · [[图表示例图库索引]]
