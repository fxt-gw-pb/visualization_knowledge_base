---
chart_name: 箱线图
chart_name_en: Boxplot
chart_family: 组间比较图
data_type:
  - continuous
  - categorical_group
recommended_backend:
  r: ggplot2 + ggpubr
  python: seaborn
difficulty: basic
priority: high
status: tested
tags:
  - dataviz
  - chart
  - boxplot
  - distribution
  - comparison
  - r
  - python
---

# 箱线图 Boxplot

> 用五数概括（min–Q1–中位数–Q3–max + 离群）比较**多组连续变量的分布**。科研最常用的组间比较图之一。

## 1. 图表定位

回答“**几组之间，某个连续指标的分布有没有差异**”。展示中位数、四分位距（IQR）、离散程度、离群值，对偏态稳健。

## 2. 适用场景

- 比较不同组（性别、是否高血压、年龄组）之间连续变量（BMI、血压、胆固醇）的分布。
- 想同时看中位数、IQR、离群点。
- 样本量中等或较大（每组 ≳ 20–30）。
- 分布偏态、不想假设正态时，比“均值±SD 柱状图”更诚实。

## 3. 不适用场景

- 样本量极小且不叠原始点 → 箱体由太少点估计，误导（改 box+jitter 或直接画点）。
- 想看**完整分布形态**（双峰/多峰）→ 箱线图看不出，改 [[小提琴图_Violin]] / [[雨云图_Raincloud]]。
- 只想表达均值差异 + 不确定性 → [[点估计置信区间图_PointRange]] 更聚焦。
- 类别极多且每类点很少 → 信息稀薄。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| group | categorical | 分组变量（x 轴）| 必需 |
| value | continuous | 连续结局（y 轴）| 必需 |
| subgroup | categorical | 可选分层（分面或 dodge）| 可选 |

长格式（每行一个观测）。

## 5. 图表架构选择

### 5.1 基础架构
- x：分组变量；y：连续变量
- 图层：boxplot（+ 必要时 jitter 原始点）
- 可选：均值点、组间 p 值、参考线

### 5.2 高质量架构
- 样本量较小 → boxplot + raw points（jitter/beeswarm），并隐藏箱线自带离群点避免重复
- 分布形态重要 → violin + boxplot + points（见 [[小提琴图_Violin]]）
- 追求美观 → raincloud（见 [[雨云图_Raincloud]]）
- 组别很多 → 横向 boxplot（`coord_flip`）+ 按中位数排序

参见 [[坐标轴设计]]（y 不必从 0）、[[标签与注释设计]]（p 值克制）。

## 6. 配色选择

### 6.1 默认配色
分类填充用 Okabe-Ito（`cat_main`），见 [[分类变量配色]]。两组优先**留白箱体 + 深色描边**，颜色用于区分而非装饰。

### 6.2 色盲友好配色
Okabe-Ito / ColorBrewer Set2；叠加形状或直接标注作冗余（[[色盲友好与打印友好原则]]）。

### 6.3 医学研究推荐配色
病例/对照、暴露/未暴露用 [[医学二分类配色]] 固定映射（病例朱红、对照蓝）。

## 7. R 实现方案

### 7.1 推荐包
ggplot2、ggpubr、ggsci、ggbeeswarm、ggdist

### 7.2 关键参数
`geom_boxplot(outlier.shape=NA, width=)`（叠点时隐离群）、`geom_jitter(width=, alpha=)` / `geom_quasirandom()`、`scale_fill_manual`、`stat_compare_means()`。

### 7.3 基础代码模板
```r
library(ggplot2); library(ggpubr)
ggplot(df, aes(grp, value, fill = grp)) +
  geom_boxplot(width = .55, alpha = .85) +
  scale_fill_manual(values = okabe_ito) +
  labs(x = NULL, y = "BMI (kg/m²)") +
  theme_pub() + theme(legend.position = "none")
```

### 7.4 发表级代码模板
```r
library(ggbeeswarm)
ggplot(df, aes(grp, value, fill = grp)) +
  geom_boxplot(outlier.shape = NA, width = .55, alpha = .85) +
  geom_quasirandom(size = .7, alpha = .45, color = "grey25") +   # 叠原始点
  stat_compare_means(method = "wilcox.test", label = "p.format",
                     comparisons = list(c("No","Yes"))) +        # 仅预设比较
  scale_fill_manual(values = c(No = "#0072B2", Yes = "#D55E00")) +# 医学二分类
  scale_y_continuous(expand = expansion(mult = c(.02,.10))) +
  labs(x = NULL, y = "BMI (kg/m²)") +
  theme_pub() + theme(legend.position = "none")
```

