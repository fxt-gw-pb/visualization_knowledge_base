#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""决策曲线分析 DCA（净获益）—— 卡片 06_预测模型评价图/决策曲线_DCA.md
比较模型 vs treat-all vs treat-none 的 net benefit。纯计算，无特殊依赖。
合成预测，可独立运行。改 # >>> PARAM 区换 y_true/y_prob。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib.pyplot as plt
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_dca"
TITLE = "Decision curve analysis"; XLAB = "Threshold probability"; YLAB = "Net benefit"
MODEL_COLOR = pal("med_case_control")["low"]
TMIN, TMAX = 0.01, 0.6
FIGSIZE = (3.8, 3.2)
# 换真实数据： y_true = df["y"].values; y_prob = model.predict_proba(X)[:,1]
n = 2000
y_prob = np.random.beta(2, 4, n)
y_true = np.random.binomial(1, y_prob)
# <<< PARAM ------------------------------------------------------

def net_benefit(y, p, t):
    tp = ((p >= t) & (y == 1)).sum(); fp = ((p >= t) & (y == 0)).sum(); n = len(y)
    return tp / n - fp / n * (t / (1 - t))

thr = np.linspace(TMIN, TMAX, 100); prev = y_true.mean()
nb_model = [net_benefit(y_true, y_prob, t) for t in thr]
nb_all = [prev - (1 - prev) * (t / (1 - t)) for t in thr]
fig, ax = plt.subplots(figsize=FIGSIZE)
ax.plot(thr, nb_model, color=MODEL_COLOR, lw=1.8, label="Model")
ax.plot(thr, nb_all, color="#999999", lw=1, ls="-", label="Treat all")
ax.axhline(0, color="black", lw=1, ls="--", label="Treat none")
ax.set_ylim(min(-0.02, min(nb_model)), max(nb_model) * 1.15 + 1e-3)
ax.set_title(TITLE); ax.set_xlabel(XLAB); ax.set_ylabel(YLAB)
ax.grid(False); ax.legend(fontsize=8)
save_fig(fig, NAME)
