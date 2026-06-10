#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""相关矩阵热图 —— 卡片 08_高维数据图/热图_Heatmap.md
发散配色（div_rdbu，中心 0）。合成数据，可独立运行。改 # >>> PARAM 区。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_heatmap"
TITLE = "Correlation heatmap"
CMAP = pal("div_rdbu")        # 发散，中心 0
FIGSIZE = (3.2, 2.9)
# 换真实数据： df = pd.read_csv("data.csv")[ ["c1","c2",...] ]
df = pd.DataFrame(np.random.randn(200, 6), columns=list("ABCDEF"))
df["B"] += .8 * df["A"]; df["E"] -= .6 * df["D"]
# <<< PARAM ------------------------------------------------------

fig, ax = plt.subplots(figsize=FIGSIZE)
sns.heatmap(df.corr(), cmap=CMAP, center=0, vmin=-1, vmax=1, annot=True, fmt=".2f",
            square=True, cbar_kws=dict(shrink=.8), ax=ax)
ax.set_title(TITLE)
save_fig(fig, NAME)
