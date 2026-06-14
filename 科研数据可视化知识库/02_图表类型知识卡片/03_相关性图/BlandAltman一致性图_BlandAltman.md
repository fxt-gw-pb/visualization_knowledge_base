---
chart_name: Bland-Altman一致性图
chart_name_en: Bland-Altman agreement plot
chart_family: 相关性图
data_type:
  - paired_measurements
recommended_backend:
  r: ggplot2
  python: matplotlib
difficulty: basic
priority: high
status: tested
tags:
  - dataviz
  - chart
  - bland-altman
  - agreement
  - method-comparison
  - reliability
  - r
  - python
---

# Bland-Altman 一致性图 Bland-Altman agreement plot

> 比较**两种测量方法/设备/评分者**测同一批对象时一致不一致：横轴=两法均值，纵轴=两法之差，画**偏倚(bias)**与**95% 一致性界限(LoA)**。回答“新方法能不能替代旧方法”——这是相关系数回答不了的问题。

## 1. 图表定位

回答“**两种方法的差异有多大、随测量水平变不变、能否互换**”。相关高 ≠ 一致(系统偏倚也能高相关)；Bland-Altman 直接看差值的偏倚与离散。

## 2. 适用场景

- 方法学比较：新仪器 vs 金标准、自动 vs 人工、可穿戴 vs 临床测量。
- 评分者/重复测量一致性(信度)。
- 替代终点/简化测量的可行性论证。

## 3. 不适用场景

- 想看“相关/预测关系”而非“能否互换” → [[散点图_Scatter]] + 回归。
- 一种方法是真值、要看准确度 → 用偏差/RMSE，而非一致性。
- 配对前提不满足(非同一对象同条件测两次) → 不适用。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| method1 | 连续 | 方法 1 测量值 | 必需 |
| method2 | 连续 | 方法 2 测量值(同对象配对) | 必需 |

派生：`mean=(m1+m2)/2`、`diff=m1−m2`、`bias=mean(diff)`、`LoA=bias±1.96·sd(diff)`。

## 5. 图表架构选择

### 5.1 基础架构
- x=两法均值；y=两法之差；散点 + 偏倚实线 + 上下 LoA 虚线 + y=0 参考。
- 右侧标注 bias 与 ±1.96SD 数值。

### 5.2 高质量架构
- LoA 加 95%CI(误差带)；点多时透明/密度。
- 检查**比例偏倚**(差值随均值变化)：可加差值~均值回归线。
- 差值非正态/有趋势 → 提示需对数变换或回归法 LoA。

## 6. 配色选择

### 6.1 默认配色
散点用 `med_case_control` low 蓝(中性)；偏倚线/LoA 用灰(实/虚区分)；y=0 淡黑。见 [[连续变量配色]]。

### 6.2 色盲友好配色
单色点 + 灰线(实线=bias、虚线=LoA) 靠线型区分，不依赖颜色。

### 6.3 医学研究推荐配色
传统黑白：黑点 + 实/虚灰线，简洁。

## 7. R 实现方案

### 7.1 推荐包
`blandr` / `BlandAltmanLeh`（专用）；或 ggplot 手绘(均值/差值 + hline)。

### 7.2 关键参数
`bias=mean(diff)`、`±1.96*sd(diff)`；`geom_point` + `geom_hline(bias, lo, hi)` + 右侧 `geom_text`，`coord_cartesian(clip="off")` 给标签留白。

### 7.3 可执行模板
**`templates/r/blandaltman.R`**。换数据：`m1/m2` 改两法配对测量。

## 8. Python 实现方案

### 8.1 推荐包
matplotlib（手绘）；`pingouin`/`statsmodels` 可算一致性统计量。

### 8.2 关键参数
`mean、diff、bias、loa`；`scatter` + `axhline(bias/loa)` + 右缘文本；x 上限留白放标签。

### 8.3 可执行模板
**`templates/python/blandaltman.py`**。换真实数据改 `m1/m2`。

## 9. 示例图像

### 9.1 网络优秀示例
参考 Bland & Altman 1986 原图与 `blandr` 文档。

### 9.2 本库模板 demo（合成数据，双后端对齐）
Python（matplotlib）：

![[tpl_blandaltman_py.png]]

R（ggplot2）：

![[tpl_blandaltman_r.png]]

> 偏倚约 −1.4(方法 2 系统性略高)，95% LoA 约 (−13, +10)，差值不随均值系统变化(无明显比例偏倚)——两法是否可互换取决于该 LoA 是否在临床可接受范围内；双后端一致。

## 10. 常见错误
- 用相关系数/R² 论证一致性(高相关掩盖系统偏倚)。
- 把一种方法当 x 轴(应用两法均值，否则引入回归假象)。
- 忽略比例偏倚(差值随均值变)仍用固定 LoA。
- 不结合临床可接受界限解读 LoA(只给数字不下结论)。
- 差值非正态仍用 ±1.96SD(应变换或用百分位法)。

## 11. 自动返修规则
- 检测到用某方法作 x 轴 → 改为两法均值。
- 差值随均值有趋势 → 提示比例偏倚 + 回归法 LoA。
- 差值明显非正态 → 提示对数变换。
- 缺 LoA/偏倚线 → 自动补三条线 + 数值。

## 12. 与其他图表的关系
- 与 [[散点图_Scatter]] 互补：散点+回归看“关系”，Bland-Altman 看“能否互换”。
- 与 [[校准曲线_Calibration]] 概念相邻(都查“预测/测量 vs 真实”的一致)，但对象不同。

## 13. 质量检查清单
- [ ] x 轴用两法均值(非单一方法)？
- [ ] 画了 bias + 95% LoA(及其 CI)？
- [ ] 检查了比例偏倚？
- [ ] 差值正态性满足(否则变换)？
- [ ] 结合临床可接受界限解读？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-14 | v0.1 | 建卡 + 双后端可执行模板(均值-差值 + bias + LoA) + demo 图，状态 tested | 未加 LoA 的 CI、未做比例偏倚回归 | 加 LoA 95%CI 带 + 差值~均值回归线 |

相关：[[散点图_Scatter]] · [[校准曲线_Calibration]] · [[连续变量配色]]
