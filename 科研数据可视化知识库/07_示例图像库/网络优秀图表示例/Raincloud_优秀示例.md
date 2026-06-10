---
title: Raincloud / Violin 优秀示例
type: example
status: active
updated: 2026-06-10
tags: [dataviz, example, raincloud, violin]
---

# 示例图：雨云图 / 小提琴图

> 关联：[[雨云图_Raincloud]] · [[小提琴图_Violin]]。

## 示例 1：ggdist gallery — raincloud（halfeye + dots + box）

### 图像来源
- 原始链接：https://mjskay.github.io/ggdist/articles/slabinterval.html
- 来源：ggdist 官方文档（Matthew Kay）
- license：MIT（代码）
- 是否可下载保存：示例图开源；默认参考链接
- 是否仅作参考：可参考/学习

### 图像特点
- 架构：半小提琴（云）+ 原始点（雨）+ 区间/箱（伞），横向排列
- 配色：分组半透明，点更透明
- 值得学习：**半 violin 避免对称镜像冗余**；三层信息不打架的偏移设计

### 可迁移规则
- raincloud 用 `stat_halfeye` + `stat_dots` + `geom_boxplot`（写入 [[雨云图_Raincloud]] 模板）。

### 不建议照搬
- 点太多需抽样。

## 示例 2：Raincloud plots 原始论文范式（Allen et al.）

### 图像来源
- 原始链接：https://wellcomeopenresearch.org/articles/4-63 （Allen et al., 2019/2021, "Raincloud plots"）
- 来源：Wellcome Open Research（开放获取）
- license：CC BY（开放）
- 是否可下载保存：可（CC BY，注明来源）
- 是否仅作参考：可下载/参考

### 图像特点
- 提出 raincloud 概念：raw data + 分布 + 概括三合一，透明且美观。
- 值得学习：**透明展示原始数据**的理念，反对只给概括统计。

### 可迁移规则
- 把“显示原始数据”作为分布图的默认偏好（[[科研图表质量检查清单]]）。

### 不建议照搬
- 原文配色随场景调整。

## 已下载参考图（开源许可，可本地查看）

> 下载 2026-06-10，存 `参考图例_开源/`，seaborn BSD-3-Clause。

**split 小提琴图**（源 https://seaborn.pydata.org/examples/grouped_violinplots.html ）

![[ref_seaborn_violin.png]]
- 学习点：`split=True` 把两组密度合到一根 violin 两半，内嵌四分位线；省空间且便于左右对比。

**山峦图 / ridgeline（KDE 堆叠）**（源 https://seaborn.pydata.org/examples/kde_ridgeplot.html ）

![[ref_seaborn_ridgeline.png]]
- 学习点：多组分布用错位堆叠的密度曲线对比，是 violin/raincloud 之外的分布族成员。

相关：[[雨云图_Raincloud]] · [[小提琴图_Violin]] · [[箱线图_Boxplot]] · [[图表示例图库索引]]
