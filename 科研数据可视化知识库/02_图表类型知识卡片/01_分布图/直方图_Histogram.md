---
chart_name: 直方图
chart_name_en: Histogram
chart_family: 分布图
data_type:
  - continuous
recommended_backend:
  r: ggplot2
  python: seaborn/matplotlib
difficulty: basic
priority: high
status: tested
tags:
  - dataviz
  - chart
  - histogram
  - distribution
  - r
  - python
---

# 直方图 Histogram

> 把单个连续变量分箱计数，看它的**分布形状**：集中趋势、离散、偏态、峰数、离群。最基础的探索性分布图。

## 1. 图表定位

回答“**这个连续变量长什么样**”——是否正态/偏态、单峰还是多峰、有无异常值。是几乎所有定量分析的第一张图。

## 2. 适用场景

- 单个连续变量的分布探查（TOTCHOL、BMI、GLUCOSE）。
- 建模前检查正态性/偏态，决定是否变换（log）。
- 配核密度曲线（KDE）兼顾“离散计数”与“平滑形态”。
- 样本量较大（≳ 100），分箱才稳定。

## 3. 不适用场景

- 多组分布对比 → 叠太多直方图会糊，改 [[密度图_Density]] / [[山峦图_Ridgeline]] / [[箱线图_Boxplot]]。
- 样本量很小（< 30）→ 分箱噪声大，改点图/密度（带 rug）。
- 离散/分类变量 → 用 [[柱状图_Bar]]（直方图是连续分箱，不是计数柱）。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| value | continuous | 要看分布的连续变量 | 必需 |
| group | categorical | 可选：分面/分组 | 可选 |

长格式，每行一个观测。

## 5. 图表架构选择

### 5.1 基础架构
- x：连续变量分箱；y：频数（count）或密度（density）。
- 分箱数（bins）或带宽是关键参数；默认 30–50，按样本量与范围调。

### 5.2 高质量架构
- 叠加 KDE 曲线 → y 用 density（计数与密度不可混轴）。
- 想比较少数几组 → 半透明叠加或分面（[[分面与多面板设计]]）；组多改 [[山峦图_Ridgeline]]。
- 偏态强 → log x 轴并注明。
- 底部加 rug 显示原始点密度。

## 6. 配色选择

### 6.1 默认配色
单变量单色即可（`cat_main` 取一色作填充 + 深一档作 KDE 线），见 [[分类变量配色]]。不要给单变量上花哨渐变。

### 6.2 色盲友好配色
单色或 Okabe-Ito；多组叠加时用半透明 + 描边区分（[[色盲友好与打印友好原则]]）。

### 6.3 医学研究推荐配色
分两组（病例/对照）叠加时用 [[医学二分类配色]]，并降低 alpha 防遮挡。

## 7. R 实现方案

### 7.1 推荐包
ggplot2

### 7.2 关键参数
`geom_histogram(aes(y=after_stat(density)), bins=)`、`geom_density()`、`binwidth`、`scale_x_log10()`。

### 7.3 可执行模板
**`templates/r/histogram.R`**（改顶部 `# >>> PARAM` 即可）。核心：
```r
ggplot(df, aes(x)) +
  geom_histogram(aes(y = after_stat(density)), bins = 40, fill = pal("cat_main")[2], color = "white") +
  geom_density(color = pal("cat_main")[5], linewidth = 1) +
  labs(x = "Value", y = "Density")
```

## 8. Python 实现方案

### 8.1 推荐包
seaborn、matplotlib

### 8.2 关键参数
`sns.histplot(stat="density", bins=, kde=True)` 或 `ax.hist(density=True)` + `sns.kdeplot()`。

### 8.3 可执行模板
**`templates/python/histogram.py`**。核心：
```python
sns.histplot(x, bins=40, stat="density", color=pal("cat_main")[1], edgecolor="white", ax=ax)
sns.kdeplot(x, color=pal("cat_main")[4], ax=ax)
```

## 9. 示例图像

### 9.1 网络优秀示例
参考 data-to-viz / R Graph Gallery 的 histogram 范式（分箱 + 可选 KDE）。

### 9.2 本库模板 demo（合成数据，双后端对齐）
Python（seaborn）：

![[tpl_histogram_py.png]]

R（ggplot2）：

![[tpl_histogram_r.png]]

> 直方图 + KDE 双后端一致：单峰近正态。可直接套 Framingham 的 TOTCHOL/BMI（连续变量）。

## 10. 常见错误
- 叠 KDE 却用 count 轴（计数与密度混轴，曲线被压扁）。
- bins 太少（丢形态）或太多（全是噪声毛刺）。
- 多组重叠不透明，互相遮挡。
- 把分类变量画成直方图（应是 [[柱状图_Bar]]）。
- 轴无单位。

## 11. 自动返修规则
- 叠 KDE → 自动切 y 为 density。
- bins 未指定 → 按样本量给默认（如 `ceil(sqrt(n))` 或 Freedman–Diaconis）。
- 偏态强（|skew|>1）→ 提示 log 轴。
- 组 > 3 重叠 → 改分面或 [[山峦图_Ridgeline]]。

## 12. 与其他图表的关系
- vs [[密度图_Density]]：直方给“离散计数+分箱”，密度给“平滑形态”；常叠加。
- vs [[箱线图_Boxplot]]：箱线给概括，直方给完整形状。
- vs [[柱状图_Bar]]：直方=连续分箱，柱状=分类计数，**勿混**。
- vs [[山峦图_Ridgeline]]：多组分布对比首选山峦。

## 13. 质量检查清单
- [ ] bins/带宽合理，形态不失真？
- [ ] 叠 KDE 时 y 为 density？
- [ ] 轴标签有单位？
- [ ] 多组是否半透明可辨？
- [ ] 偏态是否处理（log/注明）？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建卡 + 双后端可执行模板 + demo 图，状态 tested | — | 可补 Framingham TOTCHOL 实测 |

相关：[[密度图_Density]] · [[山峦图_Ridgeline]] · [[箱线图_Boxplot]] · [[柱状图_Bar]] · [[分类变量配色]]
