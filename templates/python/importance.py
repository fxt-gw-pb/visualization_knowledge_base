#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""特征重要性 / SHAP 摘要图 —— 卡片 05_模型结果图/特征重要性图_FeatureImportance.md
Python 旗舰：SHAP beeswarm（每点=一个样本，颜色=特征值高低），EHR 预测模型可解释性首选。
合成 EHR 数据 + 树模型，可独立运行。改 # >>> PARAM 区换数据/模型。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
import shap
from sklearn.ensemble import RandomForestClassifier
from _common import save_fig
np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_importance"
TITLE = "SHAP summary (beeswarm)"
MAX_DISPLAY = 10
FIGSIZE = (5.0, 3.6)
# 换真实数据： X = df[feature_cols]; y = df["outcome"]; model = 你训练好的树模型
n = 800
X = pd.DataFrame({
    "Age": np.random.normal(60, 12, n), "BMI": np.random.normal(27, 4, n),
    "SBP": np.random.normal(135, 18, n), "Glucose": np.random.normal(105, 25, n),
    "HbA1c": np.random.normal(6.0, 1.0, n), "LDL": np.random.normal(120, 30, n),
    "eGFR": np.random.normal(80, 20, n), "Smoker": np.random.binomial(1, .3, n)})
logit = (0.04 * (X.Age - 60) + 0.06 * (X.Glucose - 105) + 0.5 * X.Smoker
         + 0.03 * (X.SBP - 135) - 0.02 * (X.eGFR - 80))
y = np.random.binomial(1, 1 / (1 + np.exp(-logit)))
model = RandomForestClassifier(n_estimators=200, max_depth=5, random_state=7).fit(X, y)
# <<< PARAM ------------------------------------------------------

exp = shap.TreeExplainer(model)(X)
if exp.values.ndim == 3:                 # 二分类 → 取阳性类
    exp = exp[..., 1]
plt.figure(figsize=FIGSIZE)
shap.plots.beeswarm(exp, max_display=MAX_DISPLAY, show=False, color_bar=True)
fig = plt.gcf()
plt.gca().set_title(TITLE, fontweight="bold")
fig.subplots_adjust(left=0.26, top=0.90, right=0.99, bottom=0.13)  # 留足特征名空间
save_fig(fig, NAME)
