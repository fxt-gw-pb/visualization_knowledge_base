#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""直方图（+核密度叠加）—— 卡片 01_分布图/直方图_Histogram.md
合成数据，可独立运行。改 # >>> PARAM 区换数据/分箱/配色。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, seaborn as sns, matplotlib.pyplot as plt
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_histogram"
TITLE = "Distribution of a continuous variable"; XLAB = "Value"; YLAB = "Density"
FILL = pal("cat_main")[1]; LINE = pal("cat_main")[4]   # 浅蓝填充 + 深蓝密度线
BINS = 40
FIGSIZE = (3.6, 2.9)
# 换真实数据： x = df["TOTCHOL"].dropna().values
x = np.random.normal(230, 45, 2000)
# <<< PARAM ------------------------------------------------------

fig, ax = plt.subplots(figsize=FIGSIZE)
sns.histplot(x, bins=BINS, stat="density", color=FILL, edgecolor="white",
             alpha=.85, ax=ax)
sns.kdeplot(x, color=LINE, lw=1.6, ax=ax)
ax.set_title(TITLE); ax.set_xlabel(XLAB); ax.set_ylabel(YLAB)
save_fig(fig, NAME)
