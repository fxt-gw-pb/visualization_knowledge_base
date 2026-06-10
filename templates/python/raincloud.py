#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""雨云图（云=半边密度 + 箱 + 雨=抖动点）—— 卡片 01_分布图/雨云图_Raincloud.md
合成数据，可独立运行。matplotlib 手搓（不依赖 ptitprince）。改 # >>> PARAM 区。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy import stats
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_raincloud"
TITLE = "Raincloud (cloud + box + rain)"; XLAB = None; YLAB = "Value"
PALETTE = "cat_main"
FIGSIZE = (3.8, 3.0)
X, Y = "grp", "val"
N = 200
groups = ["A", "B", "C"]
df = pd.DataFrame({X: np.repeat(groups, N),
                   Y: np.concatenate([np.random.normal(0, 1, N),
                                      np.random.normal(.8, 1.2, N),
                                      np.random.normal(.3, .9, N)])})
# <<< PARAM ------------------------------------------------------

colors = pal(PALETTE)
fig, ax = plt.subplots(figsize=FIGSIZE)
for i, gname in enumerate(groups):
    v = df.loc[df[X] == gname, Y].values
    k = stats.gaussian_kde(v); xs = np.linspace(v.min(), v.max(), 120)
    ys = k(xs); ys = ys / ys.max() * .35
    ax.fill_betweenx(xs, i, i + ys, color=colors[i], alpha=.5, lw=0)
    q1, m, q3 = np.percentile(v, [25, 50, 75])
    ax.add_patch(plt.Rectangle((i - .07, q1), .14, q3 - q1, fill=True,
                               fc="white", ec="k", lw=.8, zorder=3))
    ax.plot([i - .07, i + .07], [m, m], c="k", lw=1.2, zorder=4)
    ax.scatter(i - .17 + np.random.uniform(-.05, .05, len(v)), v,
               s=3, color=colors[i], alpha=.25, zorder=2)
ax.set_xticks(range(len(groups))); ax.set_xticklabels(groups)
ax.set_title(TITLE); ax.set_xlabel(XLAB); ax.set_ylabel(YLAB)
save_fig(fig, NAME)
