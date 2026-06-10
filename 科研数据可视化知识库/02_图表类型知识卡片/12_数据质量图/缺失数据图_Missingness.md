---
chart_name: 缺失数据模式图
chart_name_en: Missing data pattern
chart_family: 数据质量图
data_type:
  - tabular
  - missingness
recommended_backend:
  r: ggplot2 (naniar/VIM 可选)
  python: matplotlib (missingno 可选)
difficulty: basic
priority: high
status: tested
tags:
  - dataviz
  - chart
  - missing-data
  - data-quality
  - ehr
  - rwd
  - r
  - python
---

# 缺失数据模式图 Missing data pattern

> EHR / 真实世界数据(RWD)分析的**第一张图**：看每个变量缺多少、缺失是否成块/成模式、是否与其他变量共缺。决定后续删除/填补策略的前提。

## 1. 图表定位

回答“**哪些变量缺、缺多少、缺得有没有规律**”。区分完全随机缺失(MCAR)、随机缺失(MAR)、非随机缺失(MNAR)的视觉线索——是 RWD 数据质量审计的核心。

## 2. 适用场景

- EHR/登记库/问卷等**普遍含缺失**的真实数据，建模前必做。
- 判断缺失是否集中在某些变量/某些记录/某些时间段。
- 发现“共缺”结构（如某套化验同时缺）→ 提示按就诊类型/科室系统性缺失。
- 决定：完整案例分析 vs 多重填补 vs 删除高缺变量。

## 3. 不适用场景

- 数据几乎无缺失 → 一句话报告即可。
- 想量化缺失机制检验（Little's MCAR test）→ 用统计检验，本图只作探索。
- 变量极多（数百列）→ 先按缺失率筛选/分组，再画子集。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| 任意宽表 | tabular | 行=记录、列=变量，含 NA | 必需 |

直接喂原始 DataFrame；无需预聚合。

## 5. 图表架构选择

### 5.1 基础架构
- **每列缺失比例条**（排序，缺多在前）+ **缺失矩阵**（行=记录抽样，列=变量，深色=缺失）。
- 两者共享列顺序，对齐阅读。

### 5.2 高质量架构
- 矩阵按某关键变量排序行 → 暴露“缺失随某变量变化”的 MAR 线索。
- 共缺热图（变量×变量缺失相关）识别成套缺失。
- 记录级缺失数分布（每行缺几项）。
- 纵向数据：按随访期分面看缺失随时间变化。

## 6. 配色选择

### 6.1 默认配色
二值（缺失/非缺失）：非缺失浅灰、缺失用一个醒目暖色（`med_case_control` 的 high），见 [[分类变量配色]]。**不要花哨**——重点是缺失位置。

### 6.2 色盲友好配色
灰 + 单一暖色，天然安全；缺失也可用纹理/深浅冗余。

### 6.3 医学研究推荐配色
缺失=醒目色引起注意；非缺失=中性。全文一致。

## 7. R 实现方案

### 7.1 推荐包
ggplot2（base 计算缺失，本库默认免依赖）；naniar（`vis_miss`/`gg_miss_var`）、VIM（`aggr`）更专业（需另装）。

### 7.2 关键参数
`colMeans(is.na(df))` 排序；`is.na()` 矩阵 → 长表 `geom_tile`；patchwork 拼条+矩阵。

### 7.3 可执行模板
**`templates/r/missingness.R`**（base + patchwork，免 naniar）。直接喂 `df`，自动按缺失率排序。

## 8. Python 实现方案

### 8.1 推荐包
matplotlib（本库默认）；missingno（`msno.matrix`/`msno.bar`）更省事（需另装）。

### 8.2 关键参数
`df.isna().mean()` 排序；`df.isna()` → `imshow`；上 bar 下 matrix 双面板。

### 8.3 可执行模板
**`templates/python/missingness.py`**。直接喂 `df`，输出“缺失% 条 + 缺失矩阵”。

## 9. 示例图像

### 9.1 网络优秀示例
参考 missingno（Python）`matrix`/`bar` 与 naniar（R）`vis_miss` 范式。

### 9.2 本库模板 demo（合成 EHR 数据，双后端对齐）
Python（matplotlib）：

![[tpl_missingness_py.png]]

R（ggplot2 + patchwork）：

![[tpl_missingness_r.png]]

> 合成 EHR：HbA1c/LDL/eGFR 缺失最多（化验类），Age/Sex/Outcome 无缺；矩阵显示缺失大致随机、未见明显成块。双后端一致。

## 10. 常见错误
- 跳过缺失检查直接建模（完整案例默默丢样本、引偏倚）。
- 只报总缺失率，不看模式（错过 MAR/MNAR 线索）。
- 把缺失当 0 或随手均值填补，不交代机制。
- 变量太多硬画成一团。

## 11. 自动返修规则
- 列 > ~40 → 按缺失率筛选/分组后再画。
- 发现高缺变量（如 >50%）→ 提示考虑删除或专门建模。
- 疑似成块缺失 → 建议按关键变量排序行 + 画共缺热图。
- 纵向数据 → 建议按随访期分面。

## 12. 与其他图表的关系
- 是所有分析的**前置**：缺失处理方式影响后续 [[直方图_Histogram]]/[[森林图_ForestPlot]]/模型评价结论。
- 共缺结构可进一步用 [[热图_Heatmap]] 看变量×变量缺失相关。
- 与 [[CONSORT流程图_Consort]] 配合：排除高缺记录的人数计入流程图。

## 13. 质量检查清单
- [ ] 每变量缺失率清楚（排序 + 标注）？
- [ ] 能看出缺失是否成模式（非纯随机）？
- [ ] 缺失/非缺失配色对比鲜明、色盲友好？
- [ ] 后续缺失处理策略有据可依？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建卡 + 双后端可执行模板（免 naniar/missingno）+ demo 图，状态 tested | — | 可加共缺热图 + 按变量排序行变体 |

相关：[[热图_Heatmap]] · [[CONSORT流程图_Consort]] · [[变量字典]] · [[_数据质量图族索引|数据质量图族索引]]
