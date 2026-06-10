#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sci-plot Python 模板共享层：发表级主题 + 配色 registry + 导出助手。

所有 templates/python/*.py 都 `from _common import ...`，确保主题/配色/导出一处定义。
配色 REGISTRY 是 03_配色系统/配色系统总览.md 第 2 节的代码镜像 —— 模板只用 pal() 取值，不内联 hex。
"""
import os
import matplotlib as mpl
import matplotlib.pyplot as plt

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 配色 registry（名 → 值），与 配色系统总览.md 同步
REGISTRY = {
    # 分类（Okabe-Ito，色盲友好）
    "cat_main": ["#E69F00", "#56B4E9", "#009E73", "#F0E442",
                 "#0072B2", "#D55E00", "#CC79A7", "#999999"],
    # 医学二分类：高风险/病例 暖色，低风险/对照 冷色
    "med_case_control": {"high": "#D55E00", "low": "#0072B2"},
    "med_treat_control": {"treat": "#009E73", "control": "#999999"},
    # 模型效应方向：有害 红 / 保护 蓝 / 不显著 灰
    "effect_dir": {"harm": "#B2182B", "protect": "#2166AC", "ns": "#999999"},
    # 连续 / 发散（matplotlib cmap 名）
    "div_rdbu": "RdBu_r",
    "seq_viridis": "viridis",
    "seq_blues": "Blues",
}


def pal(name):
    """按 registry 名取配色值。"""
    if name not in REGISTRY:
        raise KeyError(f"未知配色 registry 名 '{name}'，可选：{list(REGISTRY)}")
    return REGISTRY[name]


def set_theme():
    """发表级 matplotlib 主题（与 gallery_demo / framingham_figs 一致）。"""
    mpl.rcParams.update({
        "figure.dpi": 110, "savefig.dpi": 300, "font.size": 9,
        "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
        "grid.color": "#EEEEEE", "grid.linewidth": .5,
        "xtick.direction": "in", "ytick.direction": "in",
        "legend.frameon": False, "savefig.bbox": "tight",
    })


def default_outdir():
    return os.environ.get("SCIPLOT_OUT", os.path.join(REPO, "templates", "_preview"))


def save_fig(fig, name, outdir=None, formats=("png", "pdf")):
    """导出 PNG(300dpi)+PDF(矢量)；遵循 Python导出规范.md。"""
    outdir = outdir or default_outdir()
    os.makedirs(outdir, exist_ok=True)
    for ext in formats:
        fig.savefig(os.path.join(outdir, f"{name}.{ext}"))
    plt.close(fig)
    print(f"  -> {name} ({', '.join(formats)})  @ {outdir}")