## 8. Python 实现方案

### 8.1 推荐包
matplotlib、seaborn、plotnine

### 8.2 关键参数
`sns.boxplot(showfliers=False, width=)`、`sns.stripplot(jitter=, alpha=, size=)`、`palette=`、`linewidth`，导出 dpi 见 [[Python导出规范]]。

### 8.3 基础代码模板
```python
import seaborn as sns, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(3.5, 3))
sns.boxplot(data=df, x="grp", y="BMI", palette=okabe, width=.55, ax=ax)
ax.set_xlabel(None); ax.set_ylabel("BMI (kg/m²)")
```

### 8.4 发表级代码模板
```python
fig, ax = plt.subplots(figsize=(3.5, 3))
sns.boxplot(data=df, x="grp", y="BMI", showfliers=False, width=.55,
            palette={"No":"#0072B2","Yes":"#D55E00"}, linewidth=1, ax=ax)
sns.stripplot(data=df, x="grp", y="BMI", color="#333333",
              size=2.3, jitter=.18, alpha=.45, ax=ax)
ax.set_xlabel(None); ax.set_ylabel("BMI (kg/m²)")
# p 值用 statannotations 仅标预设比较（注意 seaborn 版本兼容）
```

## 9. 示例图像

### 9.1 网络优秀示例
见 [[Boxplot_优秀示例]]（≥2 个来源，含 R Graph Gallery 与 data-to-viz 的 boxplot+jitter 范式）。
本库自制范式图（合成数据，license 干净）：

![[demo_boxplot.png]]

### 9.2 Framingham 数据测试示例
✅ 已跑通（PREVHYP × BMI，箱线+jitter+Wilcoxon p）。代码见 [[R测试记录]] / [[Python测试记录]]，矢量图见 `07_示例图像库/Framingham测试图/`。

R（ggplot2 + ggpubr）：

![[fig_box_prevhyp_bmi_r.png]]

Python（seaborn）：

![[fig_box_prevhyp_bmi_py.png]]

> 结论：HTN 组 BMI 显著高于 No HTN（p < 0.001）。R 与 Python 结论一致。样本量大（n=4215），jitter 用 alpha≈0.15 防糊。

## 10. 常见错误
- 样本量很小仍只画箱体 → 分布信息不足。
- 分组颜色过多、过饱和。
- 轴标签缺单位（BMI 没写 kg/m²）。
- p 值标注过多造成混乱。
- 叠点时离群点画了两遍（忘了 `outlier.shape=NA` / `showfliers=False`）。

## 11. 自动返修规则
- x 轴标签重叠 → 旋转 30–45° 或改横向（`coord_flip`）。
- 每组 n < ~30 → 自动叠加原始点（jitter/beeswarm）。
- 组别 > 8 → 改横向或分面（[[分面与多面板设计]]）。
- 分布强偏态 → 提示 log 轴或改 violin/raincloud。
- p 值过多 → 全局检验 + 仅预设两两比较（[[标签与注释设计]]）。

## 12. 与其他图表的关系
- vs [[小提琴图_Violin]]：箱线给五数概括，小提琴给完整密度形态（双峰可见）。
- vs [[雨云图_Raincloud]]：雨云= 半小提琴 + 箱 + 点，信息最全。
- vs 柱状图：柱状(均值±SD)隐藏分布、易误导；箱线展示分布。
- vs [[点估计置信区间图_PointRange]]：后者聚焦“均值 + 不确定性”，前者展示“整组分布”。

## 13. 质量检查清单
- [ ] 展示了原始数据或足够分布信息？
- [ ] 颜色合理且色盲友好？
- [ ] 轴标签清楚、有单位？
- [ ] 图例是否必要（两组可去）？
- [ ] p 值是否克制、格式统一？
- [ ] 适合论文导出（矢量、尺寸）？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建立初稿（全 14 节）| 缺 Framingham 实测图 | 跑 PREVHYP×BMI 测试，升 tested |

相关：[[小提琴图_Violin]] · [[雨云图_Raincloud]] · [[点估计置信区间图_PointRange]] · [[分类变量配色]] · [[seaborn统计图模板]] · [[ggplot2参数系统]]
