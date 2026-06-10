#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONSORT 队列入组流程图 —— 卡片 11_医学流行病学常用图/CONSORT流程图_Consort.md
matplotlib 手搓盒+箭头；改 # >>> PARAM 的人数即可。可独立运行。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from _common import set_theme, save_fig, pal
set_theme()

# >>> PARAM ------------------------------------------------------
NAME = "tpl_consort"; TITLE = "Study flow (CONSORT-style)"
BOX = pal("cat_main")[1]      # 盒填充色（浅蓝）
# 各阶段人数与文案
assessed = 1200; excluded = 350
excl_reasons = ["Not meeting criteria (n=210)", "Declined (n=90)", "Other (n=50)"]
enrolled = assessed - excluded
arm_a, arm_b = 430, 420
ana_a, ana_b = 410, 405
FIGSIZE = (5.4, 5.6)
# <<< PARAM ------------------------------------------------------

fig, ax = plt.subplots(figsize=FIGSIZE); ax.set_xlim(0, 10); ax.set_ylim(0, 12)
ax.axis("off"); ax.set_title(TITLE, fontweight="bold")

def box(x, y, w, h, text, fc=BOX):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, fc=fc, ec="black",
                                lw=.8, boxstyle="round,pad=0.02,rounding_size=0.08"))
    ax.text(x, y, text, ha="center", va="center", fontsize=7.5)

def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=10, lw=.9, color="black"))

box(3.2, 11, 4.4, 1.0, f"Assessed for eligibility\n(n={assessed})")
box(7.3, 9.4, 4.2, 1.4, "Excluded (n={})\n".format(excluded) + "\n".join("• " + r for r in excl_reasons),
    fc="#F0F0F0")
arrow(3.2, 10.5, 3.2, 8.9); arrow(3.2, 9.7, 5.2, 9.7)
box(3.2, 8.4, 4.4, 0.9, f"Enrolled / Randomized\n(n={enrolled})")
arrow(3.2, 7.95, 3.2, 7.2); arrow(1.8, 7.2, 1.8, 6.5); arrow(4.6, 7.2, 4.6, 6.5)
ax.plot([1.8, 4.6], [7.2, 7.2], color="black", lw=.9)
box(1.8, 6.0, 3.0, 0.9, f"Arm A\nAllocated (n={arm_a})")
box(4.6, 6.0, 3.0, 0.9, f"Arm B\nAllocated (n={arm_b})")
arrow(1.8, 5.55, 1.8, 4.8); arrow(4.6, 5.55, 4.6, 4.8)
box(1.8, 4.3, 3.0, 0.9, f"Analyzed (n={ana_a})")
box(4.6, 4.3, 3.0, 0.9, f"Analyzed (n={ana_b})")
save_fig(fig, NAME)
