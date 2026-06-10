---
chart_name: CONSORT 流程图
chart_name_en: CONSORT flow diagram
chart_family: 医学流行病学常用图
data_type:
  - counts
  - flow_stages
recommended_backend:
  r: ggplot2 (手搓) / DiagrammeR
  python: matplotlib (手搓)
difficulty: intermediate
priority: high
status: tested
tags:
  - dataviz
  - chart
  - consort
  - flowchart
  - epidemiology
  - r
  - python
---

# CONSORT 流程图 CONSORT flow diagram

> 用盒+箭头追踪研究对象从**筛选→入组→分组→分析**各阶段的人数与流失，是 RCT/队列研究论文的标配第一图（CONSORT / STROBE 规范）。

## 1. 图表定位

回答“**多少人被评估、为何排除、各组各阶段还剩多少**”。本质是**带数字的流程图**，保证样本流转透明可审计。

## 2. 适用场景

- RCT 的 CONSORT 流程（评估→排除→随机化→各臂分配/随访/分析）。
- 队列/横断面的入组流程（STROBE）。
- 任何需要交代“样本怎么来的、为何排除、最终纳入多少”的研究。

## 3. 不适用场景

- 展示数据分布/关系/趋势——这是结构流程，不是数据图。
- 阶段极复杂、分支极多 → 改用专业图形工具（graphviz/DiagrammeR）或矢量编辑器手绘。
- 只需汇报最终样本量 → 一句话或小表即可，不必画图。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| 各阶段人数 | int | 评估/排除/入组/各臂/分析 n | 必需 |
| 排除原因 | text + int | 排除明细（原因 + n）| 推荐 |
| 分组结构 | — | 几个臂、几级阶段 | 必需 |

不是“数据集”，而是把**已统计好的关键人数**填进固定结构。

## 5. 图表架构选择

### 5.1 基础架构
- 自上而下盒序：评估 → 入组/随机化 → 各臂分配 → （随访）→ 分析。
- 右侧支出箭头接“排除/失访”侧盒。
- 箭头表示流向；侧盒说明流失原因与数量。

### 5.2 高质量架构
- 主流程居中竖列，排除盒靠右、浅灰填充以区分。
- 每盒数字对齐、字号一致；上下游 n 应能对账（评估−排除=入组）。
- 多臂时用一条横连接器再分叉到各臂。
- 留足盒间距，箭头不穿盒。

## 6. 配色选择

### 6.1 默认配色
主流程盒用单一温和色（`cat_main` 取一色），排除/失访盒用中性浅灰（`#F0F0F0`）以弱化。**避免花哨**——流程图重结构不重色彩。

### 6.2 色盲友好配色
单色 + 灰即可，天然安全；靠位置/文字而非颜色编码（[[色盲友好与打印友好原则]]）。

### 6.3 医学研究推荐配色
遵循期刊：多数 CONSORT 用黑白线框即可，彩色仅作轻度区分主流程/排除。

## 7. R 实现方案

### 7.1 推荐包
ggplot2（`geom_tile`+`geom_text`+`geom_segment` 手搓，导出稳定）；或 DiagrammeR（graphviz 语法，但产 htmlwidget，导 PNG 需额外步骤）。

### 7.2 关键参数
盒：`geom_tile(width=,height=)`+`geom_text(lineheight=)`；箭头：`geom_segment(arrow=arrow())`；`theme_void()`。

### 7.3 可执行模板
**`templates/r/consort.R`**（改 `# >>> PARAM` 的人数/原因）。盒坐标在 `boxes` 数据框，箭头在 `seg`。

## 8. Python 实现方案

### 8.1 推荐包
matplotlib（`FancyBboxPatch` 盒 + `FancyArrowPatch` 箭头）；graphviz 亦可。

### 8.2 关键参数
`FancyBboxPatch(boxstyle="round,pad=...")`、`FancyArrowPatch(arrowstyle="-|>")`、`ax.axis("off")`。

### 8.3 可执行模板
**`templates/python/consort.py`**。所有人数/原因在顶部 `# >>> PARAM`；`box()`/`arrow()` 两个辅助函数控制布局。

## 9. 示例图像

### 9.1 网络优秀示例
参考 CONSORT 2010 官方流程图模板（consort-statement.org）。

### 9.2 本库模板 demo（合成人数，双后端对齐）
Python（matplotlib）：

![[tpl_consort_py.png]]

R（ggplot2 手搓）：

![[tpl_consort_r.png]]

> 评估 1200 − 排除 350 = 入组 850 → 两臂 430/420 → 分析 410/405；上下游人数可对账。改 PARAM 人数即重排。

## 10. 常见错误
- 上下游人数对不上（评估−排除≠入组）。
- 排除盒缺“原因 + 各 n”，只给总数。
- 箭头穿过盒子、布局拥挤。
- 字号/对齐不一致显得潦草。
- 多臂未画清分叉，读者搞不清流向。

## 11. 自动返修规则
- 人数不平衡（不对账）→ 报警并提示核对。
- 盒重叠/箭头穿盒 → 自动增大间距或缩字。
- 排除盒缺原因 → 提示补明细。
- 臂数变化 → 按臂数自动布局横连接器。

## 12. 与其他图表的关系
- 与所有数据图正交：CONSORT 交代“样本来源”，其后才是分布/比较/生存等结果图。
- 队列入组（STROBE）与 RCT（CONSORT）结构类似，复用同模板改文案。

## 13. 质量检查清单
- [ ] 各阶段人数可对账？
- [ ] 排除/失访有原因 + n？
- [ ] 箭头不穿盒、布局清爽？
- [ ] 字号/对齐统一？
- [ ] 多臂分叉清楚？
- [ ] 黑白打印仍可读（不靠颜色编码）？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建卡 + 双后端手搓模板 + demo 图，状态 tested | 复杂多阶段布局需手调 | 可加 DiagrammeR 备选 + STROBE 变体 |

相关：[[图表类型索引]] · [[标签与注释设计]] · [[色盲友好与打印友好原则]]
