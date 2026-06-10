#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""森林图（OR/HR，log 轴，ref=1）—— 卡片 05_模型结果图/森林图_ForestPlot.md
按效应方向着色。合成数据，可独立运行。改 # >>> PARAM 区。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib.pyplot as plt
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_forest"
TITLE = "Forest plot (log axis, ref=1)"; XLAB = "Odds ratio (95% CI)"
REF = 1.0                     # OR/HR 参考线
TICKS = [0.5, 1, 2, 4]
DIR = pal("effect_dir")
FIGSIZE = (4.4, 2.7)
# 换真实数据： terms/OR/lo/hi 来自 logistic/Cox 模型（exp(coef) 与 CI）
terms = ["Age", "Sex", "Smoking", "BMI", "Hypertension"]
OR = np.array([1.8, 0.7, 1.5, 1.05, 2.3])
lo = np.array([1.4, 0.55, 1.1, 0.95, 1.7]); hi = np.array([2.3, 0.9, 2.0, 1.16, 3.1])
# <<< PARAM ------------------------------------------------------

y = np.arange(len(terms))[::-1]
fig, ax = plt.subplots(figsize=FIGSIZE)
for i in range(len(terms)):
    c = DIR["harm"] if lo[i] > REF else (DIR["protect"] if hi[i] < REF else DIR["ns"])
    ax.plot([lo[i], hi[i]], [y[i], y[i]], c=c, lw=1.4)
    ax.plot(OR[i], y[i], "s", c=c, ms=6)
ax.axvline(REF, ls="--", c="grey", lw=.8)
ax.set_xscale("log"); ax.set_xticks(TICKS); ax.set_xticklabels(TICKS)
ax.set_yticks(y); ax.set_yticklabels(terms); ax.grid(False)
ax.set_xlabel(XLAB); ax.set_title(TITLE)
save_fig(fig, NAME)
