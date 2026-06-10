#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""小提琴图（内嵌箱线）—— 卡片 02_图表类型知识卡片/01_分布图/小提琴图_Violin.md
合成数据，可独立运行。改 # >>> PARAM 区换数据/列/配色。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_violin"
TITLE = "Violin (inner box)"; XLAB = None; YLAB = "Value"
PALETTE = "cat_main"
FIGSIZE = (3.4, 2.9)
X, Y = "grp", "val"
N = 200
df = pd.DataFrame({X: np.repeat(["A", "B", "C"], N),
                   Y: np.concatenate([np.random.normal(0, 1, N),
                                      np.random.normal(.8, 1.2, N),
                                      np.concatenate([np.random.normal(-.5, .5, N // 2),
                                                      np.random.normal(2, .6, N - N // 2)])])})
# <<< PARAM ------------------------------------------------------

colors = pal(PALETTE)
fig, ax = plt.subplots(figsize=FIGSIZE)
sns.violinplot(data=df, x=X, y=Y, hue=X, palette=colors[:df[X].nunique()],
               legend=False, inner="box", cut=0, ax=ax)
ax.set_title(TITLE); ax.set_xlabel(XLAB); ax.set_ylabel(YLAB)
save_fig(fig, NAME)
