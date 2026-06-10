---
chart_name: 山峦图
chart_name_en: Ridgeline plot
chart_family: 分布图
data_type:
  - continuous
  - categorical_group
recommended_backend:
  r: ggdist (ggridges 可选)
  python: matplotlib (手搓)
difficulty: intermediate
priority: medium
status: tested
tags:
  - dataviz
  - chart
  - ridgeline
  - joyplot
  - distribution
  - r
  - python
---

# 山峦图 Ridgeline plot

> 把**多组密度曲线纵向错开、轻微重叠**地堆起来（俗称 joyplot），在一张紧凑图里比较很多组的分布形态/位移。

## 1. 图表定位

回答“**很多组（5–20）之间，某连续变量的分布如何逐组移动/变形**”。比叠在一起的密度图省空间、更易读趋势。

## 2. 适用场景

- 组数较多（≳ 5），密度叠加会糊时。
- 组间存在**有序/可排序**关系（时间、剂量、年龄段、地区），错开后能看出整体位移。
- 想兼顾“每组形态”与“跨组趋势”。

## 3. 不适用场景

- 只有 2–3 组 → 直接 [[密度图_Density]] 叠加更直接。
- 组无序且无趋势 → 错开顺序无意义，信息密度低。
- 需要精确数值比较 → 用 [[箱线图_Boxplot]] / [[点估计置信区间图_PointRange]]。
- 每组样本量很小 → 密度不稳。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| value | continuous | 连续变量（x）| 必需 |
| group | categorical（最好有序）| 分组（y，逐行错开）| 必需 |

长格式。group 的因子顺序决定堆叠顺序——**先排好序**。

## 5. 图表架构选择

### 5.1 基础架构
- x：连续变量；y：分组（每组一条密度脊）；相邻脊按 `height/scale` 重叠。

### 5.2 高质量架构
- 重叠量适中（能看出形态又不过度遮挡）。
- 可按填充色映射 x 值（温度/数值梯度）增强可读，用 [[连续变量配色]]。
- 顶/底组留白避免裁切。
- 想要分位线/中位点 → ggdist 的 slab+interval。

## 6. 配色选择

### 6.1 默认配色
逐组分类色（`cat_main`）或——若 group 有序——用顺序色阶 [[连续变量配色]]（`seq_viridis`）表达“逐组渐变”。

### 6.2 色盲友好配色
viridis/Okabe-Ito；白色描边分隔相邻脊。

### 6.3 医学研究推荐配色
按年龄段/随访期等有序变量 → 顺序色阶；分类暴露 → Okabe-Ito。

## 7. R 实现方案

### 7.1 推荐包
ggdist（`stat_slab`，本库默认，免装 ggridges）；或 ggridges（`geom_density_ridges`）。

### 7.2 关键参数
`stat_slab(height=, normalize="groups")`、因子顺序、`scale_fill_manual`。

### 7.3 可执行模板
**`templates/r/ridgeline.R`**（用 ggdist，无需 ggridges）。核心：
```r
ggplot(df, aes(x = val, y = grp, fill = grp)) +
  ggdist::stat_slab(height = 1.6, color = "white", normalize = "groups") +
  scale_fill_manual(values = pal("cat_main"))
```

## 8. Python 实现方案

### 8.1 推荐包
matplotlib（手搓 `gaussian_kde` + 偏移叠放，免装 joypy）；seaborn FacetGrid 亦可。

### 8.2 关键参数
逐组 `gaussian_kde` → 归一到统一高度 → `fill_between(offset+ys)`；`OVERLAP` 控重叠。

### 8.3 可执行模板
**`templates/python/ridgeline.py`**。核心见文件 `# >>> PARAM`，`OVERLAP>1` 即重叠。

## 9. 示例图像

### 9.1 网络优秀示例
参考 ggridges / joypy 经典 joyplot 范式（如月度温度分布）。

### 9.2 本库模板 demo（合成数据，双后端对齐）
Python（matplotlib 手搓）：

![[tpl_ridgeline_py.png]]

R（ggdist stat_slab）：

![[tpl_ridgeline_r.png]]

> 六组均值逐级右移，山峦清晰错开，整体位移一目了然；双后端形态一致。

## 10. 常见错误
- 组无序却用山峦——错开顺序无意义。
- 重叠过度，脊互相吞没。
- 顶/底脊被画布裁切。
- 各组样本量过小，密度抖动当成真实形态。

## 11. 自动返修规则
- 组 ≤ 3 → 建议改 [[密度图_Density]]。
- group 可识别为有序 → 自动按序排列 + 顺序色阶。
- 顶部裁切 → 自动扩 y 上限留白。
- 重叠过度 → 调小 height/scale。

## 12. 与其他图表的关系
- vs [[密度图_Density]]：少组叠加用密度，多组错开用山峦。
- vs [[箱线图_Boxplot]]：箱线给概括与离群，山峦给完整形态趋势。
- vs [[小提琴图_Violin]]：小提琴并排镜像密度，山峦纵向错开、更省空间。

## 13. 质量检查清单
- [ ] 分组顺序有意义（有序）？
- [ ] 重叠量适中、可辨形态？
- [ ] 顶底无裁切？
- [ ] 配色对“有序/分类”语义正确？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建卡 + 双后端可执行模板（R 用 ggdist 免依赖）+ demo 图，状态 tested | — | 如需可加 ggridges 备选模板 |

相关：[[密度图_Density]] · [[小提琴图_Violin]] · [[箱线图_Boxplot]] · [[连续变量配色]]
