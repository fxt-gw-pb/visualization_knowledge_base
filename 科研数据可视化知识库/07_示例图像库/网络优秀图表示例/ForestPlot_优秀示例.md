---
title: ForestPlot 优秀示例
type: example
status: active
updated: 2026-06-10
tags: [dataviz, example, forestplot]
---

# 示例图：森林图 Forest plot

> 关联：[[森林图_ForestPlot]]。

## 示例 1：forestploter 官方示例

### 图像来源
- 原始链接：https://github.com/adayim/forestploter ；文档 https://adayim.github.io/forestploter/
- 来源：forestploter 包（Alimu Dayimu）
- license：MIT（代码）
- 是否可下载保存：示例图开源；默认参考链接
- 是否仅作参考：可参考/学习

### 图像特点
- 架构：左表（变量 | OR(95%CI) | p）+ 右图（方块 + CI + 参考线 1）严格对齐
- 配色：黑/灰为主，可按方向着色
- 坐标轴：log 比值轴，刻度真实值
- 值得学习：**表与图像素级对齐**、参考线、方块大小编码精度

### 可迁移规则
- 用占位列对齐表图；比值类 log 轴 + 参考线 1（[[forestplot森林图模板]]）。

### 不建议照搬
- 列内容按研究定制。

## 示例 2：Cochrane / meta 森林图范式

### 图像来源
- 原始链接：https://training.cochrane.org/handbook （Cochrane Handbook, 森林图章节）
- 来源：Cochrane Collaboration
- license：参考链接（受版权，仅记链接）
- 是否仅作参考：是

### 图像特点
- 架构：各研究效应 + 权重方块 + 合并效应菱形 + 异质性 I²
- 值得学习：**meta 分析的菱形合并效应 + 权重编码 + 异质性标注**

### 可迁移规则
- meta 森林图加菱形合并效应与 I² 标注（未来 meta 卡片）。

### 不建议照搬
- Cochrane 图片受版权，不下载。

相关：[[森林图_ForestPlot]] · [[模型效应方向配色]] · [[图表示例图库索引]]
