#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ROC 曲线 + AUC —— 卡片 06_预测模型评价图/ROC曲线_ROC.md
合成预测 + sklearn。改 # >>> PARAM 区换 y_true / y_score。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_roc"
TITLE = "ROC curve"; XLAB = "1 − Specificity"; YLAB = "Sensitivity"
CURVE_COLOR = pal("med_case_control")["low"]
FIGSIZE = (3.2, 3.2)
# 换真实数据： y_true=df["y"]; y_score=model.predict_proba(X)[:,1]
n = 500
y_true = np.random.binomial(1, .4, n)
y_score = np.clip(.5 * y_true + np.random.normal(0, .4, n), 0, 1)
# <<< PARAM ------------------------------------------------------

fpr, tpr, _ = roc_curve(y_true, y_score); auc = roc_auc_score(y_true, y_score)
fig, ax = plt.subplots(figsize=FIGSIZE)
ax.plot(fpr, tpr, color=CURVE_COLOR, lw=1.8)
ax.plot([0, 1], [0, 1], ls="--", c="grey", lw=.8)
ax.text(.45, .12, f"AUC = {auc:.2f}", fontsize=9)
ax.set_aspect("equal"); ax.grid(False)
ax.set_xlabel(XLAB); ax.set_ylabel(YLAB); ax.set_title(TITLE)
save_fig(fig, NAME)
