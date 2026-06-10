#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PCA 散点图（PC1 vs PC2，按组着色）—— 卡片 08_高维数据图/PCA图_PCA.md
合成高维数据 + sklearn PCA，可独立运行。改 # >>> PARAM 区换数据/分组/配色。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_pca"
TITLE = "PCA of samples"
PALETTE = "cat_main"
FIGSIZE = (3.6, 3.2)
# 换真实数据： X = df[feature_cols].values; labels = df["group"].values
groups = ["Type A", "Type B", "Type C"]; per = 80; p = 20
centers = np.random.normal(0, 3, (len(groups), p))
X = np.vstack([centers[i] + np.random.normal(0, 1, (per, p)) for i in range(len(groups))])
labels = np.repeat(groups, per)
# <<< PARAM ------------------------------------------------------

Z = PCA(n_components=2).fit(StandardScaler().fit_transform(X))
pcs = Z.transform(StandardScaler().fit_transform(X)); ev = Z.explained_variance_ratio_ * 100
colors = pal(PALETTE)
fig, ax = plt.subplots(figsize=FIGSIZE)
for i, g in enumerate(groups):
    m = labels == g
    ax.scatter(pcs[m, 0], pcs[m, 1], s=14, alpha=.7, color=colors[i], label=g, lw=0)
ax.axhline(0, c="grey", lw=.5, ls=":"); ax.axvline(0, c="grey", lw=.5, ls=":")
ax.set_title(TITLE); ax.grid(False)
ax.set_xlabel(f"PC1 ({ev[0]:.1f}%)"); ax.set_ylabel(f"PC2 ({ev[1]:.1f}%)")
ax.legend(fontsize=8)
save_fig(fig, NAME)
