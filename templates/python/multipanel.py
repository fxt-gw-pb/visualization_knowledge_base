#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""多面板组合图（A/B/C/D 讲一个故事）—— 卡片 10_多面板组合图/多面板组合图_MultiPanel.md
gridspec/subplots 布局 + 左上角粗体面板标签。合成数据，可独立运行。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
from sklearn.metrics import roc_curve
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_multipanel"
SUPTITLE = "Multi-panel figure (A/B/C/D)"
PALETTE = "cat_main"; DIR = pal("effect_dir"); BLUE = pal("med_case_control")["low"]
FIGSIZE = (6.4, 4.8)
# <<< PARAM ------------------------------------------------------

colors = pal(PALETTE)
N = 200
g3 = pd.DataFrame({"grp": np.repeat(["A", "B", "C"], N),
                   "val": np.concatenate([np.random.normal(0, 1, N),
                                          np.random.normal(.8, 1.2, N),
                                          np.random.normal(.3, .8, N)])})
fig, axd = plt.subplots(2, 2, figsize=FIGSIZE); axd = axd.ravel()
# A 分布
sns.boxplot(data=g3, x="grp", y="val", hue="grp", palette=colors[:3], legend=False,
            showfliers=False, ax=axd[0]); axd[0].set_title("A  Distribution", loc="left", fontweight="bold")
# B 关系
x = np.random.randn(200)
axd[1].scatter(x, 1.2 * x + np.random.randn(200), s=8, alpha=.4, color=BLUE)
axd[1].set_title("B  Relationship", loc="left", fontweight="bold")
# C 模型（森林）
terms = ["X1", "X2", "X3"]; OR = [1.8, .7, 1.3]; lo = [1.4, .55, .9]; hi = [2.3, .9, 1.9]
for i in range(3):
    c = DIR["harm"] if lo[i] > 1 else (DIR["protect"] if hi[i] < 1 else DIR["ns"])
    axd[2].plot([lo[i], hi[i]], [i, i], c=c); axd[2].plot(OR[i], i, "s", c=c, ms=5)
axd[2].axvline(1, ls="--", c="grey"); axd[2].set_xscale("log")
axd[2].set_yticks(range(3)); axd[2].set_yticklabels(terms)
axd[2].set_title("C  Model", loc="left", fontweight="bold")
# D 评价（ROC）
yy = np.random.binomial(1, .4, 400); ss = np.clip(.5 * yy + np.random.normal(0, .4, 400), 0, 1)
f, t, _ = roc_curve(yy, ss)
axd[3].plot(f, t, color=BLUE); axd[3].plot([0, 1], [0, 1], ls="--", c="grey")
axd[3].set_title("D  Evaluation", loc="left", fontweight="bold")
for a in axd: a.grid(False)
fig.suptitle(SUPTITLE, fontweight="bold"); fig.tight_layout()
save_fig(fig, NAME)
