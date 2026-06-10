#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Swimmer plot 患者时间线 —— 卡片 11_医学流行病学常用图/Swimmer图_Swimmer.md
每名患者一条横条=随访时长，叠加事件标记（应答/进展/死亡）+ 进行中箭头。RWD/肿瘤常用。
合成患者数据，可独立运行。改 # >>> PARAM 区换数据。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_swimmer"
TITLE = "Swimmer plot: patient timelines"; XLAB = "Months since enrollment"
BAR = pal("cat_main")[1]; C = pal("cat_main")
FIGSIZE = (4.6, 3.8)
# 换真实数据： 每行一患者：duration / response / progression / death(bool) / ongoing(bool)
m = 16
df = pd.DataFrame({
    "pid": [f"P{i:02d}" for i in range(1, m + 1)],
    "duration": np.round(np.random.uniform(3, 30, m), 1),
    "response": np.round(np.random.uniform(1, 8, m), 1),
    "progression": [np.round(np.random.uniform(8, 20), 1) if np.random.rand() < .6 else np.nan for _ in range(m)],
    "death": np.random.rand(m) < .35,
    "ongoing": np.random.rand(m) < .4})
# <<< PARAM ------------------------------------------------------

df = df.sort_values("duration").reset_index(drop=True)
fig, ax = plt.subplots(figsize=FIGSIZE)
for i, r in df.iterrows():
    ax.barh(i, r.duration, height=.6, color=BAR, alpha=.55, zorder=1)
    ax.scatter(r.response, i, marker="^", s=28, color=C[2], zorder=3)          # 应答
    if not np.isnan(r.progression) and r.progression <= r.duration:
        ax.scatter(r.progression, i, marker="X", s=30, color=C[5], zorder=3)   # 进展
    if r.death:
        ax.scatter(r.duration, i, marker="s", s=26, color="#333333", zorder=3) # 死亡
    elif r.ongoing:
        ax.annotate("", xy=(r.duration + 1.2, i), xytext=(r.duration, i),
                    arrowprops=dict(arrowstyle="-|>", color="grey", lw=1))      # 进行中
ax.set_yticks(range(len(df))); ax.set_yticklabels(df.pid, fontsize=6)
ax.set_xlabel(XLAB); ax.set_title(TITLE); ax.grid(False, axis="y")
handles = [plt.Line2D([], [], marker=m, ls="", color=c, label=l) for m, c, l in
           [("^", C[2], "Response"), ("X", C[5], "Progression"), ("s", "#333333", "Death")]]
handles.append(plt.Line2D([], [], marker=">", ls="", color="grey", label="Ongoing"))
ax.legend(handles=handles, fontsize=7, loc="lower right")
save_fig(fig, NAME)
