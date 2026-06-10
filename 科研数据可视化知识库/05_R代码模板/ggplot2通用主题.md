---
title: ggplot2 通用主题
type: code-template
status: active
backend: r
updated: 2026-06-10
tags:
  - dataviz
  - r
  - ggplot2
  - theme
  - template
---

# ggplot2 通用主题

> 一套**发表级 + 汇报级**可复用主题，供所有 R 图表卡片 `+ theme_pub()` 调用。设计原则：高数据墨水比、无衬线、刻度朝内、网格克制。

## 1. 设计原则（为什么这样写）

- 去掉默认灰底/重网格 → 提高数据墨水比（Tufte）。
- 无衬线字体、统一 base_size → 全 figure 一致（[[论文单栏双栏尺寸]]）。
- 只留必要的浅色网格辅助读数；轴线保留。
- 主题与配色解耦：颜色走 [[配色系统总览]]，主题只管非数据外观。

## 2. 发表级主题 `theme_pub()`

```r
library(ggplot2)

theme_pub <- function(base_size = 9, base_family = "sans") {  # >>> PARAM base_size
  theme_minimal(base_size = base_size, base_family = base_family) +
    theme(
      panel.grid.minor   = element_blank(),
      panel.grid.major   = element_line(color = "grey92", linewidth = 0.3),
      axis.line          = element_line(color = "black", linewidth = 0.4),
      axis.ticks         = element_line(color = "black", linewidth = 0.3),
      axis.title         = element_text(size = base_size + 1),
      plot.title         = element_text(size = base_size + 3, face = "bold"),
      plot.subtitle      = element_text(size = base_size, color = "grey30"),
      legend.position    = "right",
      legend.key.size    = unit(0.9, "lines"),
      strip.text         = element_text(size = base_size, face = "bold"),
      strip.background   = element_blank(),
      plot.margin        = margin(4, 6, 4, 4)
    )
}
```

## 3. 汇报级主题 `theme_talk()`

```r
theme_talk <- function(base_size = 18) {            # >>> PARAM 放大
  theme_pub(base_size = base_size) +
    theme(
      legend.position  = "bottom",
      panel.grid.major = element_line(color = "grey88", linewidth = 0.4),
      plot.background  = element_rect(fill = "white", color = NA)
    )
}
```

## 4. 设全局默认（少写 theme）

```r
theme_set(theme_pub())              # 一次设定，后续所有图继承
# 配色默认（Okabe-Ito）：
okabe_ito <- c("#E69F00","#56B4E9","#009E73","#F0E442",
               "#0072B2","#D55E00","#CC79A7","#999999")
options(ggplot2.discrete.colour = okabe_ito,
        ggplot2.discrete.fill   = okabe_ito)
```

## 5. 字体说明

- `family = "sans"` 跨平台映射到系统无衬线字体。
- 想固定 Arial/Helvetica：用 `ragg`/`systemfonts` + `showtext`，并在 [[R导出规范]] 里用 `cairo_pdf`/`ragg::agg_png` 保证字体嵌入。
- 中文图：`showtext::showtext_auto()` + 指定中文字体；论文图尽量英文。

## 6. 用法示例

```r
ggplot(mtcars, aes(wt, mpg)) +
  geom_point(color = "#0072B2") +
  labs(x = "Weight (1000 lbs)", y = "MPG", title = "Demo") +
  theme_pub()                         # 发表级
# 汇报： + theme_talk()
```

## 7. 与其他文件的关系

- 参数（scale/facet/geom 细节）→ [[ggplot2参数系统]]
- 组合多面板 → [[patchwork与cowplot组合图]]
- 导出（尺寸/dpi/矢量/字体）→ [[R导出规范]]
- 配色 → [[配色系统总览]]

相关：[[ggplot2参数系统]] · [[R导出规范]] · [[matplotlib通用主题]]（Python 对应）
