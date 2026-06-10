---
title: R 绘图资源索引
type: resource-index
status: active
updated: 2026-06-10
tags:
  - dataviz
  - resource
  - r
  - index
---

# R 绘图资源索引

> 每个资源按 [[资源评价标准]] 的统一格式记录，重点是“**对本知识库有什么用**”，而不是复制官方介绍。
> 维护状态/license 截至 2026-06，若过时请在对应条目标注。

## 速览（按角色）

| 角色 | 包 | 一句话 |
|---|---|---|
| 核心框架 | ggplot2 | R 科研绘图的图形语法地基 |
| 图例库 | R Graph Gallery | 按图类型组织的代码示例集 |
| 期刊配色 | ggsci | NPG/Lancet/JAMA/NEJM/AAAS 色板 |
| 出版增强 | ggpubr | publication-ready + p 值标注 |
| 媒体主题 | ggthemes | Economist/Tufte/WSJ 等主题 |
| 组合图 | patchwork / cowplot | 多面板拼版与对齐 |
| 热图 | ComplexHeatmap / pheatmap | 注释热图 / 快速聚类热图 |
| 生存 | survminer | KM + risk table + p 值 |
| 森林图 | forestplot / forestploter | OR/HR/RR/meta 表图对齐 |
| 组学 | EnhancedVolcano | 火山图 |
| 降维 | factoextra | PCA/聚类结果可视化 |
| 分布 | ggdist / ggridges / ggbeeswarm | 雨云/山峦/蜂群 |

---

## ggplot2 ★核心

- **官网/文档**：https://ggplot2.tidyverse.org/ ｜ 书：https://ggplot2-book.org/
- **GitHub**：https://github.com/tidyverse/ggplot2 ｜ **维护**：活跃（tidyverse 核心）｜ **license**：MIT ｜ **适合程度**：高
- **主要用途**：用 Grammar of Graphics 搭几乎所有静态统计图。
- **可迁移到本库**：图层心智模型（data+aes+geom+scale+facet+theme）是所有 R 卡片的骨架；`theme_*()` → [[ggplot2通用主题]]；scale/facet/geom 参数 → [[ggplot2参数系统]]。
- **代表性思路**：`ggplot(df, aes(x, y, color=g)) + geom_*() + scale_*() + facet_*() + theme_*()`；所有卡片第 7 节都基于它。

## R Graph Gallery ★图例库

- **网址**：https://r-graph-gallery.com/ ｜ **维护**：活跃 ｜ **license**：示例代码可学习（注明出处）｜ **适合程度**：高
- **用途**：按图表类型（distribution/correlation/ranking/part-of-whole/evolution/map/flow）组织的可运行示例。
- **可迁移**：它的**图表分类法**可作为本库 `02_图表类型知识卡片` 分族的对照；每张卡片第 9.1 节优先从这里找网络示例（见 [[图表示例图库索引]]）。
- **注意**：示例偏“能跑”，未必发表级；需经本库质量清单再加工。

## ggsci ★期刊配色

- **文档**：https://nanx.me/ggsci/ ｜ **GitHub**：https://github.com/nanxstats/ggsci ｜ **license**：GPL-3 ｜ **适合程度**：高
- **用途**：`scale_color_npg()/lancet()/jama()/nejm()/aaas()/lancet()` 等期刊风格离散色板。
- **可迁移**：→ [[分类变量配色]] 与 [[医学二分类配色]] 的“期刊色板”来源；但**不要盲目追同款**，先过色盲检查（见 [[色盲友好与打印友好原则]]）。
- **注意**：部分期刊色板红绿对立，色盲不友好；NPG 较常用且相对安全。

## ggpubr ★出版增强

- **文档**：https://rpkgs.datanovia.com/ggpubr/ ｜ **GitHub**：https://github.com/kassambara/ggpubr ｜ **license**：GPL-2 ｜ **适合程度**：高
- **用途**：`ggboxplot/ggviolin/ggscatter` 一行出图 + `stat_compare_means()` 加组间检验 p 值。
- **可迁移**：组间比较图卡片（[[箱线图_Boxplot]]/[[小提琴图_Violin]]）的“快速 + 标 p 值”路径。
- **注意**：封装高、定制性弱于原生 ggplot2；发表级图建议回到原生层精修。p 值标注别滥用（见 [[标签与注释设计]]）。

## ggthemes

- **文档**：https://jrnold.github.io/ggthemes/ ｜ **license**：GPL-2 ｜ **适合程度**：中
- **用途**：Economist/Tufte/FiveThirtyEight/WSJ/Stata 等主题与色板。
- **可迁移**：`theme_tufte()` 的极简/高数据墨水比理念 → [[ggplot2通用主题]] 的设计原则；多数媒体主题**不适合论文**，仅作风格参考。

