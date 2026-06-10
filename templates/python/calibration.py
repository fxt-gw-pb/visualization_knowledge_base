#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校准曲线 —— 卡片 06_预测模型评价图/校准曲线_Calibration.md
合成预测 + sklearn calibration_curve。改 # >>> PARAM 区换 y_true / y_prob。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib.pyplot as plt
from sklearn.calibration import calibration_curve
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_calibration"
TITLE = "Calibration curve"; XLAB = "Predicted probability"; YLAB = "Observed frequency"
CURVE_COLOR = pal("med_case_control")["low"]
N_BINS = 10
FIGSIZE = (3.2, 3.2)
# 换真实数据： y_true=df["y"]; y_prob=model.predict_proba(X)[:,1]
n = 2000
y_prob = np.random.beta(2, 3, n)
y_true = np.random.binomial(1, y_prob)
# <<< PARAM ------------------------------------------------------

pt, pp = calibration_curve(y_true, y_prob, n_bins=N_BINS, strategy="quantile")
brier = np.mean((y_prob - y_true) ** 2)
fig, ax = plt.subplots(figsize=FIGSIZE)
ax.plot([0, 1], [0, 1], ls="--", c="grey", lw=.8)
ax.plot(pp, pt, "o-", color=CURVE_COLOR)
ax.plot(y_prob, np.full(n, -.02), "|", color="k", alpha=.03)
ax.text(.05, .92, f"Brier = {brier:.3f}", transform=ax.transAxes, fontsize=9)
ax.set_xlim(-.03, 1); ax.set_ylim(-.05, 1); ax.set_aspect("equal"); ax.grid(False)
ax.set_xlabel(XLAB); ax.set_ylabel(YLAB); ax.set_title(TITLE)
save_fig(fig, NAME)
