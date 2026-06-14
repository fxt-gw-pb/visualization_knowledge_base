#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Meta 分析森林图（逆方差合并 + 权重方块 + 合并菱形 + I²）—— 卡片 14_证据合成图/Meta森林图_MetaForest.md
合成各研究 OR/CI，手算 DerSimonian-Laird 随机效应合并。改 # >>> PARAM 区。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_metaforest"
TITLE = "Random-effects meta-analysis"; XLAB = "Odds ratio (95% CI)"
TICKS = [0.5, 1, 2]; REF = 1.0
BOX_C = pal("med_case_control")["low"]; DIA_C = pal("effect_dir")["harm"]
FIGSIZE = (5.0, 3.4)
# 换真实数据： 各研究 OR 与 95%CI（或 log OR + SE）
study = ["Cohort A 2018", "RCT B 2019", "Registry C 2020", "Cohort D 2021", "RCT E 2023"]
OR = np.array([1.62, 1.21, 1.95, 1.10, 1.48])
lo = np.array([1.10, 0.88, 1.30, 0.80, 1.05]); hi = np.array([2.38, 1.66, 2.92, 1.51, 2.09])
# <<< PARAM ------------------------------------------------------

yi = np.log(OR); sei = (np.log(hi) - np.log(lo)) / (2 * 1.96); wi = 1 / sei ** 2
Q = np.sum(wi * (yi - np.sum(wi * yi) / np.sum(wi)) ** 2); dfree = len(yi) - 1
C = np.sum(wi) - np.sum(wi ** 2) / np.sum(wi)
tau2 = max(0, (Q - dfree) / C); I2 = max(0, (Q - dfree) / Q) * 100
wr = 1 / (sei ** 2 + tau2); mu = np.sum(wr * yi) / np.sum(wr); se_mu = np.sqrt(1 / np.sum(wr))
pOR, plo, phi = np.exp(mu), np.exp(mu - 1.96 * se_mu), np.exp(mu + 1.96 * se_mu)
wpct = wr / np.sum(wr) * 100

n = len(study); y = np.arange(n)[::-1] + 1     # diamond 占 y=0
fig, ax = plt.subplots(figsize=FIGSIZE)
fig.subplots_adjust(left=0.28, right=0.80)
T = ax.get_yaxis_transform()
for i in range(n):
    ax.plot([lo[i], hi[i]], [y[i], y[i]], color=BOX_C, lw=1)
    ax.scatter(OR[i], y[i], s=30 + wpct[i] * 12, color=BOX_C, marker="s", zorder=3)
    ax.text(-0.40, y[i], study[i], transform=T, ha="left", va="center", fontsize=8)
    ax.text(1.02, y[i], f"{OR[i]:.2f} ({lo[i]:.2f}-{hi[i]:.2f})  {wpct[i]:.0f}%",
            transform=T, ha="left", va="center", fontsize=7)
hh = 0.32
ax.add_patch(Polygon([[plo, 0], [pOR, hh], [phi, 0], [pOR, -hh]], facecolor=DIA_C, edgecolor="none"))
ax.text(-0.40, 0, "Pooled (RE)", transform=T, ha="left", va="center", fontsize=8, fontweight="bold")
ax.text(1.02, 0, f"{pOR:.2f} ({plo:.2f}-{phi:.2f})", transform=T, ha="left", va="center",
        fontsize=7, fontweight="bold")
ax.axvline(REF, ls="--", color="grey", lw=.8)
ax.set_xscale("log"); ax.set_xticks(TICKS); ax.set_xticklabels([str(t) for t in TICKS])
ax.minorticks_off()                   # 关闭 log 轴杂散次刻度标签
ax.set_yticks([]); ax.set_ylim(-0.8, n + 0.8); ax.set_xlim(0.45, 3.2)
for sp in ["left", "top", "right"]:
    ax.spines[sp].set_visible(False)
ax.grid(False); ax.set_xlabel(XLAB)
ax.set_title(f"{TITLE}\nI² = {I2:.0f}%, τ² = {tau2:.3f}", fontsize=9)
save_fig(fig, NAME)
