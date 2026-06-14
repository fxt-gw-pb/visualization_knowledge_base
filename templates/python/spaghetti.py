#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""个体轨迹 Spaghetti 图（纵向）+ 组均值 95%CI —— 卡片 04_时间趋势图/个体轨迹图_Spaghetti.md
合成纵向数据（每人多次随访），细线=个体，粗线=组均值。改 # >>> PARAM 区。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_spaghetti"
TITLE = "Individual trajectories"; XLAB = "Visit"; YLAB = "Biomarker"
PALETTE = "cat_main"
FIGSIZE = (4.0, 3.0)
ID, T, Y, GROUP = "id", "visit", "y", "grp"
# 换真实数据： 长格式 df[ID,T,Y,GROUP]（每人多行）
rows = []
for g, (slope, base) in {"Treatment": (-0.6, 10), "Control": (-0.1, 10)}.items():
    for i in range(25):
        r0 = base + np.random.normal(0, 1.2); s = slope + np.random.normal(0, 0.25)
        for t in range(5):
            rows.append((f"{g}_{i}", t, r0 + s * t + np.random.normal(0, 0.4), g))
df = pd.DataFrame(rows, columns=[ID, T, Y, GROUP])
# <<< PARAM ------------------------------------------------------

colors = pal(PALETTE); levels = list(dict.fromkeys(df[GROUP]))
cmap = {lv: colors[i] for i, lv in enumerate(levels)}
fig, ax = plt.subplots(figsize=FIGSIZE)
for _, sub in df.groupby(ID):
    ax.plot(sub[T], sub[Y], color=cmap[sub[GROUP].iloc[0]], lw=.5, alpha=.22)
for g, sub in df.groupby(GROUP):
    m = sub.groupby(T)[Y].agg(["mean", "count", "std"])
    se = m["std"] / np.sqrt(m["count"])
    ax.fill_between(m.index, m["mean"] - 1.96 * se, m["mean"] + 1.96 * se, color=cmap[g], alpha=.2)
    ax.plot(m.index, m["mean"], color=cmap[g], lw=2.2, label=g)
ax.set_xlabel(XLAB); ax.set_ylabel(YLAB); ax.set_title(TITLE); ax.grid(False)
ax.legend(fontsize=8)
save_fig(fig, NAME)
