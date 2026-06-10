#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""柱状图 —— 卡片 02_组间比较图/柱状图_Bar.md
默认百分比堆叠（构成比）；MODE 可切 count(计数) / stack(堆叠) / fill(百分比堆叠)。合成数据，可独立运行。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_bar"
TITLE = "Composition by group (100% stacked)"; XLAB = None; YLAB = "Proportion"
MODE = "fill"                 # count | stack | fill
PALETTE = "cat_main"
FIGSIZE = (3.6, 3.0)
GROUP, SUB = "grp", "sub"     # x 轴分组 / 堆叠子类
df = pd.DataFrame({
    GROUP: np.random.choice(["Group 1", "Group 2", "Group 3"], 600),
    SUB:   np.random.choice(["Mild", "Moderate", "Severe"], 600, p=[.5, .3, .2])})
# <<< PARAM ------------------------------------------------------

ct = df.groupby([GROUP, SUB]).size().unstack(fill_value=0)
subs = list(ct.columns); colors = pal(PALETTE)
mat = ct.values.astype(float)
if MODE == "fill":
    mat = mat / mat.sum(axis=1, keepdims=True)
fig, ax = plt.subplots(figsize=FIGSIZE)
x = np.arange(len(ct.index))
if MODE == "count":           # 并排
    w = .8 / len(subs)
    for j, s in enumerate(subs):
        ax.bar(x + j * w, mat[:, j], w, label=s, color=colors[j])
    ax.set_xticks(x + w * (len(subs) - 1) / 2)
else:                         # 堆叠 / 百分比堆叠
    bottom = np.zeros(len(ct.index))
    for j, s in enumerate(subs):
        ax.bar(x, mat[:, j], .6, bottom=bottom, label=s, color=colors[j])
        bottom += mat[:, j]
    ax.set_xticks(x)
ax.set_xticklabels(ct.index); ax.grid(False, axis="x")
ax.set_title(TITLE); ax.set_xlabel(XLAB); ax.set_ylabel(YLAB)
ax.legend(title=None, fontsize=8)
save_fig(fig, NAME)
