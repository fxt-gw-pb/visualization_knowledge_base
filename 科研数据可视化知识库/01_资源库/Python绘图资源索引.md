---
title: Python 绘图资源索引
type: resource-index
status: active
updated: 2026-06-10
tags:
  - dataviz
  - resource
  - python
  - index
---

# Python 绘图资源索引

> 格式同 [[R绘图资源索引]]，重点是“对本库有什么用”。维护状态/license 截至 2026-06。

## 速览（按角色）

| 角色 | 库 | 一句话 |
|---|---|---|
| 底层核心 | matplotlib | Python 绘图地基，精细控制 |
| 统计快速 | seaborn | 统计图一行出 + 美观默认 |
| 图形语法 | plotnine | Python 版 ggplot2 |
| 论文样式 | SciencePlots | matplotlib 的 science/ieee/nature 样式 |
| 声明式 | altair | Vega-Lite 声明式 + 交互 |
| 交互 | plotly | 网页交互图 |
| 模型评价 | scikit-learn display | ROC/PR/混淆矩阵/校准一行出 |
| 生存 | lifelines | KM/Cox/AalenJohansen |
| 统计诊断 | statsmodels graphics | QQ/残差/影响图 |
| 缺失值 | missingno | 缺失模式可视化 |
| 山峦图 | joypy | ridgeline |
| 统计标注 | statannotations | seaborn 图加检验 p 值 |

---

## matplotlib ★底层核心

- **官网**：https://matplotlib.org/ ｜ **GitHub**：https://github.com/matplotlib/matplotlib ｜ **license**：PSF-based(BSD-compatible) ｜ **维护**：活跃 ｜ **适合程度**：高
- **用途**：figure/axes 的命令式精细控制；所有 Python 图最终都落到它。
- **可迁移**：`rcParams` 全局样式 → [[matplotlib通用主题]]；figure/axes/gridspec → [[多面板组合图_MultiPanel]]；导出 → [[Python导出规范]]。
- **代表性思路**：`fig, ax = plt.subplots(figsize=...)`；`ax.plot/scatter/...`；`ax.set_xlabel/ylabel/legend`；`fig.savefig(..., dpi=300, bbox_inches='tight')`。

## seaborn ★统计快速

- **官网**：https://seaborn.pydata.org/ ｜ **GitHub**：https://github.com/mwaskom/seaborn ｜ **license**：BSD-3 ｜ **适合程度**：高
- **用途**：`boxplot/violinplot/stripplot/regplot/heatmap/pairplot/kdeplot`；`objects` 接口（v0.12+）走图形语法。
- **可迁移**：组间/分布/相关卡片的 Python 主路径（[[箱线图_Boxplot]]/[[小提琴图_Violin]]/[[散点图_Scatter]]）→ [[seaborn统计图模板]]。
- **注意**：返回的是 matplotlib Axes，可继续用 mpl 精修；调色板用 `palette=` 接入命名色板（见 [[配色系统总览]]）。

## plotnine ★图形语法

- **文档**：https://plotnine.org/ ｜ **GitHub**：https://github.com/has2k1/plotnine ｜ **license**：MIT ｜ **适合程度**：高
- **用途**：几乎 1:1 复刻 ggplot2 API（`ggplot(df, aes(...)) + geom_*()`）。
- **可迁移**：把 R 卡片的 ggplot 思路平移到 Python；跨语言统一心智模型 → [[plotnine模板]]。
- **注意**：生态/扩展少于 ggplot2；个别 geom 行为有差异。

## SciencePlots ★论文样式

- **GitHub**：https://github.com/garrettj403/SciencePlots ｜ **license**：MIT ｜ **适合程度**：高
- **用途**：`plt.style.use(['science','nature'])` 等，一键切到论文风（衬线/无衬线、刻度朝内、紧凑）。
- **可迁移**：→ [[SciencePlots模板]] + [[matplotlib通用主题]] 的论文风预设。
- **注意**：默认用 LaTeX 渲染文字，需本机有 LaTeX；可关掉 `tex` 子样式避免依赖。

## altair

- **文档**：https://altair-viz.github.io/ ｜ **license**：BSD-3 ｜ **适合程度**：中
- **用途**：基于 Vega-Lite 的声明式语法，快速探索 + 交互 + 链接刷选。
- **可迁移**：探索阶段快速出图；最终论文图仍回 matplotlib/ggplot2 导矢量。

## plotly

- **文档**：https://plotly.com/python/ ｜ **license**：MIT ｜ **适合程度**：中（交互场景高）
- **用途**：交互式 HTML 图、3D、悬停。→ 网页展示/汇报，不用于论文静态图。

## scikit-learn metrics display ★模型评价

- **文档**：https://scikit-learn.org/stable/visualizations.html ｜ **license**：BSD-3 ｜ **适合程度**：高
- **用途**：`RocCurveDisplay`、`PrecisionRecallDisplay`、`ConfusionMatrixDisplay`、`CalibrationDisplay`（后者在 `sklearn.calibration`）一行出评价图，可叠多模型。
- **可迁移**：→ [[ROC曲线_ROC]]、[[校准曲线_Calibration]] 的 Python 主路径 + [[sklearn模型评价图模板]]。

## lifelines ★生存

- **文档**：https://lifelines.readthedocs.io/ ｜ **GitHub**：https://github.com/CamDavidsonPilon/lifelines ｜ **license**：MIT ｜ **适合程度**：高
- **用途**：`KaplanMeierFitter`、`CoxPHFitter`、`add_at_risk_counts()`（risk table）、log-rank 检验。
- **可迁移**：→ [[KM生存曲线_KaplanMeier]] Python 路径 + [[lifelines生存曲线模板]]。

## statsmodels graphics

- **文档**：https://www.statsmodels.org/stable/graphics.html ｜ **license**：BSD-3 ｜ **适合程度**：中
- **用途**：QQ 图、残差图、影响图、partial regression、ROC 等统计诊断。→ 模型诊断/回归卡片。

## missingno

- **GitHub**：https://github.com/ResidentMario/missingno ｜ **license**：MIT ｜ **适合程度**：中
- **用途**：`matrix/bar/heatmap/dendrogram` 看缺失模式。→ [[变量字典]] 缺失值探查（Framingham 的 GLUCOSE/TOTCHOL 有缺失）。

## joypy

- **GitHub**：https://github.com/leotac/joypy ｜ **license**：MIT ｜ **适合程度**：中
- **用途**：ridgeline/joyplot（山峦图）。→ 未来山峦图卡片；也可用 seaborn 的 KDE 叠加替代。

## statannotations

- **GitHub**：https://github.com/trevismd/statannotations ｜ **license**：MIT ｜ **适合程度**：中（注意与新版 seaborn 兼容性）
- **用途**：在 seaborn boxplot/violin 上自动加组间检验括号 + p 值（对标 R 的 ggpubr `stat_compare_means`）。
- **注意**：对 seaborn 版本敏感，升级 seaborn 后可能需固定版本。

---

## 取舍小结（给 Agent 路由用）

- 统计图快速出 → **seaborn**；要精细/论文级 → 落到 **matplotlib**（+ **SciencePlots** 样式）。
- 想用 ggplot 语法 → **plotnine**。
- 模型评价图 → **scikit-learn display**；生存 → **lifelines**。
- 交互/探索 → **altair / plotly**，不用于最终论文静态图。

相关：[[R绘图资源索引]] · [[科研配色资源索引]] · [[资源评价标准]] · [[R与Python后端选择规则]]
