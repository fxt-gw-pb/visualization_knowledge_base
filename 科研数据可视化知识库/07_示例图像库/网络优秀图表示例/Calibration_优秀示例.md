---
title: Calibration 优秀示例
type: example
status: active
updated: 2026-06-10
tags: [dataviz, example, calibration]
---

# 示例图：校准曲线 Calibration

> 关联：[[校准曲线_Calibration]]。

## 示例 1：scikit-learn — CalibrationDisplay 多模型

### 图像来源
- 原始链接：https://scikit-learn.org/stable/auto_examples/calibration/plot_calibration_curve.html
- 来源：scikit-learn 官方 examples
- license：BSD-3（开源）
- 是否可下载保存：可
- 是否仅作参考：可参考/下载

### 图像特点
- 架构：x 预测概率 vs y 观测频率，对角参考线，多模型对比，**底部叠预测概率直方图**
- 值得学习：**直方图显示概率分布** + 对角线 + 多模型校准对比

### 可迁移规则
- 校准图加 rug/hist 显示分布（[[校准曲线_Calibration]] 发表级）。

### 不建议照搬
- 粗分箱抖动大，论文改 loess。

## 示例 2：rms val.prob（Harrell 范式）

### 图像来源
- 原始链接：https://hbiostat.org/rmsc/ ；包文档 https://cran.r-project.org/package=rms
- 来源：Frank Harrell《Regression Modeling Strategies》/ rms 包
- license：参考链接
- 是否仅作参考：是

### 图像特点
- 架构：loess 平滑校准曲线 + 理想线 + 截距/斜率 + Brier，分布直方
- 值得学习：**平滑校准 + 统计量（截距≈0/斜率≈1/Brier）** 的完整报告

### 可迁移规则
- 报 Brier、校准截距/斜率；平滑优于粗分箱（[[校准曲线_Calibration]]）。

### 不建议照搬
- —

## 已下载参考图（开源许可，可本地查看）

> 下载 2026-06-10，存 `参考图例_开源/`，scikit-learn BSD-3-Clause。

**校准曲线（reliability diagram，多模型对比 + 概率直方）**（源 https://scikit-learn.org/stable/auto_examples/calibration/plot_calibration_curve.html ）

![[ref_sklearn_calibration.png]]
- 学习点：上图预测概率 vs 实际频率 + 对角理想线，下图叠**预测概率直方**显示分布；多模型对比校准好坏。

相关：[[校准曲线_Calibration]] · [[ROC曲线_ROC]] · [[图表示例图库索引]]
