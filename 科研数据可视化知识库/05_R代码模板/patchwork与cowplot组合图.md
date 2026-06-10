---
title: patchwork 与 cowplot 组合图
type: code-template
status: active
backend: r
updated: 2026-06-10
tags:
  - dataviz
  - r
  - patchwork
  - cowplot
  - multipanel
  - template
---

# patchwork 与 cowplot 组合图

> R 端拼多面板的两把工具：**patchwork** 写法直观、随手拼；**cowplot** 对齐严格、共享图例强。配合 [[多面板组合图_MultiPanel]] 卡片使用。

## 1. 选哪个

| 需求 | 用 |
|---|---|
| 随手拼、运算符直观、自动 A/B/C/D | **patchwork** |
| 坐标轴严格对齐、画中画、精确定位 | **cowplot** |
| 共享一个图例 | 两者都行（见下）|

## 2. patchwork 速成

```r
library(patchwork)
# 运算符：| 并排，/ 堆叠，() 分组
(p1 | p2) / p3

# 控制比例与高度
p1 + p2 + plot_layout(widths = c(2, 1))
(p1 / p2) + plot_layout(heights = c(1, 2))

# 自动 A/B/C/D 标号 + 总标题
(p1 | p2) / p3 +
  plot_annotation(tag_levels = "A", title = "Figure 1") &
  theme(plot.tag = element_text(face = "bold", size = 12))

# 收集共享图例到一处
(p1 | p2) + plot_layout(guides = "collect") & theme(legend.position = "bottom")
```

## 3. cowplot 速成

```r
library(cowplot)
# 网格拼版 + 对齐 + 标号
plot_grid(p1, p2, p3, p4,
          labels = c("A","B","C","D"), label_fontface = "bold",
          ncol = 2, align = "hv", axis = "tblr")     # 严格对齐四边

# 提取并共享图例
legend <- get_legend(p1 + theme(legend.position = "bottom"))
body   <- plot_grid(p1 + theme(legend.position="none"),
                    p2 + theme(legend.position="none"), ncol = 2)
plot_grid(body, legend, ncol = 1, rel_heights = c(1, .1))

# 画中画（inset）
ggdraw(p_main) + draw_plot(p_inset, x = .6, y = .6, width = .35, height = .35)
```

## 4. 一致性检查（拼之前）

- 各子图用**同一主题**（[[ggplot2通用主题]] `theme_pub()`）→ 字体/字号/网格统一。
- 各子图配色来自同一 registry（[[配色系统总览]]）。
- 子图坐标轴单位/范围在需要比较时对齐。
- A/B/C/D 位置、字号统一。

## 5. 导出

```r
fig <- (p1 | p2) / p3 + plot_annotation(tag_levels = "A")
ggsave("fig1.pdf", fig, width = 183, height = 130, units = "mm", device = cairo_pdf)
```
尺寸/dpi/字体见 [[R导出规范]] 与 [[论文单栏双栏尺寸]]。

## 6. 常见错误（→ 返修）

- ❌ 子图主题不一致 → 统一 `theme_set(theme_pub())`。
- ❌ 每个子图各放相同图例 → `guides="collect"` / `get_legend`。
- ❌ 坐标轴没对齐（patchwork 默认不强制）→ 关键场景用 cowplot `align="hv"`。
- ❌ A/B/C/D 字号/位置乱。

相关：[[多面板组合图_MultiPanel]] · [[分面与多面板设计]] · [[ggplot2通用主题]] · [[R导出规范]]
