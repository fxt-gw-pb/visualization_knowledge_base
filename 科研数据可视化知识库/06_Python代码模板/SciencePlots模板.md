---
title: SciencePlots 模板
type: code-template
status: active
backend: python
updated: 2026-06-10
tags:
  - dataviz
  - python
  - scienceplots
  - matplotlib
  - template
---

# SciencePlots 模板

> 给 matplotlib 一键套上论文风（紧凑、刻度朝内、衬线/无衬线、IEEE/Nature 风）。是 [[matplotlib通用主题]] 的“现成皮肤”。

## 1. 安装与基本用法

```python
# pip install SciencePlots
import scienceplots
import matplotlib.pyplot as plt

plt.style.use(["science"])                  # 基础论文风（默认用 LaTeX 渲染）
# 叠加子样式：
plt.style.use(["science", "nature"])        # Nature 风
plt.style.use(["science", "ieee"])          # IEEE 双栏窄图
```

## 2. 无 LaTeX 环境（重要）

SciencePlots 默认调用本机 LaTeX 渲染文字，没装会报错。关掉：

```python
plt.style.use(["science", "no-latex"])      # >>> 不依赖 LaTeX
# 或叠加： ["science", "nature", "no-latex"]
```

## 3. 常用子样式

| 子样式 | 效果 |
|---|---|
| `science` | 基础：刻度朝内、紧凑、衬线 |
| `nature` | Nature 风（无衬线、特定字号）|
| `ieee` | IEEE 双栏窄图、黑白友好 |
| `grid` | 加浅网格 |
| `no-latex` | 不用 LaTeX 渲染 |
| `scatter` | 散点优化 |
| `high-vis` / `bright` / `vibrant` / `muted` | 色盲友好配色组（基于 Paul Tol）|

## 4. 与本库配色/尺寸协同

```python
plt.style.use(["science", "no-latex"])
mm = 1/25.4
fig, ax = plt.subplots(figsize=(89*mm, 70*mm))   # 单栏，见 论文单栏双栏尺寸
# 配色仍用本库 registry：
okabe = ["#E69F00","#56B4E9","#009E73","#0072B2","#D55E00"]
for i,(k,g) in enumerate(df.groupby("grp")):
    ax.plot(g.x, g.y, color=okabe[i], label=k)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.legend()
fig.savefig("fig.pdf")                            # 矢量
```

## 5. 注意事项

- SciencePlots 改的是**样式（线宽/字体/刻度）**，**不替你选语义配色**——配色仍走 [[配色系统总览]]。
- `science` 默认衬线体；要无衬线叠 `nature` 或自设 `font.family`。
- 与 seaborn 混用时，先 `plt.style.use` 再画，避免被 seaborn 主题覆盖。
- 论文投稿仍按目标期刊调尺寸/字号（[[论文单栏双栏尺寸]]）。

## 6. 常见错误（→ 返修）

- ❌ 没装 LaTeX 直接用 `science` 报错 → 加 `no-latex`。
- ❌ 以为它会自动选好配色 → 仍要手动接 Okabe-Ito/viridis。
- ❌ 样式被后续 seaborn/rcParams 覆盖 → 注意调用顺序。

相关：[[matplotlib通用主题]] · [[配色系统总览]] · [[论文单栏双栏尺寸]] · [[Python导出规范]]
