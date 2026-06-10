---
chart_name: 柱状图
chart_name_en: Bar plot
chart_family: 组间比较图
data_type:
  - categorical_group
  - count_or_proportion
recommended_backend:
  r: ggplot2
  python: matplotlib/seaborn
difficulty: basic
priority: high
status: tested
tags:
  - dataviz
  - chart
  - bar
  - stacked
  - composition
  - r
  - python
---

# 柱状图 Bar plot

> 用柱高表示**分类变量的计数或构成比**。含三种常用变体：分组（并排）、堆叠（计数）、百分比堆叠（构成比 100%）。

## 1. 图表定位

回答“**各类别有多少 / 各组的构成比例如何**”。处理**离散/分类**数据（区别于连续分箱的 [[直方图_Histogram]]）。

## 2. 适用场景

- 分类变量计数（各诊断、各分期人数）。
- 组×子类构成比（各组的严重度构成）→ 百分比堆叠。
- 少数类别（≤ ~8）、需精确读数。
- 流行病学：各组危险因素阳性率、构成比。

## 3. 不适用场景

- 表达连续变量分布 → [[直方图_Histogram]] / [[密度图_Density]]。
- 用柱高表示“均值±SD”掩盖分布 → 改 [[箱线图_Boxplot]] / [[点估计置信区间图_PointRange]]（“dynamite plot”是反模式）。
- 类别很多 → 改横向柱 + 排序，或棒棒糖图（lollipop，规划中）。
- 堆叠层数过多（>5）→ 难比较，改分面或百分比堆叠 + 精选类别。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| group | categorical | x 轴主分类 | 必需 |
| sub | categorical | 堆叠/并排的子类 | 堆叠/分组时必需 |
| count/prop | numeric | 已聚合的计数/比例（也可由原始数据自动统计）| 可选 |

可给原始长格式（自动计数）或已聚合表。

## 5. 图表架构选择

### 5.1 基础架构
- x：类别；y：计数或比例；`position` 决定变体：
  - `dodge`（并排）：比较各子类绝对量。
  - `stack`（堆叠）：看总量 + 构成绝对量。
  - `fill`（百分比堆叠）：只看**构成比**，各柱等高=100%。

### 5.2 高质量架构
- 比较“比例”用 `fill`；比较“绝对量”用 `dodge`。
- 类别按数值排序（除非有自然顺序）。
- 柱顶可标数值/百分比；y 从 0 开始（柱图必须）。
- 误差棒只在 y 是估计量（均值/率）时加，并说明含义。

## 6. 配色选择

### 6.1 默认配色
子类用分类色 `cat_main`（Okabe-Ito），见 [[分类变量配色]]；有序子类（轻/中/重）可用顺序色阶。

### 6.2 色盲友好配色
Okabe-Ito / Set2；堆叠层间白描边分隔。

### 6.3 医学研究推荐配色
严重度等有序子类 → 顺序色（浅→深 = 轻→重）；二分结局 → [[医学二分类配色]]。

## 7. R 实现方案

### 7.1 推荐包
ggplot2

### 7.2 关键参数
`geom_bar(position = "fill"/"stack"/position_dodge())`、`width`、白描边、`scale_fill_manual`。

### 7.3 可执行模板
**`templates/r/bar.R`**（`MODE` 切 count/stack/fill）。核心：
```r
ggplot(df, aes(grp, fill = sub)) +
  geom_bar(position = "fill", width = .65, color = "white") +   # 百分比堆叠
  scale_fill_manual(values = pal("cat_main"))
```

## 8. Python 实现方案

### 8.1 推荐包
matplotlib（堆叠用 `bottom` 累加）、seaborn（`countplot`/`barplot`）

### 8.2 关键参数
分组聚合 → `ax.bar(..., bottom=)` 累加堆叠；`fill` 模式先按行归一。

### 8.3 可执行模板
**`templates/python/bar.py`**（`MODE` = count/stack/fill）。核心见文件 `# >>> PARAM`。

## 9. 示例图像

### 9.1 网络优秀示例
参考 data-to-viz 的 stacked / grouped / percent-stacked barplot 三变体范式。

### 9.2 本库模板 demo（合成数据，双后端对齐）
Python（matplotlib）：

![[tpl_bar_py.png]]

R（ggplot2）：

![[tpl_bar_r.png]]

> 百分比堆叠（构成比）：三组的严重度构成一目了然，各柱等高=100%；双后端一致。改 `MODE` 即得并排/堆叠计数。

## 10. 常见错误
- 用柱高表示均值并省略分布（dynamite plot）。
- 百分比堆叠却想读绝对量（应配 `stack` 或标 n）。
- y 轴不从 0（柱图比较的是“高度面积”，截断会误导）。
- 堆叠层数过多、颜色过饱和。
- 把连续变量当类别画柱。

## 11. 自动返修规则
- 目的=比例 → 用 `fill`；目的=绝对量 → `stack`/`dodge`。
- 类别 > 8 或标签重叠 → 横向 + 排序。
- y 轴被截断 → 强制从 0。
- 堆叠层 > 5 → 合并低频为 “Other” 或分面。
- y 是均值/率 → 提示加误差棒并注明含义（或改点估计图）。

## 12. 与其他图表的关系
- vs [[直方图_Histogram]]：直方=连续分箱，柱状=分类计数。
- vs [[箱线图_Boxplot]]/[[点估计置信区间图_PointRange]]：表达连续结局组差异用后两者，别用均值柱。
- vs 饼图：构成比优先用百分比堆叠柱（更易比较），少用饼图。

## 13. 质量检查清单
- [ ] 变体（dodge/stack/fill）匹配目的（绝对量 vs 比例）？
- [ ] y 轴从 0？
- [ ] 类别排序合理？
- [ ] 颜色数量受控、色盲友好？
- [ ] 误差棒（若有）含义说明？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建卡（含三变体）+ 双后端可执行模板 + demo 图，状态 tested | — | 可补 Framingham 吸烟×性别构成实测 |

相关：[[直方图_Histogram]] · [[箱线图_Boxplot]] · [[点估计置信区间图_PointRange]] · [[分类变量配色]]
