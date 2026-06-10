---
chart_name: 多面板组合图
chart_name_en: Multi-panel figure
chart_family: 多面板组合图
data_type:
  - composite
recommended_backend:
  r: patchwork/cowplot
  python: matplotlib gridspec
difficulty: intermediate
priority: high
status: tested
tags:
  - dataviz
  - chart
  - multipanel
  - figure
  - layout
  - r
  - python
---

# 多面板组合图 Multi-panel figure

> 把多张子图拼成一张完整 Figure（A/B/C/D），讲一个完整故事。论文 Figure 1（baseline）、Figure 2（model result）的标准形态。区别于“分面”（同种图按变量拆），多面板是**不同图**的组合。

## 1. 图表定位

回答“**围绕一个主题，用几张互补的子图把证据链讲完整**”。子图各司其职，整体大于部分之和。

## 2. 适用场景

- Figure 1：研究人群 baseline 特征可视化（分布 + 组间 + 比例）。
- Figure 2：模型结果（森林图 + ROC + 校准 + KM）。
- 方法/结果的多步骤叙事。
- 期刊版面要求把相关图合并为一个编号 Figure。

## 3. 不适用场景

- 单图就能讲清 → 别硬拼。
- 同种图按变量拆 → 用**分面**（[[分面与多面板设计]]），不是多面板。
- 子图毫不相关 → 拆成独立 Figure。
- 版面太小塞 6+ 子图 → 拆图或转补充材料。

## 4. 数据结构要求

无统一矩阵；每个子图有各自数据。组织上需要：

| 要素 | 说明 |
|---|---|
| 子图列表 | 各自独立的 ggplot/Axes 对象 |
| 布局 | 行列/比例/嵌套关系 |
| 标号 | A/B/C/D 顺序与位置 |
| 共享元素 | 共享图例/配色/字体 |

## 5. 图表架构选择

### 5.1 基础架构
- 网格布局（2×2、1+2、上大下小）；
- 每子图左上角 A/B/C/D 加粗；
- 统一字体/字号/配色。

### 5.2 高质量架构
- 子图大小按信息量分配（重点子图更大）。
- 共享图例合并到一处（[[图例设计]]）。
- 坐标轴对齐（cowplot/gridspec）。
- 嵌套布局（patchwork `()` 分组 / gridspec 子网格）。
- 总标题/总图注统筹。

参见 [[分面与多面板设计]] 与 [[论文单栏双栏尺寸]]（按双栏设计）。

## 6. 配色选择
- 全 figure **统一一套** registry 配色（[[配色系统总览]]），子图间语义一致（病例在每个子图都同色）。
- 一个共享图例服务全 figure。

## 7. R 实现方案

### 7.1 推荐包
patchwork（随手拼 + 自动标号）、cowplot（严格对齐 + 共享图例）。详见 [[patchwork与cowplot组合图]]。

### 7.2 关键参数
patchwork `+ | /`、`plot_layout(widths=, heights=, guides="collect")`、`plot_annotation(tag_levels="A")`；cowplot `plot_grid(align="hv", labels=)`、`get_legend()`。

### 7.3 基础代码模板
```r
library(patchwork)
(p_box | p_scatter) / (p_forest | p_roc) +
  plot_annotation(tag_levels = "A") &
  theme(plot.tag = element_text(face = "bold"))
```

### 7.4 发表级代码模板（不等大 + 共享图例）
```r
library(patchwork)
design <- "
AAB
AAC
"
fig <- p_main + p_top + p_bottom +
  plot_layout(design = design, guides = "collect") +
  plot_annotation(tag_levels = "A",
                  title = "Figure 2. Model performance") &
  theme(legend.position = "bottom",
        plot.tag = element_text(face = "bold", size = 11))
ggsave("fig2.pdf", fig, width = 183, height = 130, units = "mm", device = cairo_pdf)
```

## 8. Python 实现方案

### 8.1 推荐包
matplotlib（`gridspec`、`subplot_mosaic`、`subplots`）

### 8.2 关键参数
`fig.add_gridspec(nrows, ncols, height_ratios=, hspace=)`、`plt.subplot_mosaic(layout_str)`、`ax.text(transform=ax.transAxes)` 标号、`fig.legend` 共享图例。

