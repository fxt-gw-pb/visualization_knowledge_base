---
chart_name: Meta分析森林图
chart_name_en: Meta-analysis forest plot
chart_family: 证据合成图
data_type:
  - study_effect_ci
  - weights
recommended_backend:
  r: ggplot2
  python: matplotlib
difficulty: intermediate
priority: high
status: tested
tags:
  - dataviz
  - chart
  - meta-analysis
  - forest-plot
  - pooled-effect
  - heterogeneity
  - evidence-synthesis
  - r
  - python
---

# Meta 分析森林图 Meta-analysis forest plot

> 把纳入的每项研究效应量（OR/RR/HR）按**权重**画成方块+CI，底部用**菱形**给合并效应，并报**异质性 I²/τ²**。荟萃分析的“主结果图”，一张图讲清“综合起来到底有没有效应、证据有多一致”。

## 1. 图表定位

回答“**多项研究合起来的效应是多少、各研究权重几何、彼此一致吗**”。方块大小=权重（精度），菱形宽度=合并 CI，I² 量化异质性。

## 2. 适用场景

- 系统综述/荟萃分析的主结果（几乎必有）。
- 亚组/敏感性合并对比（按设计、人群分层合并）。
- 把同一问题的多来源 RWD 证据汇总。

## 3. 不适用场景

- 只有 1 项研究 → 用单研究 [[森林图_ForestPlot]]。
- 研究间临床/方法异质性过大、不应合并 → 只做定性综述。
- 想看偏倚 → 配 [[漏斗图_Funnel]]，森林图不查偏倚。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| study | 文本 | 研究标识（作者+年份） | 必需 |
| effect | 数值 | 效应量 OR/RR/HR（或 log 效应） | 必需 |
| ci_low / ci_high | 数值 | 95%CI | 必需 |
| (weight) | 数值 | 权重，可由 1/方差自动算 | 自动 |

权重 `w = 1/SE²`（固定效应）或 `1/(SE²+τ²)`（随机效应）；SE 由 CI 反推 `(ln hi − ln lo)/(2×1.96)`。

## 5. 图表架构选择

### 5.1 基础架构
- y=各研究（含合并行）；x=效应量(log 轴)；方块=点估计、横线=CI；ref=1 竖虚线。
- 底部菱形=合并效应；右侧列出数值 + 权重%。

### 5.2 高质量架构
- 方块面积 ∝ 权重；标题/角注报 `I²、τ²、合并 CI、异质性 p`。
- 分组合并加亚组小菱形 + 组间差异检验。
- 左列研究名、右列“效应(CI) 权重%”对齐成表格式。

## 6. 配色选择

### 6.1 默认配色
研究方块用 `med_case_control` low 蓝（中性），合并菱形用 `effect_dir` harm 红（醒目，仅表“汇总”不表方向）；ref 线灰。见 [[模型效应方向配色]]。

### 6.2 色盲友好配色
单色方块 + 深色菱形即可（靠形状区分研究/合并），无需多彩。

### 6.3 医学研究推荐配色
约定俗成黑/蓝方块 + 黑/红菱形；全文一致。

## 7. R 实现方案

### 7.1 推荐包
`meta`（`metabin/metagen` + `forest()`）或 `metafor`（`rma` + `forest()`）最标准；本机无 → 手算 DerSimonian-Laird + ggplot。

### 7.2 关键参数
逆方差：`wi=1/sei²`；`Q、I²、τ²`；随机效应 `wr=1/(sei²+τ²)`；菱形用 `geom_polygon`，方块 `size∝w`。

### 7.3 可执行模板
**`templates/r/metaforest.R`**（手算 DL 随机效应，免 meta/metafor）。换数据：`d` 填 study/OR/lo/hi（或直接给 log 效应+SE）。

## 8. Python 实现方案

### 8.1 推荐包
`statsmodels`（无专用 meta 类，常自算）或手算 + matplotlib；`PythonMeta`/`pymare` 可选。

### 8.2 关键参数
同公式向量化算 `I²/τ²`；`scatter(s∝weight, marker="s")` + `Polygon` 菱形 + log 轴。

### 8.3 可执行模板
**`templates/python/metaforest.py`**。换真实数据改 `study/OR/lo/hi`。

## 9. 示例图像

### 9.1 网络优秀示例
参考 `meta`/`metafor` 的 `forest()` 范式与 Cochrane 综述森林图。

### 9.2 本库模板 demo（合成数据，双后端对齐）
Python（matplotlib）：

![[tpl_metaforest_py.png]]

R（ggplot2）：

![[tpl_metaforest_r.png]]

> 5 项研究合并 OR=1.41 (1.16–1.71)，菱形整体落在 1 右侧 → 有效应；I²=36% 属中度异质性，用随机效应合理；双后端一致。

## 10. 常见错误
- 在原始尺度（非 log）平均效应量 → 偏倚；必须 log 尺度合并。
- 异质性大仍用固定效应 → 低估 CI。
- 方块大小没映射权重，读者误判贡献。
- 不报 I²/τ²，无法判断能不能合并。
- 把红色菱形当“有害方向”——这里红只表“汇总行”，方向看其相对 ref。

## 11. 自动返修规则
- 检测到原始尺度平均 → 强制 log 尺度合并。
- I² 高(>50%)却用固定效应 → 提示改随机效应。
- 方块未按权重缩放 → 自动 `size∝1/var`。
- 缺异质性统计量 → 自动在角注补 I²/τ²。

## 12. 与其他图表的关系
- 与 [[漏斗图_Funnel]] 配套：森林图给结论，漏斗图查偏倚。
- 与 [[森林图_ForestPlot]] 同源但多“权重+菱形+异质性”；亚组合并见 [[亚组森林图_Subgroup]]。

## 13. 质量检查清单
- [ ] 效应在 log 尺度合并？
- [ ] 固定/随机效应选择与 I² 匹配？
- [ ] 方块面积映射权重？
- [ ] 报了 I²/τ²/合并 CI？
- [ ] ref 线 + 数值列对齐？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-14 | v0.1 | 建卡 + 双后端可执行模板（手算 DL 随机效应 + 菱形 + I²）+ demo 图，状态 tested | 未做亚组合并/预测区间 | 加亚组小菱形 + 95% 预测区间 |

相关：[[漏斗图_Funnel]] · [[森林图_ForestPlot]] · [[亚组森林图_Subgroup]]
