#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""折线趋势 + 95%CI 带 —— 卡片 04_时间趋势图/折线趋势图_Line.md
合成数据，可独立运行。改 # >>> PARAM 区换数据/列/配色。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_line"
TITLE = "Mean ± 95% CI trend"; XLAB = "Time"; YLAB = "Value"
PALETTE = "cat_main"          # 取前 N 类
FIGSIZE = (3.7, 2.8)
T, Y, GROUP = "t", "y", "grp"
rows = []
for gi, (g, base) in enumerate([("Group 1", 0), ("Group 2", 2)]):
    for _ in range(30):
        rows += [(g, ti, base + 0.4 * ti + np.random.normal(0, 1.2)) for ti in range(10)]
df = pd.DataFrame(rows, columns=[GROUP, T, Y])
# <<< PARAM ------------------------------------------------------

colors = pal(PALETTE)
levels = list(dict.fromkeys(df[GROUP]))
palette = {lv: colors[i] for i, lv in enumerate(levels)}
fig, ax = plt.subplots(figsize=FIGSIZE)
sns.lineplot(data=df, x=T, y=Y, hue=GROUP, errorbar=("ci", 95), marker="o",
             palette=palette, ax=ax)
ax.set_title(TITLE); ax.set_xlabel(XLAB); ax.set_ylabel(YLAB)
ax.legend(title=None, fontsize=8)
save_fig(fig, NAME)
