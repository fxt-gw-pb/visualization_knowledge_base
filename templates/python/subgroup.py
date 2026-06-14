#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""亚组分析森林图（含交互 p）—— 卡片 05_模型结果图/亚组森林图_Subgroup.md
合成各亚组层 OR/CI + 交互 p，分层带表头森林图。改 # >>> PARAM 区换真实数据。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib.pyplot as plt
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_subgroup"
TITLE = "Subgroup analysis"; XLAB = "Odds ratio (95% CI)"
REF = 1.0; TICKS = [0.5, 1, 2]
DIR = pal("effect_dir")
FIGSIZE = (5.4, 3.4)
# 每行： (label, OR, lo, hi, is_header, p_interaction)  表头行 OR=None
rows = [
    ("Sex",          None, None, None, True,  "0.62"),
    ("  Male",       1.45, 1.10, 1.92, False, None),
    ("  Female",     1.30, 0.98, 1.72, False, None),
    ("Age group",    None, None, None, True,  "0.03"),
    ("  < 50 y",     1.10, 0.82, 1.48, False, None),
    ("  >= 50 y",    1.85, 1.40, 2.45, False, None),
    ("Smoking",      None, None, None, True,  "0.48"),
    ("  Never",      1.38, 1.02, 1.86, False, None),
    ("  Current",    1.55, 1.12, 2.15, False, None),
]
# <<< PARAM ------------------------------------------------------

n = len(rows); y = np.arange(n)[::-1]
fig, ax = plt.subplots(figsize=FIGSIZE)
fig.subplots_adjust(left=0.30, right=0.80)
T = ax.get_yaxis_transform()          # x=轴比例, y=数据
for yi, (label, OR, lo, hi, hdr, pint) in zip(y, rows):
    if hdr:
        ax.text(-0.42, yi, label, transform=T, ha="left", va="center", fontweight="bold")
        if pint:
            ax.text(1.02, yi, f"P-int = {pint}", transform=T, ha="left", va="center",
                    fontsize=7.5, color="#555555")
    else:
        c = DIR["harm"] if lo > REF else (DIR["protect"] if hi < REF else DIR["ns"])
        ax.plot([lo, hi], [yi, yi], color=c, lw=1.4)
        ax.plot(OR, yi, "s", color=c, ms=6)
        ax.text(-0.40, yi, label, transform=T, ha="left", va="center", fontsize=8.5)
        ax.text(1.02, yi, f"{OR:.2f} ({lo:.2f}-{hi:.2f})", transform=T,
                ha="left", va="center", fontsize=7.5)
ax.axvline(REF, ls="--", color="grey", lw=.8)
ax.set_xscale("log"); ax.set_xticks(TICKS); ax.set_xticklabels([str(t) for t in TICKS])
ax.minorticks_off()                   # 关闭 log 轴杂散次刻度标签
ax.set_yticks([]); ax.set_ylim(-0.6, n - 0.4); ax.set_xlim(0.45, 2.6)
ax.spines["left"].set_visible(False)
ax.grid(False); ax.set_xlabel(XLAB); ax.set_title(TITLE)
save_fig(fig, NAME)
