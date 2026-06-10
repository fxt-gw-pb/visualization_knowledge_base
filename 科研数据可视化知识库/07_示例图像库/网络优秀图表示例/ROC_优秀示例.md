---
title: ROC 优秀示例
type: example
status: active
updated: 2026-06-10
tags: [dataviz, example, roc, auc]
---

# 示例图：ROC 曲线

> 关联：[[ROC曲线_ROC]]。

## 示例 1：scikit-learn — RocCurveDisplay 多模型对比

### 图像来源
- 原始链接：https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
- 来源：scikit-learn 官方 examples
- license：BSD-3（代码/图开源）
- 是否可下载保存：可（开源）
- 是否仅作参考：可参考/下载

### 图像特点
- 架构：多模型 ROC 叠加，正方形，对角参考线，图例标 AUC
- 配色：分模型不同色
- 坐标轴：FPR vs TPR，0–1
- 值得学习：**正方形 + 对角线 + AUC 进图例** 的标准范式；micro/macro 平均

### 可迁移规则
- `set_aspect("equal")` + 对角线 + AUC 标注（[[sklearn模型评价图模板]]）。

### 不建议照搬
- 训练集自评不可取；用测试集。

## 示例 2：pROC — ROC + AUC CI + DeLong

### 图像来源
- 原始链接：https://xrobin.github.io/pROC/
- 来源：pROC 文档（Xavier Robin）
- license：GPL（代码）
- 是否仅作参考：可参考/学习

### 图像特点
- 架构：ROC + 置信带（bootstrap），AUC 95% CI，DeLong 比较两曲线
- 值得学习：**AUC 给 CI**、两模型 AUC 统计比较

### 可迁移规则
- AUC 必给 CI；两模型用 `roc.test`（[[ROC曲线_ROC]] 发表级）。

### 不建议照搬
- —

## 已下载参考图（开源许可，可本地查看）

> 下载 2026-06-10，存 `参考图例_开源/`，scikit-learn BSD-3-Clause。

**ROC 曲线（micro-average OvR + 对角线 + AUC）**（源 https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html ）

![[ref_sklearn_roc.png]]
- 学习点：正方形坐标 + 对角随机线 + 图例标 AUC，多分类用 micro/macro 平均。

**混淆矩阵热图**（源 https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html ）

![[ref_sklearn_confusion.png]]
- 学习点：单色顺序色 + 数值标注；ROC 的同族“某阈值快照”。

相关：[[ROC曲线_ROC]] · [[校准曲线_Calibration]] · [[图表示例图库索引]]
