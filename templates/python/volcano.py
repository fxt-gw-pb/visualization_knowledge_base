#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""火山图 Volcano（差异表达）—— 卡片 09_组学图/火山图_Volcano.md
合成基因数据，可独立运行。按 log2FC + p 阈值分 up/down/ns 着色。改 # >>> PARAM 区。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_volcano"
TITLE = "Volcano plot"; XLAB = "log2 fold change"; YLAB = "-log10 (adj. p)"
FC_THR = 1.0; P_THR = 0.05
DIR = pal("effect_dir")       # 上调=harm(红) 下调=protect(蓝) 不显著=ns(灰)
FIGSIZE = (3.6, 3.4)
# 换真实数据： df 需含 log2fc / padj（每行一个基因）
n = 4000
log2fc = np.random.normal(0, 1, n)
padj = 10 ** (-np.abs(np.random.normal(0, 1.5, n)) - 0.2 * np.abs(log2fc))
df = pd.DataFrame({"log2fc": log2fc, "padj": padj})
# <<< PARAM ------------------------------------------------------

def cls(r):
    if r.padj < P_THR and r.log2fc > FC_THR: return "up"
    if r.padj < P_THR and r.log2fc < -FC_THR: return "down"
    return "ns"
df["sig"] = df.apply(cls, axis=1)
cmap = {"up": DIR["harm"], "down": DIR["protect"], "ns": DIR["ns"]}
fig, ax = plt.subplots(figsize=FIGSIZE)
for s in ["ns", "up", "down"]:
    sub = df[df.sig == s]
    ax.scatter(sub.log2fc, -np.log10(sub.padj), s=6, alpha=.5, color=cmap[s],
               label=f"{s} ({len(sub)})", lw=0)
ax.axhline(-np.log10(P_THR), ls="--", c="grey", lw=.7)
ax.axvline(FC_THR, ls="--", c="grey", lw=.7); ax.axvline(-FC_THR, ls="--", c="grey", lw=.7)
ax.set_title(TITLE); ax.set_xlabel(XLAB); ax.set_ylabel(YLAB)
ax.grid(False); ax.legend(fontsize=7, markerscale=1.6)
save_fig(fig, NAME)
