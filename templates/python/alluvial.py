#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""状态转移 Alluvial 图（患者状态随时间流动）—— 卡片 11_医学流行病学常用图/状态转移图_Alluvial.md
手绘（免 ggalluvial/plotly）：各时点分类堆叠 + 转移流量彩带。改 # >>> PARAM 区换真实转移数据。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_alluvial"
TITLE = "Disease state transitions"
STAGES = ["Baseline", "Year 1", "Year 2"]
STATES = ["Healthy", "Mild", "Severe", "Dead"]
COLORS = pal("cat_main")[:len(STATES)]
FIGSIZE = (4.8, 3.3)
# 换真实数据： 给每个个体在各 stage 的状态序列 seq[n, len(STAGES)]（整数 0..len(STATES)-1）。
# 下面用 Markov 转移矩阵 P（行=from，列=to）合成。
P = np.array([[.70, .20, .08, .02],
              [.15, .55, .25, .05],
              [.03, .20, .57, .20],
              [0,   0,   0,   1]])
n = 500
# <<< PARAM ------------------------------------------------------

ns, nst = len(STATES), len(STAGES)
seq = np.zeros((n, nst), int)
seq[:, 0] = np.random.choice(ns, n, p=[.6, .25, .13, .02])
for s in range(1, nst):
    for i in range(n):
        seq[i, s] = np.random.choice(ns, p=P[seq[i, s - 1]])

GAP = 0.03 * n; BW = 0.16
def blocks(col):
    top, out = 0.0, []
    for c in range(ns):
        cnt = (seq[:, col] == c).sum(); out.append((top, top + cnt)); top += cnt + GAP
    return out
def smooth(t): return 3 * t ** 2 - 2 * t ** 3
def ribbon(ax, x0, x1, a, b, color):
    t = np.linspace(0, 1, 40); xs = x0 + (x1 - x0) * t
    top = a[0] + (b[0] - a[0]) * smooth(t); bot = a[1] + (b[1] - a[1]) * smooth(t)
    xy = np.vstack([np.c_[xs, top], np.c_[xs[::-1], bot[::-1]]])
    ax.add_patch(Polygon(xy, closed=True, facecolor=color, alpha=.45, edgecolor="none"))

xpos = np.arange(nst, dtype=float)
BL = [blocks(s) for s in range(nst)]
fig, ax = plt.subplots(figsize=FIGSIZE)
for s in range(nst - 1):
    oc = [BL[s][c][0] for c in range(ns)]; ic = [BL[s + 1][c][0] for c in range(ns)]
    for src in range(ns):
        for dst in range(ns):
            h = ((seq[:, s] == src) & (seq[:, s + 1] == dst)).sum()
            if h <= 0: continue
            a = (oc[src], oc[src] + h); oc[src] += h
            b = (ic[dst], ic[dst] + h); ic[dst] += h
            ribbon(ax, xpos[s] + BW / 2, xpos[s + 1] - BW / 2, a, b, COLORS[src])
for s in range(nst):
    for c, (y0, y1) in enumerate(BL[s]):
        ax.add_patch(Rectangle((xpos[s] - BW / 2, y0), BW, y1 - y0,
                               facecolor=COLORS[c], edgecolor="white", lw=.5))
for c, st in enumerate(STATES):
    ax.plot([], [], color=COLORS[c], lw=6, label=st)
ax.set_xticks(xpos); ax.set_xticklabels(STAGES)
ax.set_yticks([]); ax.invert_yaxis(); ax.grid(False)
for sp in ["left", "right", "top"]:
    ax.spines[sp].set_visible(False)
ax.set_title(TITLE)
ax.legend(fontsize=7, ncol=ns, loc="lower center", bbox_to_anchor=(0.5, -0.20))
save_fig(fig, NAME)