### 8.3 基础代码模板（subplot_mosaic）
```python
fig, axd = plt.subplot_mosaic([["A","B"],["C","D"]], figsize=(7,6), constrained_layout=True)
plot_box(axd["A"]); plot_scatter(axd["B"]); plot_forest(axd["C"]); plot_roc(axd["D"])
for k, ax in axd.items():
    ax.text(-0.12, 1.05, k, transform=ax.transAxes, fontweight="bold", fontsize=12)
```

### 8.4 发表级代码模板（gridspec 不等大 + 共享图例）
```python
mm = 1/25.4
fig = plt.figure(figsize=(183*mm, 130*mm), constrained_layout=True)
gs = fig.add_gridspec(2, 3, width_ratios=[2,1,1])
axA = fig.add_subplot(gs[:, 0])    # 大主图占左两行
axB = fig.add_subplot(gs[0, 1:])
axC = fig.add_subplot(gs[1, 1:])
# ... 各自画图，统一配色 ...
handles, labels = axA.get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False)  # 共享图例
for ax, lab in zip([axA,axB,axC], "ABC"):
    ax.text(-0.08, 1.04, lab, transform=ax.transAxes, fontweight="bold")
fig.savefig("fig2.pdf", bbox_inches="tight")
```

## 9. 示例图像

### 9.1 网络优秀示例
见 [[MultiPanel_优秀示例]]（含 Nature/医学 Figure 1/2 多面板范式）。
本库自制范式图（合成数据，A/B/C/D 四面板）：

![[demo_multipanel.png]]

### 9.2 Framingham 数据测试示例
✅ 已跑通 **Figure 1（baseline）** 与 **Figure 2（model）**。代码见 [[R测试记录]] / [[Python测试记录]] 与 [[patchwork与cowplot组合图]]。

Figure 1 — baseline characteristics（R / patchwork：A 年龄组、B BMI 箱线、C 吸烟率、D 相关热图）：

![[fig1_baseline_multipanel_r.png]]

Figure 2 — model performance（A 森林、B ROC、C 校准、D KM）：

R（patchwork）：

![[fig2_model_multipanel_r.png]]

Python（subplot_mosaic）：

![[fig2_model_multipanel_py.png]]

> 结论：一张 figure 讲完一条证据链，两后端的 Figure 1/2 均做到字体/配色统一 + A/B/C/D 标号 + 共享图例。R 的 patchwork 用运算符拼版最直观；Python 的 gridspec/mosaic 更贴合分析管道。另有 `fig1_baseline_multipanel_py.png`（Python 版 Figure 1）。

## 10. 常见错误
- 子图字体/字号/配色不一致。
- 每个子图各放一份相同图例。
- A/B/C/D 位置/字号乱。
- 子图坐标轴不对齐。
- 塞太多子图导致每个都太小。
- 子图间语义不一致（同一组在不同子图换色）。

## 11. 自动返修规则
- 字号不一 → 统一 `theme_set`/`rcParams` 基准。
- 重复图例 → `guides="collect"` / `get_legend` / `fig.legend` 合并。
- 子图过小 → 减子图数 / 转补充材料 / 增大画布。
- 对齐差 → cowplot `align="hv"` / gridspec 对齐。
- 标号不统一 → 统一 tag 系统。

## 12. 与其他图表的关系
- vs 分面（facet）：分面是同种图按变量拆（[[分面与多面板设计]]）；多面板是不同图组合。
- 子图通常来自其他卡片（[[箱线图_Boxplot]]/[[森林图_ForestPlot]]/[[ROC曲线_ROC]]/[[KM生存曲线_KaplanMeier]]/[[热图_Heatmap]]）。
- 工具细节见 [[patchwork与cowplot组合图]]。

## 13. 质量检查清单
- [ ] 全 figure 字体/字号/配色一致？
- [ ] 共享图例合并到一处？
- [ ] A/B/C/D 规范统一？
- [ ] 子图对齐？
- [ ] 子图数量与大小合理？
- [ ] 语义跨子图一致？
- [ ] 适合论文双栏导出？

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建立初稿 | 缺实测图 | 拼 Framingham Figure 1/2 |

相关：[[分面与多面板设计]] · [[patchwork与cowplot组合图]] · [[图例设计]] · [[论文单栏双栏尺寸]] · [[配色系统总览]]
