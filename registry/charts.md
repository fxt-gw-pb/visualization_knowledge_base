---
title: 图表卡片状态总表（自动生成）
type: index
tags: [dataviz, index, generated]
---

# 图表卡片状态总表（自动生成）

> ⚠️ 本文件由 `scripts/build_registry.py` 从各卡片 frontmatter 生成，**请勿手改**。
> 改了卡片后重跑脚本即可刷新。机器可读版见 `registry/charts.json`。

共 35 张卡片。

## 分布图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[密度图_Density]] | Density plot | tested | high | ggplot2 | seaborn |
| [[小提琴图_Violin]] | Violin plot | tested | high | ggplot2 | seaborn |
| [[山峦图_Ridgeline]] | Ridgeline plot | tested | medium | ggdist (ggridges 可选) | matplotlib (手搓) |
| [[直方图_Histogram]] | Histogram | tested | high | ggplot2 | seaborn/matplotlib |
| [[雨云图_Raincloud]] | Raincloud plot | tested | high | ggdist + ggplot2 | matplotlib/ptitprince |

## 医学流行病学常用图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[CONSORT流程图_Consort]] | CONSORT flow diagram | tested | high | ggplot2 (手搓) / DiagrammeR | matplotlib (手搓) |
| [[Swimmer图_Swimmer]] | Swimmer plot | tested | medium | ggplot2 | matplotlib |
| [[状态转移图_Alluvial]] | Alluvial / state transition diagram | tested | medium | ggplot2 | matplotlib |

## 因果推断图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[倾向评分重叠图_PSOverlap]] | Propensity score overlap | tested | high | ggplot2 | matplotlib |
| [[协变量平衡图_LovePlot]] | Covariate balance (Love plot) | tested | high | ggplot2 | matplotlib |
| [[限制性立方样条_RCS]] | Restricted cubic spline (RCS) dose-response | tested | high | ggplot2 | matplotlib |

## 多面板组合图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[多面板组合图_MultiPanel]] | Multi-panel figure | tested | high | patchwork/cowplot | matplotlib gridspec |

## 数据质量图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[缺失数据图_Missingness]] | Missing data pattern | tested | high | ggplot2 (naniar/VIM 可选) | matplotlib (missingno 可选) |

## 时间趋势图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[个体轨迹图_Spaghetti]] | Spaghetti plot (individual trajectories) | tested | high | ggplot2 | matplotlib |
| [[折线趋势图_Line]] | Line plot | tested | high | ggplot2 | matplotlib/seaborn |

## 模型结果图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[亚组森林图_Subgroup]] | Subgroup forest plot | tested | high | ggplot2 | matplotlib |
| [[列线图_Nomogram]] | Nomogram | tested | high | ggplot2 | matplotlib |
| [[森林图_ForestPlot]] | Forest plot | tested | high | forestploter | matplotlib |
| [[特征重要性图_FeatureImportance]] | Feature importance / SHAP summary | tested | high | pROC (置换重要性) | shap (beeswarm) |

## 生存分析图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[KM生存曲线_KaplanMeier]] | Kaplan-Meier curve | tested | high | survminer | lifelines |
| [[竞争风险累积发病图_CompetingRisk]] | Cumulative incidence (competing risks) | tested | high | survival (broom) | lifelines |

## 相关性图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[BlandAltman一致性图_BlandAltman]] | Bland-Altman agreement plot | tested | high | ggplot2 | matplotlib |
| [[散点图_Scatter]] | Scatter plot | tested | high | ggplot2 | seaborn/matplotlib |

## 组学图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[火山图_Volcano]] | Volcano plot | tested | high | ggplot2 | matplotlib/seaborn |

## 组间比较图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[柱状图_Bar]] | Bar plot | tested | high | ggplot2 | matplotlib/seaborn |
| [[点估计置信区间图_PointRange]] | Point-range plot | tested | high | ggplot2 | matplotlib |
| [[箱线图_Boxplot]] | Boxplot | tested | high | ggplot2 + ggpubr | seaborn |

## 证据合成图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[Meta森林图_MetaForest]] | Meta-analysis forest plot | tested | high | ggplot2 | matplotlib |
| [[漏斗图_Funnel]] | Funnel plot | tested | medium | ggplot2 | matplotlib |

## 预测模型评价图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[ROC曲线_ROC]] | ROC curve | tested | high | pROC | scikit-learn |
| [[决策曲线_DCA]] | Decision curve analysis (DCA) | tested | high | ggplot2 | matplotlib |
| [[校准曲线_Calibration]] | Calibration curve | tested | high | rms | scikit-learn |
| [[混淆矩阵_ConfusionMatrix]] | Confusion matrix | tested | high | ggplot2 | scikit-learn/seaborn |

## 高维数据图

| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |
|---|---|---|---|---|---|
| [[PCA图_PCA]] | PCA plot | tested | high | ggplot2 (prcomp) | scikit-learn + matplotlib |
| [[热图_Heatmap]] | Heatmap | tested | high | ComplexHeatmap/pheatmap | seaborn |
