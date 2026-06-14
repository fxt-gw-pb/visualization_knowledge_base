#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""列线图 Nomogram（logistic 预测模型）—— 卡片 05_模型结果图/列线图_Nomogram.md
手绘（免 rms）：每个预测因子一条带刻度的点数标尺 + 总点数 + 风险标尺。改 # >>> PARAM 区。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_nomogram"
TITLE = "Nomogram (logistic model)"
AXIS_C = pal("med_case_control")["low"]
RISKS = [0.1, 0.2, 0.3, 0.5, 0.7, 0.9]    # 风险标尺要标的概率
INTERCEPT = -6.5
FIGSIZE = (6.0, 3.4)
# 每个预测因子： (name, beta, (xmin, xmax), [显示刻度值])  —— beta 来自 logistic 模型系数
preds = [
    ("Age (years)",     0.06, (40, 80), [40, 50, 60, 70, 80]),
    ("BMI (kg/m2)",     0.10, (18, 40), [18, 24, 30, 36]),
    ("Smoking (1=yes)", 0.80, (0, 1),   [0, 1]),
    ("Hypertension",    0.70, (0, 1),   [0, 1]),
]
# <<< PARAM ------------------------------------------------------

ranges = [abs(b) * (xr[1] - xr[0]) for _, b, xr, _ in preds]
scale = 100.0 / max(ranges)               # 贡献范围最大的因子映射到 0–100 分
los = [min(b * xr[0], b * xr[1]) for _, b, xr, _ in preds]
def points_of(j, x): return scale * (preds[j][1] * x - los[j])
max_total = scale * sum(ranges); sum_lo = sum(los)

rows = ["Points"] + [p[0] for p in preds] + ["Total Points", "Predicted risk"]
ny = len(rows); ys = list(range(ny))[::-1]
xmap_pts = lambda p: p / 100.0
xmap_tot = lambda tp: tp / max_total
fig, ax = plt.subplots(figsize=FIGSIZE)

def ruler(y, ticks, xs_norm, labels, color):
    ax.plot([min(xs_norm), max(xs_norm)], [y, y], color=color, lw=1.1)
    for xx, lab in zip(xs_norm, labels):
        ax.plot([xx, xx], [y - 0.12, y + 0.12], color=color, lw=.8)
        ax.text(xx, y + 0.18, lab, ha="center", va="bottom", fontsize=6.5)

# Points 标尺
pp = list(range(0, 101, 10))
ruler(ys[0], pp, [xmap_pts(p) for p in pp], [str(p) for p in pp], "black")
# 各预测因子标尺
for j, (name, b, xr, ticks) in enumerate(preds):
    ruler(ys[1 + j], ticks, [xmap_pts(points_of(j, t)) for t in ticks],
          [f"{t:g}" for t in ticks], AXIS_C)
# Total Points 标尺
tp = np.linspace(0, max_total, 6)
ruler(ys[-2], tp, [xmap_tot(t) for t in tp], [f"{t:.0f}" for t in tp], "black")
# 风险标尺： risk r → lp=logit(r) → 总点数 = scale*(lp - intercept - Σlo)
yr = ys[-1]; ax.plot([0, 1], [yr, yr], color="black", lw=1.1)
for r in RISKS:
    tpr = scale * (np.log(r / (1 - r)) - INTERCEPT - sum_lo)
    if 0 <= tpr <= max_total:
        xx = xmap_tot(tpr); ax.plot([xx, xx], [yr - 0.12, yr + 0.12], color="black", lw=.8)
        ax.text(xx, yr - 0.30, f"{r:g}", ha="center", va="top", fontsize=6.5)
# 行名
for y, name in zip(ys, rows):
    ax.text(-0.02, y, name, ha="right", va="center", fontsize=8, fontweight="bold")
ax.set_xlim(-0.34, 1.06); ax.set_ylim(-0.7, ny - 0.3)
ax.axis("off"); ax.set_title(TITLE)
save_fig(fig, NAME)
