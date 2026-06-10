#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""竞争风险累积发病曲线 CIF —— 卡片 07_生存分析图/竞争风险累积发病图_CompetingRisk.md
RWD 生存常有竞争事件（如目标事件 vs 死亡）。用 Aalen-Johansen 估计 event-of-interest 的 CIF。
合成竞争风险数据 + lifelines，可独立运行。改 # >>> PARAM 区。"""
import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from lifelines import AalenJohansenFitter
from _common import set_theme, save_fig, pal
set_theme(); np.random.seed(7)

# >>> PARAM ------------------------------------------------------
NAME = "tpl_cif"
TITLE = "Cumulative incidence (event of interest)"; XLAB = "Time (days)"; YLAB = "Cumulative incidence"
EVENT_OF_INTEREST = 1            # 1=目标事件；2=竞争事件（如死亡）；0=删失
TC = pal("med_case_control")
FIGSIZE = (3.8, 3.2)
# 换真实数据： df 含 time / event(0/1/2) / group
def make(group, hz1, hz2, m=300):
    t1 = np.random.exponential(1 / hz1, m); t2 = np.random.exponential(1 / hz2, m)
    tc = np.random.exponential(3000, m)     # 删失
    t = np.minimum(np.minimum(t1, t2), tc)
    ev = np.where((t1 <= t2) & (t1 <= tc), 1, np.where((t2 < t1) & (t2 <= tc), 2, 0))
    return pd.DataFrame({"time": t, "event": ev, "group": group})
df = pd.concat([make("Exposed", .0009, .0006), make("Unexposed", .0005, .0006)], ignore_index=True)
groups = [("Exposed", TC["high"]), ("Unexposed", TC["low"])]
# <<< PARAM ------------------------------------------------------

fig, ax = plt.subplots(figsize=FIGSIZE)
for g, c in groups:
    sub = df[df.group == g]
    t = sub.time.values + np.random.uniform(0, 1e-3, len(sub))   # 抖动破除并列
    ajf = AalenJohansenFitter(seed=7)
    ajf.fit(t, sub.event.values, event_of_interest=EVENT_OF_INTEREST)
    cif = ajf.cumulative_density_
    ax.step(cif.index, cif.iloc[:, 0], where="post", color=c, lw=1.6, label=g)
ax.set_title(TITLE); ax.set_xlabel(XLAB); ax.set_ylabel(YLAB)
ax.grid(False); ax.legend(fontsize=8, title="Group")
save_fig(fig, NAME)
