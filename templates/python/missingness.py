#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""缺失数据模式图 —— 卡片 12_数据质量图/缺失数据图_Missingness.md
上：每列缺失比例条；下：缺失矩阵（行=记录抽样，列=变量，深色=缺失）。
EHR/RWD 第一步必看。合成数据，可独立运行。改 # >>> PARAM 区换数据。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_missingness"
TITLE = "Missing data pattern"
BAR_COLOR = pal("cat_main")[4]; MISS_COLOR = pal("med_case_control")["high"]
FIGSIZE = (4.6, 3.8); MATRIX_ROWS = 200      # 矩阵抽样行数
# 换真实数据： df = pd.read_csv("ehr.csv")   # 直接喂原始 DataFrame 即可
cols = ["Age", "Sex", "BMI", "SBP", "Glucose", "HbA1c", "LDL", "eGFR", "Smoker", "Outcome"]
n = 1000
df = pd.DataFrame({c: np.random.randn(n) for c in cols})
for c, rate in zip(cols, [0, 0, .01, .08, .12, .35, .22, .18, .05, 0]):
    df.loc[np.random.rand(n) < rate, c] = np.nan
# <<< PARAM ------------------------------------------------------

miss_frac = df.isna().mean().values
order = np.argsort(-miss_frac)                 # 缺失多的列在左
cols_o = [df.columns[i] for i in order]
M = df[cols_o].isna().iloc[:MATRIX_ROWS].astype(int).values

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=FIGSIZE, height_ratios=[1, 3], sharex=True)
ax1.bar(range(len(cols_o)), miss_frac[order] * 100, color=BAR_COLOR, width=.7)
ax1.set_ylabel("Missing %"); ax1.grid(False, axis="x")
for i, v in enumerate(miss_frac[order] * 100):
    if v > 0:
        ax1.text(i, v + 1, f"{v:.0f}", ha="center", va="bottom", fontsize=6.5)
ax2.imshow(M, aspect="auto", interpolation="none",
           cmap=ListedColormap(["#F2F2F2", MISS_COLOR]))
ax2.set_yticks([]); ax2.set_ylabel(f"Records (n={MATRIX_ROWS})"); ax2.grid(False)
ax2.set_xticks(range(len(cols_o))); ax2.set_xticklabels(cols_o, rotation=45, ha="right", fontsize=7)
fig.suptitle(TITLE, fontweight="bold"); fig.tight_layout()
save_fig(fig, NAME)
