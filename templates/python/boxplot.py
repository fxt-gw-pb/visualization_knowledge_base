#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""箱线图 + 抖动点 —— 卡片 02_图表类型知识卡片/02_组间比较图/箱线图_Boxplot.md
合成数据，可独立运行。改 # >>> PARAM 区换数据/列/配色。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_boxplot"
TITLE = "Boxplot + jittered points"; XLAB = None; YLAB = "Value"
PALETTE = "cat_main"          # 分类配色 registry 名
FIGSIZE = (3.4, 2.9)
# 换真实数据： df = pd.read_csv("data.csv"); X="grp"; Y="val"
X, Y = "grp", "val"
N = 200
df = pd.DataFrame({X: np.repeat(["A", "B", "C"], N),
                   Y: np.concatenate([np.random.normal(0, 1, N),
                                      np.random.normal(.8, 1.2, N),
                                      np.random.normal(.3, .8, N)])})
# <<< PARAM ------------------------------------------------------

colors = pal(PALETTE)
fig, ax = plt.subplots(figsize=FIGSIZE)
sns.boxplot(data=df, x=X, y=Y, hue=X, palette=colors[:df[X].nunique()],
            legend=False, showfliers=False, width=.55, ax=ax)
sns.stripplot(data=df, x=X, y=Y, color="#333333", size=2, alpha=.25, ax=ax)
ax.set_title(TITLE); ax.set_xlabel(XLAB); ax.set_ylabel(YLAB)
save_fig(fig, NAME)
