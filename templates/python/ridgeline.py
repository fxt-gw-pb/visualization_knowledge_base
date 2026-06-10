#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""山峦图 / ridgeline（多组密度纵向堆叠）—— 卡片 01_分布图/山峦图_Ridgeline.md
matplotlib 手搓（不依赖 joypy）。合成数据，可独立运行。改 # >>> PARAM 区。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy import stats
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_ridgeline"
TITLE = "Ridgeline: value across groups"; XLAB = "Value"
PALETTE = "cat_main"; OVERLAP = 1.4      # >1 让相邻山峦重叠
FIGSIZE = (3.8, 3.4)
X, GROUP = "val", "grp"
groups = [f"Grp {i}" for i in range(1, 7)]
df = pd.concat([pd.DataFrame({GROUP: g, X: np.random.normal(i * .8, 1, 300)})
                for i, g in enumerate(groups)], ignore_index=True)
# <<< PARAM ------------------------------------------------------

colors = pal(PALETTE)
fig, ax = plt.subplots(figsize=FIGSIZE)
for i, g in enumerate(groups):                      # 自下而上
    v = df.loc[df[GROUP] == g, X].values
    k = stats.gaussian_kde(v); xs = np.linspace(df[X].min(), df[X].max(), 200)
    ys = k(xs); ys = ys / ys.max() * OVERLAP
    ax.fill_between(xs, i, i + ys, color=colors[i % len(colors)], alpha=.75, lw=.8, ec="white")
    ax.plot(xs, i + ys, color="white", lw=.6)
ax.set_yticks(range(len(groups))); ax.set_yticklabels(groups)
ax.set_xlabel(XLAB); ax.set_ylabel(None); ax.set_title(TITLE); ax.grid(False)
save_fig(fig, NAME)
