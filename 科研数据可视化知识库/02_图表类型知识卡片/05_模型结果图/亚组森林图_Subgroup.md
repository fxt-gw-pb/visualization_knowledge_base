---
chart_name: 亚组分析森林图
chart_name_en: Subgroup forest plot
chart_family: 模型结果图
data_type:
  - subgroup_effect_ci
  - interaction_p
recommended_backend:
  r: ggplot2
  python: matplotlib
difficulty: intermediate
priority: high
status: tested
tags:
  - dataviz
  - chart
  - subgroup
  - forest-plot
  - interaction
  - effect-modification
  - r
  - python
---

# 亚组分析森林图 Subgroup forest plot

> 把处理/暴露效应在各**亚组**（性别、年龄段、合并症…）里分别画成森林图，并标**交互 p(P-interaction)**，回答“**效应在不同人群里是否一致**”——即效应修饰/异质性治疗效应(HTE)。RCT 与 RWD 的标准“图 3/4”。

## 1. 图表定位

回答“**这个效应对所有人都一样，还是某些亚组更受益/更受害**”。每个亚组层一行点+CI，按分层变量分组并加表头与 P-interaction。

## 2. 适用场景

- RCT/队列的预设亚组分析（效应一致性）。
- RWD 异质性治疗效应(HTE)初探。
- 检验某协变量是否为效应修饰因子。

## 3. 不适用场景

- 亚组未预设、纯事后大量切分 → 多重比较假阳性，慎用/标注探索性。
- 想看“整体一个效应” → [[森林图_ForestPlot]]。
- 想看连续修饰因子的平滑变化 → [[限制性立方样条_RCS]]（含交互）。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| subgroup | 分类 | 分层变量(表头) + 各层 | 必需 |
| estimate | 数值 | 各层效应 OR/HR/RR | 必需 |
| ci_low / ci_high | 数值 | 95%CI | 必需 |
| p_interaction | 数值 | 该分层变量的交互检验 p | 必需 |

交互 p 来自模型 `outcome ~ treat * subgroup` 的乘积项（或似然比检验），**不是**各层单独 p。

## 5. 图表架构选择

### 5.1 基础架构
- y=亚组（表头行 + 缩进层行）；x=效应(log 轴) + ref=1；点+CI。
- 每个分层变量旁标 P-interaction。

### 5.2 高质量架构
- 左列亚组名（表头加粗、层缩进），右列“效应(CI)”对齐成表。
- 按方向着色（保护/有害/不显著）；可加各层 n / 事件数列。
- 全图共用一条 x 轴与 ref 线。

## 6. 配色选择

### 6.1 默认配色
按效应方向 `effect_dir`：有害红、保护蓝、跨 1 灰；表头黑、P-int 灰。见 [[模型效应方向配色]]。

### 6.2 色盲友好配色
方向用红/蓝(Okabe-Ito) + 跨 1 用灰 + 形状一致；不靠颜色单独承载信息。

### 6.3 医学研究推荐配色
多数期刊用单色点；本库默认方向着色更直观，投稿可按刊改单色。

## 7. R 实现方案

### 7.1 推荐包
`forestploter`（表格式，支持缩进/分组）；或 ggplot 手绘（`geom_pointrange` + 文本列）。

### 7.2 关键参数
表头行 estimate=NA 不画点；`scale_x_log10` + ref=1；`geom_text` 放亚组名/数值/P-int；方向映射颜色。

### 7.3 可执行模板
**`templates/r/subgroup.R`**（ggplot 手绘，含表头/缩进/交互 p）。换数据改 `d`（label/OR/lo/hi/header/p_int）。

## 8. Python 实现方案

### 8.1 推荐包
matplotlib（手绘，`get_yaxis_transform` 放左右文本列）。

### 8.2 关键参数
表头行只放文本+P-int；层行点+CI；`set_xscale("log")` + `minorticks_off()`（避免杂散次刻度标签）。

### 8.3 可执行模板
**`templates/python/subgroup.py`**。换真实数据改 `rows`（label, OR, lo, hi, is_header, p_int）。

## 9. 示例图像

### 9.1 网络优秀示例
参考 NEJM/Lancet RCT 的亚组森林图与 `forestploter` 文档。

### 9.2 本库模板 demo（合成数据，双后端对齐）
Python（matplotlib）：

![[tpl_subgroup_py.png]]

R（ggplot2）：

![[tpl_subgroup_r.png]]

> Age group 的 P-interaction=0.03 提示效应随年龄显著不同（≥50 岁更强），而 Sex/Smoking 一致(P>0.4)；双后端一致。

## 10. 常见错误
- 用各层“是否显著”来判异质性 → 错；要看 **交互 p**，不是层内 p 的有无。
- 大量事后亚组不校正多重比较 → 假阳性。
- 表头行画了点（表头不是一个效应）。
- 各层 x 轴/ref 不统一，无法横向比较。
- 小亚组 CI 极宽仍下强结论。

## 11. 自动返修规则
- 仅有层内 p、缺交互 p → 提示补 P-interaction。
- 表头行误带点 → 自动去除。
- 多个事后亚组 → 提示标注“探索性”+多重比较。
- log 轴杂散次刻度 → 自动 `minorticks_off`。

## 12. 与其他图表的关系
- 是 [[森林图_ForestPlot]] 的分层扩展；连续修饰因子见 [[限制性立方样条_RCS]]。
- 与 [[Meta森林图_MetaForest]] 形似但语义不同：那是跨研究合并，这是单研究内分层。

## 13. 质量检查清单
- [ ] 报的是交互 p 而非层内 p？
- [ ] 亚组是否预设（事后须标注）？
- [ ] 表头/缩进/数值列对齐？
- [ ] 统一 x 轴 + ref 线？
- [ ] 小亚组的不确定性如实呈现？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-14 | v0.1 | 建卡 + 双后端可执行模板（手绘，含表头/交互 p）+ demo 图，状态 tested | 未加 n/事件列 | 加各层样本量/事件数列 + 多重比较校正注释 |

相关：[[森林图_ForestPlot]] · [[限制性立方样条_RCS]] · [[Meta森林图_MetaForest]] · [[模型效应方向配色]]
