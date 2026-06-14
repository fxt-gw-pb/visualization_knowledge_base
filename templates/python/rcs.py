#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""限制性立方样条 RCS 剂量反应曲线（非线性 OR + 95%CI 带）—— 卡片 13_因果推断图/限制性立方样条_RCS.md
合成 J 形暴露-结局，RCS(4 节点) logistic 拟合，参考点 OR=1。改 # >>> PARAM 区。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib.pyplot as plt, statsmodels.api as sm
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_rcs"
TITLE = "RCS dose-response"; XLAB = "Exposure"; YLAB = "Odds ratio (95% CI)"
KNOT_Q = [.05, .35, .65, .95]         # 4 节点位置（Harrell 推荐分位）
LINE_C = pal("med_case_control")["low"]; BAND_C = LINE_C
FIGSIZE = (4.0, 3.0)
# 换真实数据： x = df["exposure"].values; y = df["outcome"].values（0/1）
n = 1500; x = np.random.normal(0, 1, n)
y = np.random.binomial(1, 1 / (1 + np.exp(-(0.4 * x ** 2 - 0.3 * x - 0.5))))  # J 形真实关系
REF = float(np.median(x))             # 参考点（OR=1）
# <<< PARAM ------------------------------------------------------

def rcs_basis(v, knots):              # Harrell 限制性立方样条基（k 节点 → k-1 列）
    v = np.asarray(v, float); t = np.asarray(knots, float); k = len(t)
    cube = lambda u: np.where(u > 0, u ** 3, 0.0)
    cols = [v]; tk, tk1 = t[-1], t[-2]
    for j in range(k - 2):
        cols.append(cube(v - t[j]) - cube(v - tk1) * (tk - t[j]) / (tk - tk1)
                    + cube(v - tk) * (tk1 - t[j]) / (tk - tk1))
    return np.column_stack(cols)

knots = np.quantile(x, KNOT_Q)
fit = sm.GLM(y, sm.add_constant(rcs_basis(x, knots)), family=sm.families.Binomial()).fit()
grid = np.linspace(np.percentile(x, 1), np.percentile(x, 99), 200)
Bg = sm.add_constant(rcs_basis(grid, knots), has_constant="add")
Br = sm.add_constant(rcs_basis([REF], knots), has_constant="add")
contrast = Bg - Br                    # 相对参考点的对比（截距项相消）
lp = contrast @ fit.params
se = np.sqrt(np.einsum("ij,jk,ik->i", contrast, fit.cov_params(), contrast))
OR, lo, hi = np.exp(lp), np.exp(lp - 1.96 * se), np.exp(lp + 1.96 * se)

fig, ax = plt.subplots(figsize=FIGSIZE)
ax.fill_between(grid, lo, hi, color=BAND_C, alpha=.18)
ax.plot(grid, OR, color=LINE_C, lw=1.8)
ax.axhline(1, ls="--", color="grey", lw=.8)
ax.axvline(REF, ls=":", color="grey", lw=.8)
ax.set_xlabel(XLAB); ax.set_ylabel(YLAB); ax.set_title(TITLE); ax.grid(False)
save_fig(fig, NAME)
