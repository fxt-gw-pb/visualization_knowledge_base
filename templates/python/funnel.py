#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""漏斗图 Funnel plot（发表偏倚）—— 卡片 14_证据合成图/漏斗图_Funnel.md
效应量 vs 标准误（y 反向），含合并线 + 伪 95% 置信漏斗。改 # >>> PARAM 区。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib.pyplot as plt
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_funnel"
TITLE = "Funnel plot"; XLAB = "log Odds ratio"; YLAB = "Standard error"
PT_C = pal("med_case_control")["low"]
FIGSIZE = (4.0, 3.4)
# 换真实数据： yi = 各研究 log 效应量; sei = 其标准误（每研究一行）
k = 25; mu_true = 0.3
sei = np.random.uniform(0.05, 0.45, k)
yi = np.random.normal(mu_true, sei)        # 对称散布（无明显偏倚）
# <<< PARAM ------------------------------------------------------

wi = 1 / sei ** 2; mu = np.sum(wi * yi) / np.sum(wi)
se_grid = np.linspace(1e-3, sei.max() * 1.05, 100)
fig, ax = plt.subplots(figsize=FIGSIZE)
ax.plot(mu - 1.96 * se_grid, se_grid, color="grey", lw=.8, ls="--")
ax.plot(mu + 1.96 * se_grid, se_grid, color="grey", lw=.8, ls="--")
ax.axvline(mu, color="grey", lw=.8)
ax.scatter(yi, sei, s=22, color=PT_C, alpha=.7, edgecolor="white", lw=.4, zorder=3)
ax.set_ylim(se_grid.max(), 0)              # y 反向：精确(小 SE)在上
ax.set_xlabel(XLAB); ax.set_ylabel(YLAB); ax.set_title(TITLE); ax.grid(False)
save_fig(fig, NAME)
