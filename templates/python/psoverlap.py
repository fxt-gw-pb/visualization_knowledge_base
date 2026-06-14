#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""倾向评分重叠图（mirror density，正性/共同支持域）—— 卡片 13_因果推断图/倾向评分重叠图_PSOverlap.md
合成 treated/control 倾向评分，上下镜像密度看重叠。改 # >>> PARAM 区。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_psoverlap"
TITLE = "Propensity score overlap"; XLAB = "Propensity score"; YLAB = "Density"
C_T = pal("med_treat_control")["treat"]; C_C = pal("med_treat_control")["control"]
FIGSIZE = (4.2, 3.0)
# 换真实数据： ps = model.predict_proba(X)[:,1]; treat = df["treat"].values（0/1）
ps_treat   = np.clip(np.random.beta(5, 3, 600), 1e-3, 1 - 1e-3)
ps_control = np.clip(np.random.beta(3, 5, 900), 1e-3, 1 - 1e-3)
# <<< PARAM ------------------------------------------------------

grid = np.linspace(0, 1, 200)
dt = gaussian_kde(ps_treat)(grid); dc = gaussian_kde(ps_control)(grid)
fig, ax = plt.subplots(figsize=FIGSIZE)
ax.fill_between(grid, 0, dt, color=C_T, alpha=.7, label="Treated")
ax.fill_between(grid, 0, -dc, color=C_C, alpha=.7, label="Control")
ax.axhline(0, color="black", lw=.6)
ax.set_yticks([])                     # 镜像密度 y 仅示意
ax.set_xlim(0, 1); ax.grid(False)
ax.set_xlabel(XLAB); ax.set_ylabel(YLAB); ax.set_title(TITLE)
ax.legend(fontsize=8, loc="upper center", ncol=2)
save_fig(fig, NAME)
