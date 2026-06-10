---
title: seaborn 统计图模板
type: code-template
status: active
backend: python
updated: 2026-06-10
tags:
  - dataviz
  - python
  - seaborn
  - template
---

# seaborn 统计图模板

> Python 端统计图主力，一行出图 + 美观默认；返回 matplotlib Axes 可继续精修。配合各分布/组间/相关卡片。

## 1. 通用骨架

```python
import seaborn as sns, matplotlib.pyplot as plt
set_pub_style()                       # 见 matplotlib通用主题
okabe = ["#E69F00","#56B4E9","#009E73","#0072B2","#D55E00"]

fig, ax = plt.subplots(figsize=(3.5, 3))
sns.<plot>(data=df, x="...", y="...", hue="...", palette=okabe, ax=ax)  # >>> PARAM
ax.set_xlabel("..."); ax.set_ylabel("...")
fig.savefig("fig.pdf")
```

## 2. 各图类型速查

| 图 | 函数 | 关键参数 | 卡片 |
|---|---|---|---|
| 箱线 | `sns.boxplot` | `showfliers=False`(叠点时), `width` | [[箱线图_Boxplot]] |
| 箱线+点 | `boxplot` + `stripplot(jitter=True, alpha=.5)` | 叠加顺序 | [[箱线图_Boxplot]] |
| 小提琴 | `sns.violinplot` | `inner="box"/"quartile"`, `cut`, `bw_adjust` | [[小提琴图_Violin]] |
| 散点 | `sns.scatterplot` | `alpha`, `size`, `hue` | [[散点图_Scatter]] |
| 散点+回归 | `sns.regplot`/`lmplot` | `order`, `lowess=True`, `ci` | [[散点图_Scatter]] |
| 折线 | `sns.lineplot` | `errorbar=("ci",95)`, `estimator` | [[折线趋势图_Line]] |
| 密度 | `sns.kdeplot` | `fill`, `bw_adjust`, `common_norm` | (分布族) |
| 直方 | `sns.histplot` | `bins`, `stat="density"`, `kde=True` | (分布族) |
| 热图 | `sns.heatmap` | `cmap`, `center=0`, `annot` | [[热图_Heatmap]] |
| 成对 | `sns.pairplot` | `corner=True`, `hue` | (相关族) |
| 蜂群 | `sns.swarmplot` | 小样本叠点 | [[箱线图_Boxplot]] |

## 3. 箱线 + 抖动点（最常用组合）

```python
fig, ax = plt.subplots(figsize=(3.5, 3))
sns.boxplot(data=df, x="grp", y="BMI", showfliers=False,
            width=.55, color="white", linewidth=1, ax=ax)
sns.stripplot(data=df, x="grp", y="BMI", color="#333333",
              size=2.5, jitter=.18, alpha=.5, ax=ax)   # 叠原始点
ax.set_ylabel("BMI (kg/m²)"); ax.set_xlabel(None)
```

## 4. 组间 p 值（statannotations，注意版本兼容）

```python
from statannotations.Annotator import Annotator
pairs = [("A","B")]                     # 只标预设比较
ann = Annotator(ax, pairs, data=df, x="grp", y="BMI")
ann.configure(test="Mann-Whitney", text_format="full", loc="inside")
ann.apply_and_annotate()
```
> 与新版 seaborn 兼容性敏感，固定 seaborn 版本或改手动标注（[[标签与注释设计]]）。

## 5. seaborn objects 接口（v0.12+，图形语法味）

```python
import seaborn.objects as so
(so.Plot(df, x="grp", y="BMI", color="grp")
   .add(so.Dots(alpha=.4), so.Jitter())
   .add(so.Range(), so.Est(errorbar="ci"))    # 点估计+CI
   .label(y="BMI (kg/m²)"))
```

## 6. 配色接入

- 分类 `palette=okabe`（[[分类变量配色]]）；连续 `cmap="viridis"`；发散 `cmap="RdBu_r", center=0`。
- 医学二分类用固定映射 dict（[[医学二分类配色]]）。

## 7. 常见错误（→ 返修）

- ❌ 箱线叠点时离群点画两遍 → `showfliers=False`。
- ❌ 散点重叠 → `alpha` / 改 hexbin（[[散点图_Scatter]]）。
- ❌ p 值满天飞 → 只标预设比较。
- ❌ 用默认调色板未过色盲检查 → 换 Okabe-Ito/viridis。
- ❌ 轴标签缺单位。

相关：[[matplotlib通用主题]] · [[plotnine模板]] · [[配色系统总览]] · [[Python导出规范]]
