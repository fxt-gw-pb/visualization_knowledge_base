#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kaplan-Meier 生存曲线 —— 卡片 07_生存分析图/KM生存曲线_KaplanMeier.md
合成生存数据 + lifelines。改 # >>> PARAM 区换数据/分组/配色。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_km"
TITLE = "Kaplan-Meier curves"; XLAB = "Time"; YLAB = "Survival probability"
TC = pal("med_treat_control")    # 处理 vs 对照
FIGSIZE = (3.6, 3.0)
# 换真实数据： 每组提供 T(时间) 与 E(事件 1/0)，一行一个体
groups = [("Treatment", TC["treat"], .0008), ("Control", TC["control"], .0016)]
# <<< PARAM ------------------------------------------------------

fig, ax = plt.subplots(figsize=FIGSIZE)
for label, c, hz in groups:
    T = np.random.exponential(1 / hz, 150)
    E = (np.random.rand(150) < .7).astype(int)
    KaplanMeierFitter(label=label).fit(T, E).plot_survival_function(ax=ax, ci_show=True, color=c)
ax.set_title(TITLE); ax.set_xlabel(XLAB); ax.set_ylabel(YLAB)
ax.grid(False); ax.legend(fontsize=8)
save_fig(fig, NAME)
