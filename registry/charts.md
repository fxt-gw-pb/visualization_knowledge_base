---
title: 图表卡片状态总表（自动生成）
type: index
tags: [dataviz, index, generated]
---

# 图表卡片状态总表（自动生成）

> ⚠️ 本文件由 `scripts/build_registry.py` 从各卡片 frontmatter 生成，**请勿手改**。
> 改了卡片后重跑脚本即可刷新。机器可读版见 `registry/charts.json`。

共 12 张卡片。

## 分布图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[小提琴图_Violin]] | Violin plot | tested | high | ggplot2 | seaborn |
| [[雨云图_Raincloud]] | Raincloud plot | tested | high | ggdist + ggplot2 | matplotlib/ptitprince |

## 多面板组合图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[多面板组合图_MultiPanel]] | Multi-panel figure | tested | high | patchwork/cowplot | matplotlib gridspec |

## 时间趋势图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[折线趋势图_Line]] | Line plot | tested | high | ggplot2 | matplotlib/seaborn |

## 模型结果图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[森林图_ForestPlot]] | Forest plot | tested | high | forestploter | matplotlib |

## 生存分析图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[KM生存曲线_KaplanMeier]] | Kaplan-Meier curve | tested | high | survminer | lifelines |

## 相关性图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[散点图_Scatter]] | Scatter plot | tested | high | ggplot2 | seaborn/matplotlib |

## 组间比较图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[点估计置信区间图_PointRange]] | Point-range plot | tested | high | ggplot2 | matplotlib |
| [[箱线图_Boxplot]] | Boxplot | tested | high | ggplot2 + ggpubr | seaborn |

## 预测模型评价图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[ROC曲线_ROC]] | ROC curve | tested | high | pROC | scikit-learn |
| [[校准曲线_Calibration]] | Calibration curve | tested | high | rms | scikit-learn |

## 高维数据图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[热图_Heatmap]] | Heatmap | tested | high | ComplexHeatmap/pheatmap | seaborn |