## patchwork ★组合图

- **文档**：https://patchwork.data-imaginist.com/ ｜ **license**：MIT ｜ **适合程度**：高
- **用途**：用 `p1 + p2`、`p1 / p2`、`(p1|p2)/p3` 直观拼多面板；`plot_annotation(tag_levels='A')` 自动 A/B/C/D。
- **可迁移**：→ [[多面板组合图_MultiPanel]] 与 [[patchwork与cowplot组合图]] 的首选拼版工具。

## cowplot

- **文档**：https://wilkelab.org/cowplot/ ｜ **license**：GPL-2 ｜ **适合程度**：高
- **用途**：`plot_grid()` 精确对齐、`get_legend()` 共享图例、`draw_plot()` 画中画。
- **可迁移**：对齐要求高（坐标轴严格对齐）时优于 patchwork；→ [[patchwork与cowplot组合图]]。

## ComplexHeatmap ★热图天花板

- **文档**：https://jokergoo.github.io/ComplexHeatmap-reference/book/ ｜ **GitHub**：https://github.com/jokergoo/ComplexHeatmap ｜ 来源 Bioconductor ｜ **license**：MIT ｜ **适合程度**：高
- **用途**：多层 row/column annotation、聚类、按变量拆分、热图并排组合。组学/临床注释热图无可替代。
- **可迁移**：→ [[热图_Heatmap]] 高质量路径 + [[ComplexHeatmap模板]]。
- **注意**：API 学习曲线陡；简单聚类热图用 pheatmap 即可。

## pheatmap

- **GitHub**：https://github.com/raivokolde/pheatmap ｜ CRAN ｜ **license**：GPL-2 ｜ **适合程度**：中（维护较慢）
- **用途**：一行出聚类热图 + 简单 annotation。
- **可迁移**：[[热图_Heatmap]] 的“快速版”；复杂需求转 ComplexHeatmap。

## survminer ★生存可视化

- **文档**：https://rpkgs.datanovia.com/survminer/ ｜ 依赖 survival 包 ｜ **license**：GPL-2 ｜ **适合程度**：高
- **用途**：`ggsurvplot()` 一步出 KM 曲线 + risk table + log-rank p 值 + censoring 标记；`ggforest()` 出 Cox 森林图。
- **可迁移**：→ [[KM生存曲线_KaplanMeier]] + [[survminer生存曲线模板]]。
- **注意**：底层用 survival::survfit / coxph，先把统计建对再画。

## forestplot / forestploter ★森林图

- **forestplot**：https://github.com/gforge/forestplot （CRAN, GPL-2）
- **forestploter**：https://github.com/adayim/forestploter （CRAN, MIT，**更现代、表图对齐更灵活**，推荐）
- **用途**：OR/HR/RR、回归系数、meta 分析的“左表 + 右图 + 参考线”。
- **可迁移**：→ [[森林图_ForestPlot]] + [[forestplot森林图模板]]。

## EnhancedVolcano

- **Bioconductor**：https://bioconductor.org/packages/EnhancedVolcano/ ｜ **license**：GPL-3 ｜ **适合程度**：高（组学）
- **用途**：差异表达火山图，自动阈值线 + 标基因。→ 未来组学族卡片。

## factoextra

- **文档**：https://rpkgs.datanovia.com/factoextra/ ｜ **license**：GPL-2 ｜ **适合程度**：中
- **用途**：`fviz_pca_ind/var()`、`fviz_cluster()`、`fviz_dend()` 可视化 PCA/聚类/层次树。→ 未来高维族卡片。

## ggdist / ggridges / ggbeeswarm ★分布扩展

- **ggdist**：https://mjskay.github.io/ggdist/ （MIT）— 雨云图、分位点区间、`stat_halfeye`/`stat_dots`。→ [[雨云图_Raincloud]]
- **ggridges**：https://wilkelab.org/ggridges/ （GPL-2）— 山峦图（ridgeline）。
- **ggbeeswarm**：https://github.com/eclarke/ggbeeswarm （GPL-3）— 蜂群图避免点重叠。→ [[箱线图_Boxplot]]/[[小提琴图_Violin]] 叠点。

---

## 取舍小结（给 Agent 路由用）

- 统计图骨架永远是 **ggplot2**；快速 + p 值用 **ggpubr**；期刊配色用 **ggsci**（先过色盲检查）。
- 多面板：随手拼用 **patchwork**，要严格对齐用 **cowplot**。
- 热图：简单 **pheatmap**，复杂注释 **ComplexHeatmap**。
- 生存 **survminer**；森林图 **forestploter**；分布扩展 **ggdist** 系。

相关：[[Python绘图资源索引]] · [[科研配色资源索引]] · [[资源评价标准]] · [[R与Python后端选择规则]]
