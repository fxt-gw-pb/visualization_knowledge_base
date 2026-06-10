#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""散点图 + 回归线 + r —— 卡片 03_相关性图/散点图_Scatter.md
合成数据，可独立运行。改 # >>> PARAM 区换数据/列/配色。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, seaborn as sns, matplotlib.pyplot as plt
from scipy import stats
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_scatter"
TITLE = "Scatter + regression"; XLAB = "x"; YLAB = "y"
PT_COLOR = pal("med_case_control")["low"]    # 点：中性蓝
LINE_COLOR = pal("med_case_control")["high"]  # 回归线：朱红
FIGSIZE = (3.4, 3.0)
# 换真实数据： x = df["colx"].values; y = df["coly"].values
x = np.random.normal(0, 1, 400)
y = 1.2 * x + np.random.normal(0, 1, 400)
# <<< PARAM ------------------------------------------------------

fig, ax = plt.subplots(figsize=FIGSIZE)
sns.regplot(x=x, y=y, scatter_kws=dict(alpha=.3, s=12, color=PT_COLOR),
            line_kws=dict(color=LINE_COLOR), ax=ax)
r, _ = stats.pearsonr(x, y)
ax.text(.05, .92, f"r = {r:.2f}", transform=ax.transAxes, fontsize=9)
ax.set_title(TITLE); ax.set_xlabel(XLAB); ax.set_ylabel(YLAB)
save_fig(fig, NAME)
