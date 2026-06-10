---
title: ggplot2 参数系统
type: code-template
status: active
backend: r
updated: 2026-06-10
tags:
  - dataviz
  - r
  - ggplot2
  - parameters
  - template
---

# ggplot2 参数系统

> 把 ggplot2 拆成**可参数化的 6 个槽位**，便于卡片复用、便于未来 Skill 注入参数。每个槽位标了常用旋钮。

## 1. 六槽位心智模型

```r
ggplot(data, aes(MAPPING)) +   # ① 数据 + ② 映射(aes)
  GEOM(...) +                  # ③ 几何对象（可多层）
  SCALE(...) +                 # ④ 标度（颜色/坐标/大小）
  FACET(...) +                 # ⑤ 分面
  THEME(...)                   # ⑥ 主题（见 ggplot2通用主题）
```

## 2. ① 映射 aes — 可注入点

```r
aes(x = , y = , color = , fill = , shape = , size = , linetype = , group = , alpha = )
# >>> PARAM 哪些列映射到哪些视觉通道，由数据语义决定
```
- 位置（x/y）最重要；color/fill 走配色系统；shape/linetype 做色盲冗余编码。

## 3. ③ 常用 geom 与关键参数

| geom | 用途 | 关键参数 |
|---|---|---|
| `geom_point` | 散点 | `alpha`(防重叠), `size`, `shape` |
| `geom_jitter` | 抖动散点 | `width`,`height`,`alpha`（叠在箱线上）|
| `geom_boxplot` | 箱线 | `outlier.shape=NA`(叠点时隐离群), `width` |
| `geom_violin` | 小提琴 | `trim`,`scale`("area"/"width"/"count"), `bw` |
| `geom_line`/`geom_path` | 折线/轨迹 | `linewidth`,`group`,`linetype` |
| `geom_smooth` | 拟合 | `method`("lm"/"loess"),`se`,`formula` |
| `geom_col`/`geom_bar` | 柱状 | `position`("dodge"/"stack"/"fill"),`width` |
| `geom_pointrange` | 点+区间 | `aes(ymin=,ymax=)`,`fatten` |
| `geom_tile`/`geom_raster` | 热图格 | `aes(fill=)` |
| `geom_hline/vline` | 参考线 | `yintercept`,`linetype`,`color` |
| `geom_errorbar` | 误差棒 | `width`,`aes(ymin=,ymax=)` |

## 4. ④ scale — 标度旋钮

```r
# 颜色（接配色系统）
scale_color_manual(values = okabe_ito)              # 分类
scale_color_viridis_c()                             # 连续
scale_fill_gradient2(low,mid,high, midpoint = 0)    # 发散
scale_color_npg()                                   # ggsci 期刊

# 坐标（接坐标轴设计）
scale_y_continuous(limits = c(0,NA), expand = expansion(mult = c(0,.05)))
scale_x_log10(breaks = c(0.25,0.5,1,2,4))           # 比值/跨量级
scale_x_discrete(labels = function(x) str_wrap(x, 10))  # 长标签换行

# 大小/形状
scale_size_continuous(range = c(1,6))
scale_shape_manual(values = c(16,17,15))
```

## 5. ⑤ facet — 分面（接 [[分面与多面板设计]]）

```r
facet_wrap(~ var, ncol = 3, scales = "fixed")       # >>> PARAM scales
facet_grid(rows ~ cols)
```

## 6. 常用辅助包旋钮

| 包 | 函数 | 作用 |
|---|---|---|
| ggpubr | `stat_compare_means()` | 组间 p 值（[[标签与注释设计]]）|
| ggrepel | `geom_text_repel()` | 防重叠标注 / 直接标注 |
| ggbeeswarm | `geom_quasirandom()` | 蜂群点替代 jitter |
| ggdist | `stat_halfeye()`,`stat_dots()` | 雨云图（[[雨云图_Raincloud]]）|
| scales | `label_number()`,`label_percent()` | 轴标签格式 |

## 7. 一个“全槽位”示例

```r
ggplot(df, aes(x = group, y = value, fill = group)) +    # ①②
  geom_boxplot(outlier.shape = NA, width = .55, alpha = .85) +  # ③
  geom_quasirandom(size = .8, alpha = .5) +                     # ③ 叠点
  scale_fill_manual(values = okabe_ito) +                       # ④ 颜色
  scale_y_continuous(expand = expansion(mult = c(.02,.08))) +   # ④ 坐标
  facet_wrap(~ subgroup) +                                      # ⑤ 分面
  labs(x = NULL, y = "BMI (kg/m²)") +
  theme_pub() + theme(legend.position = "none")                # ⑥ 主题
```

## 8. 给 Skill 的参数清单（机器可读雏形）

```yaml
geom: boxplot+jitter        # 几何组合
x: group                    # 分类
y: value                    # 连续
fill_palette: cat_main      # 配色 registry 名
y_from_zero: false
facet_by: subgroup | null
add_pvalue: kruskal + preset
theme: pub | talk
```

相关：[[ggplot2通用主题]] · [[配色系统总览]] · [[坐标轴设计]] · [[分面与多面板设计]] · [[输入输出规范]]
