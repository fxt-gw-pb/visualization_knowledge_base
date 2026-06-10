---
title: matplotlib 通用主题
type: code-template
status: active
backend: python
updated: 2026-06-10
tags:
  - dataviz
  - python
  - matplotlib
  - theme
  - template
---

# matplotlib 通用主题

> Python 端发表级 + 汇报级 `rcParams` 预设，供所有 Python 卡片复用。对应 R 的 [[ggplot2通用主题]]。

## 1. 设计原则

- 去重网格、刻度朝内、无衬线、统一字号 → 高数据墨水比 + 全 figure 一致。
- 主题与配色解耦：颜色走 [[配色系统总览]]。
- 通过 `rcParams` 一次设定，后续所有图继承。

## 2. 发表级 rcParams

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

def set_pub_style(base=9):                       # >>> PARAM base font size
    mpl.rcParams.update({
        "figure.dpi": 120,
        "savefig.dpi": 600,
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": base,
        "axes.titlesize": base + 2,
        "axes.labelsize": base + 1,
        "axes.linewidth": 0.6,
        "axes.spines.top": False,                # 去上右边框
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#ECECEC",
        "grid.linewidth": 0.5,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.labelsize": base - 1,
        "ytick.labelsize": base - 1,
        "legend.frameon": False,
        "legend.fontsize": base - 1,
        "lines.linewidth": 1.0,
        "savefig.bbox": "tight",
    })

set_pub_style()
```

## 3. 汇报级（放大）

```python
def set_talk_style(base=16):                     # >>> PARAM 放大
    set_pub_style(base)
    mpl.rcParams.update({
        "lines.linewidth": 2.2,
        "axes.linewidth": 1.0,
        "savefig.transparent": True,             # 深色 slide
    })
```

## 4. 论文风一键方案：SciencePlots（可选）

```python
import scienceplots
plt.style.use(["science", "nature"])             # 见 SciencePlots模板
# 无 LaTeX 环境： plt.style.use(["science", "no-latex"])
```
详见 [[SciencePlots模板]]。

## 5. 配色接入

```python
okabe_ito = ["#E69F00","#56B4E9","#009E73","#F0E442",
             "#0072B2","#D55E00","#CC79A7","#999999"]
mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=okabe_ito)  # 默认分类循环色
# seaborn： sns.set_palette(okabe_ito)
```
连续/发散见 [[连续变量配色]] / [[发散变量配色]]。

## 6. 用法示例

```python
set_pub_style()
fig, ax = plt.subplots(figsize=(3.5, 2.8))       # 单栏英寸
ax.scatter(df.x, df.y, color="#0072B2", s=10, alpha=.6)
ax.set_xlabel("Weight (1000 lbs)"); ax.set_ylabel("MPG")
fig.savefig("demo.pdf")                          # 矢量
```

## 7. 与其他文件的关系

- 统计图快速封装 → [[seaborn统计图模板]]
- ggplot 语法 → [[plotnine模板]]
- 论文样式 → [[SciencePlots模板]]
- 多面板 → [[多面板组合图_MultiPanel]]
- 导出 → [[Python导出规范]]

相关：[[seaborn统计图模板]] · [[SciencePlots模板]] · [[Python导出规范]] · [[ggplot2通用主题]]（R 对应）
