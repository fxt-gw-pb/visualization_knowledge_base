#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""混淆矩阵热图 —— 卡片 06_预测模型评价图/混淆矩阵_ConfusionMatrix.md
注格：计数 + 行归一百分比。合成预测，可独立运行。改 # >>> PARAM 区换 y_true/y_pred。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, seaborn as sns, matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_confusion"
TITLE = "Confusion matrix"; XLAB = "Predicted"; YLAB = "Actual"
LABELS = ["No event", "Event"]
CMAP = pal("seq_blues")
FIGSIZE = (3.3, 3.0)
# 换真实数据： y_true = df["y"]; y_pred = (model.predict_proba(X)[:,1] >= 0.5).astype(int)
n = 600
y_true = np.random.binomial(1, .35, n)
y_pred = np.where(np.random.rand(n) < np.where(y_true == 1, .78, .12), 1, 0)
# <<< PARAM ------------------------------------------------------

cm = confusion_matrix(y_true, y_pred)
row = cm.sum(axis=1, keepdims=True)
ann = np.array([[f"{cm[i,j]}\n{cm[i,j]/row[i,0]*100:.0f}%" for j in range(cm.shape[1])]
                for i in range(cm.shape[0])])
fig, ax = plt.subplots(figsize=FIGSIZE)
sns.heatmap(cm / row, annot=ann, fmt="", cmap=CMAP, vmin=0, vmax=1, cbar=False,
            square=True, linewidths=.5, linecolor="white",
            xticklabels=LABELS, yticklabels=LABELS, annot_kws=dict(fontsize=9), ax=ax)
ax.set_title(TITLE); ax.set_xlabel(XLAB); ax.set_ylabel(YLAB)
save_fig(fig, NAME)
