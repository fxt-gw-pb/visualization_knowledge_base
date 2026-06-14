#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bland-Altman 一致性图（两测量方法）—— 卡片 03_相关性图/BlandAltman一致性图_BlandAltman.md
合成两方法测量，均值 vs 差值 + 偏倚 + 95% 一致性界限(LoA)。改 # >>> PARAM 区。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib.pyplot as plt
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_blandaltman"
TITLE = "Bland-Altman agreement"; XLAB = "Mean of two methods"; YLAB = "Difference (M1 - M2)"
PT_C = pal("med_case_control")["low"]
FIGSIZE = (4.0, 3.0)
# 换真实数据： m1 = df["method1"].values; m2 = df["method2"].values
n = 150; truth = np.random.normal(100, 15, n)
m1 = truth + np.random.normal(0, 4, n)
m2 = truth + 2 + np.random.normal(0, 4, n)    # 方法 2 系统性偏高 ~2
# <<< PARAM ------------------------------------------------------

mean = (m1 + m2) / 2; diff = m1 - m2
bias = diff.mean(); sd = diff.std(ddof=1)
loa_lo, loa_hi = bias - 1.96 * sd, bias + 1.96 * sd
fig, ax = plt.subplots(figsize=FIGSIZE)
ax.scatter(mean, diff, s=18, color=PT_C, alpha=.6, edgecolor="none")
for val, ls, lab in [(bias, "-", f"Bias {bias:.1f}"),
                     (loa_hi, "--", f"+1.96 SD {loa_hi:.1f}"),
                     (loa_lo, "--", f"-1.96 SD {loa_lo:.1f}")]:
    ax.axhline(val, ls=ls, color="grey", lw=1)
    ax.text(mean.max(), val, " " + lab, va="center", ha="left", fontsize=7, color="#555555")
ax.axhline(0, color="black", lw=.5, alpha=.4)
span = mean.max() - mean.min()
ax.set_xlim(mean.min(), mean.max() + span * 0.20)   # 右侧给标签留白
ax.set_xlabel(XLAB); ax.set_ylabel(YLAB); ax.set_title(TITLE); ax.grid(False)
save_fig(fig, NAME)
