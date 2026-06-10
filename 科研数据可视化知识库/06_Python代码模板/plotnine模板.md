---
title: plotnine 模板
type: code-template
status: active
backend: python
updated: 2026-06-10
tags:
  - dataviz
  - python
  - plotnine
  - ggplot
  - template
---

# plotnine 模板

> Python 里的 ggplot2：几乎 1:1 复刻图形语法。想把 R 卡片思路平移到 Python 时用它，跨语言统一心智模型。

## 1. 与 ggplot2 的映射

| ggplot2 (R) | plotnine (Py) |
|---|---|
| `ggplot(df, aes(x,y))` | `ggplot(df, aes("x","y"))`（字符串列名）|
| `geom_point()` | `geom_point()` |
| `scale_color_manual()` | `scale_color_manual()` |
| `facet_wrap(~g)` | `facet_wrap("~g")` |
| `theme_minimal()` | `theme_minimal()` |
| `+ labs(...)` | `+ labs(...)` |

> 主要差异：列名用**字符串**；公式用字符串（`"~g"`）；个别 geom/stat 行为略有不同。

## 2. 通用骨架

```python
from plotnine import *
okabe = ["#E69F00","#56B4E9","#009E73","#0072B2","#D55E00","#CC79A7"]

p = (ggplot(df, aes("grp", "BMI", fill="grp"))
     + geom_boxplot(outlier_shape="", width=.55, alpha=.85)   # 隐离群叠点
     + geom_jitter(width=.18, size=.8, alpha=.4)
     + scale_fill_manual(values=okabe)                        # >>> PARAM 配色
     + labs(x="", y="BMI (kg/m²)")
     + theme_minimal(base_size=9)
     + theme(legend_position="none"))
p
```

## 3. 发表级主题（对齐 [[matplotlib通用主题]] 思路）

```python
theme_pub = (theme_minimal(base_size=9)
             + theme(panel_grid_minor=element_blank(),
                     panel_grid_major=element_line(color="#ECECEC", size=.3),
                     axis_line=element_line(color="black", size=.4),
                     legend_position="right",
                     strip_background=element_blank(),
                     strip_text=element_text(weight="bold")))
# 用： p + theme_pub
```

## 4. 常用 geom（与 R 同名）

`geom_point/jitter/line/smooth(method='lm'/'lowess')/boxplot/violin/col/bar/tile/errorbar/hline/vline/density/histogram`

```python
# 散点 + 回归 + CI 带
(ggplot(df, aes("sysBP","diaBP")) + geom_point(alpha=.4)
 + geom_smooth(method="lm", se=True, color="#D55E00"))
```

## 5. 导出

```python
p.save("fig.pdf", width=89, height=70, units="mm")   # 矢量
p.save("fig.png", width=89, height=70, units="mm", dpi=600)
```
见 [[Python导出规范]]。

## 6. 何时用 plotnine vs seaborn

| 选 plotnine | 选 seaborn |
|---|---|
| 想完全套用 R 卡片的 ggplot 思路 | 想最快出统计图 |
| 团队习惯图形语法 | 紧贴 pandas/sklearn 管道 |
| 需要图层叠加心智清晰 | 需要 mpl 深度精修 |

## 7. 常见错误（→ 返修）

- ❌ 列名忘了加引号（plotnine 要字符串）。
- ❌ 期望与 ggplot2 完全一致——个别 stat 默认值不同，核对。
- ❌ 配色没接 registry → 用 Okabe-Ito/viridis（[[配色系统总览]]）。

相关：[[matplotlib通用主题]] · [[seaborn统计图模板]] · [[ggplot2参数系统]]（R 对应）· [[Python导出规范]]
