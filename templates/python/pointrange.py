#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""点估计 + 95%CI（dot-and-whisker / 系数图）—— 卡片 02_组间比较图/点估计置信区间图_PointRange.md
按效应方向着色（有害红/保护蓝/不显著灰）。合成数据，可独立运行。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib.pyplot as plt
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_pointrange"
TITLE = "Dot-and-whisker (ref line at 0)"; XLAB = "Coefficient (95% CI)"
REFLINE = 0.0                 # 参考线（系数=0）
DIR = pal("effect_dir")       # harm/protect/ns
FIGSIZE = (3.4, 2.6)
# 换真实数据： terms/est/se 来自模型 summary
terms = ["X1", "X2", "X3", "X4", "X5"]
est = np.array([.8, -.3, .1, -.6, .4]); se = np.array([.15, .2, .18, .12, .25])
# <<< PARAM ------------------------------------------------------

order = np.argsort(est); est, se = est[order], se[order]
terms = [terms[i] for i in order]
lo, hi = est - 1.96 * se, est + 1.96 * se
cols = [DIR["harm"] if lo[i] > REFLINE else (DIR["protect"] if hi[i] < REFLINE else DIR["ns"])
        for i in range(len(terms))]
fig, ax = plt.subplots(figsize=FIGSIZE)
for i in range(len(terms)):
    ax.plot([lo[i], hi[i]], [i, i], c=cols[i], lw=1.4)
    ax.plot(est[i], i, "o", c=cols[i], ms=5)
ax.axvline(REFLINE, ls="--", c="grey", lw=.8)
ax.set_yticks(range(len(terms))); ax.set_yticklabels(terms); ax.grid(False)
ax.set_xlabel(XLAB); ax.set_title(TITLE)
save_fig(fig, NAME)
