---
title: Boxplot 优秀示例
type: example
status: active
updated: 2026-06-10
tags: [dataviz, example, boxplot]
---

# 示例图：箱线图 Boxplot

> 关联知识卡片：[[箱线图_Boxplot]]。本页登记 ≥2 个网络优秀示例（只记链接 + 提炼设计点，不擅自下载受限图片，见 [[资源评价标准]]）。

## 示例 1：R Graph Gallery — Boxplot with jitter

### 图像来源
- 原始链接：https://r-graph-gallery.com/89-box-and-scatter-plot-with-ggplot2.html
- 来源：R Graph Gallery（Yan Holtz）
- 作者/机构：R Graph Gallery
- license：示例代码可学习（注明出处）；图为生成示例
- 是否可下载保存：否（按参考链接处理）
- 是否仅作参考链接：是

### 图像特点
- 图表架构：boxplot + jitter 原始点叠加，隐藏箱体离群点避免重复
- 配色：克制，分组浅填充
- 字体：无衬线
- 坐标轴：y 连续带边距，x 分类
- 图例：少组时省略
- 注释：无冗余
- 值得学习：**叠原始点透明化**是小样本箱线的标准做法

### 可迁移规则
- 小样本必叠 jitter/beeswarm（写进 [[箱线图_Boxplot]] 返修规则）。
- `outlier.shape=NA` + 叠点，避免离群点画两遍。

### 不建议照搬
- gallery 默认配色未必色盲友好，换 Okabe-Ito（[[分类变量配色]]）。

## 示例 2：from Data to Viz — Boxplot 陷阱页

### 图像来源
- 原始链接：https://www.data-to-viz.com/caveat/boxplot.html
- 来源：from Data to Viz（Holtz & Healy）
- license：参考链接
- 是否仅作参考：是

### 图像特点
- 用动图展示“箱线图隐藏了底层分布”，对比 box vs box+jitter vs violin。
- 值得学习：**箱线图会隐藏多峰/样本量**，需叠点或换 violin/raincloud。

### 可迁移规则
- 收尾质检加一条：箱线是否隐藏了重要分布信息（[[科研图表质量检查清单]]）。

### 不建议照搬
- 动图仅适合网页，论文用静态。

## 已下载参考图（开源许可，可本地查看）

> 下载日期 2026-06-10。许可明确开放，已存 `参考图例_开源/`，可直接复用并署名。

**seaborn — 横向箱线图**（BSD-3-Clause，源 https://seaborn.pydata.org/examples/horizontal_boxplot.html ）

![[ref_seaborn_boxplot.png]]
- 学习点：组别多时**横向 boxplot** + 叠点，正是本卡片返修规则“组>8 改横向”的范式。

**matplotlib — boxplot 解剖示例**（Matplotlib License，源 https://matplotlib.org/stable/gallery/statistics/boxplot_demo.html ）

![[ref_mpl_boxplot.png]]
- 学习点：箱体/须/离群/缺口（notch）各部件的标准画法与含义。

相关：[[箱线图_Boxplot]] · [[小提琴图_Violin]] · [[雨云图_Raincloud]] · [[图表示例图库索引]]
