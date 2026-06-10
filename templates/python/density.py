#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""密度图（分组 KDE 叠加）—— 卡片 01_分布图/密度图_Density.md
合成数据，可独立运行。改 # >>> PARAM 区换数据/分组/配色。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_density"
TITLE = "Density by group"; XLAB = "Value"; YLAB = "Density"
PALETTE = "cat_main"
FIGSIZE = (3.7, 2.9)
X, GROUP = "val", "grp"
df = pd.DataFrame({GROUP: np.repeat(["A", "B", "C"], 400),
                   X: np.concatenate([np.random.normal(0, 1, 400),
                                      np.random.normal(1.5, 1, 400),
                                      np.random.normal(3, 1.3, 400)])})
# <<< PARAM ------------------------------------------------------

colors = pal(PALETTE)
levels = list(dict.fromkeys(df[GROUP]))
palette = {lv: colors[i] for i, lv in enumerate(levels)}
fig, ax = plt.subplots(figsize=FIGSIZE)
sns.kdeplot(data=df, x=X, hue=GROUP, fill=True, alpha=.35, palette=palette,
            common_norm=False, ax=ax)
ax.set_title(TITLE); ax.set_xlabel(XLAB); ax.set_ylabel(YLAB)
save_fig(fig, NAME)
