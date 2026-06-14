#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""协变量平衡 Love plot（PSM/IPTW 前后 |SMD|）—— 卡片 13_因果推断图/协变量平衡图_LovePlot.md
合成各协变量匹配前/后标准化均差，点线对照 + 平衡阈值。改 # >>> PARAM 区换真实数据。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib.pyplot as plt
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_love"
TITLE = "Covariate balance (Love plot)"; XLAB = "Absolute standardized mean difference"
THRESH = 0.1                          # 平衡阈值（惯例 0.1）
C_BEFORE = pal("effect_dir")["ns"]; C_AFTER = pal("med_case_control")["low"]
FIGSIZE = (4.2, 3.0)
# 换真实数据： 每个协变量匹配前/后 |SMD|（cobalt::bal.tab 或手算）
covars = ["Age", "BMI", "Total cholesterol", "Glucose", "Smoking", "Hypertension", "Sex"]
smd_before = np.array([0.42, 0.31, 0.28, 0.51, 0.22, 0.37, 0.05])
smd_after  = np.array([0.06, 0.04, 0.08, 0.05, 0.07, 0.03, 0.02])
# <<< PARAM ------------------------------------------------------

order = np.argsort(smd_before)        # 影响最大的协变量排到顶部
covars = [covars[i] for i in order]; b = smd_before[order]; a = smd_after[order]
y = np.arange(len(covars))
fig, ax = plt.subplots(figsize=FIGSIZE)
for i in range(len(covars)):
    ax.plot([a[i], b[i]], [y[i], y[i]], color="#CCCCCC", lw=.8, zorder=1)
ax.scatter(b, y, color=C_BEFORE, s=34, label="Before matching", zorder=2)
ax.scatter(a, y, color=C_AFTER, s=34, label="After matching", zorder=3)
ax.axvline(THRESH, ls="--", color="grey", lw=.8)
ax.set_yticks(y); ax.set_yticklabels(covars); ax.grid(False)
ax.set_xlim(0, max(b) * 1.12); ax.set_xlabel(XLAB); ax.set_title(TITLE)
ax.legend(fontsize=8, loc="lower right")
save_fig(fig, NAME)
