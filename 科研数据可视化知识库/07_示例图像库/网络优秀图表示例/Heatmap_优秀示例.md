---
title: Heatmap 优秀示例
type: example
status: active
updated: 2026-06-10
tags: [dataviz, example, heatmap]
---

# 示例图：热图 Heatmap

> 关联：[[热图_Heatmap]]。

## 示例 1：ComplexHeatmap 参考手册示例

### 图像来源
- 原始链接：https://jokergoo.github.io/ComplexHeatmap-reference/book/
- 来源：ComplexHeatmap 参考书（Zuguang Gu）
- license：MIT（代码）
- 是否可下载保存：示例图开源；默认参考链接
- 是否仅作参考：可参考/学习

### 图像特点
- 架构：z-score 热图 + 多层顶部/侧边注释条 + 行列聚类 + 按变量拆块
- 配色：发散 RdBu 中心 0；注释条分类色
- 值得学习：**多层注释 + 拆块** 把临床/组学信息和表达矩阵对应起来

### 可迁移规则
- 注释聚类热图用 ComplexHeatmap，z-score + 截断 + 注释条（[[ComplexHeatmap模板]]）。

### 不建议照搬
- 注释复杂度按数据定，别堆砌。

## 示例 2：seaborn — clustermap / 相关矩阵

### 图像来源
- 原始链接：https://seaborn.pydata.org/generated/seaborn.clustermap.html
- 来源：seaborn 官方
- license：BSD-3（开源）
- 是否可下载保存：可
- 是否仅作参考：可参考/下载

### 图像特点
- 架构：聚类热图 + 行/列颜色条；相关矩阵用 RdBu center=0
- 值得学习：**相关矩阵中心对 0 用发散色**；`z_score` 标准化参数

### 可迁移规则
- 相关/ z-score 热图发散色中心 0；离群截断（[[发散变量配色]]）。

### 不建议照搬
- 默认 cmap 若是 rainbow 类，换 viridis/RdBu。

## 已下载参考图（开源许可，可本地查看）

> 下载 2026-06-10，存 `参考图例_开源/`，seaborn BSD-3-Clause。

**相关矩阵热图（发散色中心 0）**（源 https://seaborn.pydata.org/examples/many_pairwise_correlations.html ）

![[ref_seaborn_corr_heatmap.png]]
- 学习点：相关矩阵用**发散色 + center=0**，常只画下三角避免冗余；正是本卡片相关矩阵的范式。

相关：[[热图_Heatmap]] · [[发散变量配色]] · [[ComplexHeatmap模板]] · [[图表示例图库索引]]
