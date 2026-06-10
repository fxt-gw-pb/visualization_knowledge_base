---
chart_name: Swimmer plot
chart_name_en: Swimmer plot
chart_family: 医学流行病学常用图
data_type:
  - per_patient_timeline
  - events
recommended_backend:
  r: ggplot2
  python: matplotlib
difficulty: intermediate
priority: medium
status: tested
tags:
  - dataviz
  - chart
  - swimmer
  - patient-timeline
  - oncology
  - rwd
  - r
  - python
---

# Swimmer plot 患者时间线

> 每名患者一条横向泳道=随访时长，叠加关键事件标记（应答、进展、死亡）与“仍在随访”箭头。在病例级别讲清**每个人何时发生了什么**，肿瘤/RWD 个体随访经典图。

## 1. 图表定位

回答“**每名患者的随访轨迹与事件时序是怎样的**”。不是聚合统计，而是**病例级**叙事：谁应答了、谁进展了、谁还在治疗、谁死亡。

## 2. 适用场景

- 早期/小样本临床研究、肿瘤个案系列、RWD 个体随访展示。
- 强调**事件时序与持续时间**（应答持续期 DoR、至进展时间 TTP）。
- 配合疗效汇报，直观看异质性（谁长期获益）。

## 3. 不适用场景

- 样本量大（> ~50–80 人）→ 泳道太密，改聚合（[[KM生存曲线_KaplanMeier]]/[[竞争风险累积发病图_CompetingRisk]]）。
- 只关心组间生存概率 → KM 更合适。
- 需要统计推断 → swimmer 是描述性叙事图，不做检验。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| pid | id | 患者标识 | 必需 |
| duration | continuous | 随访时长（条长）| 必需 |
| 事件时点 | continuous | 应答/进展等发生时间 | 可选 |
| death / ongoing | bool | 是否死亡 / 是否仍随访 | 可选 |

每行一名患者；事件以时点列叠加为标记。

## 5. 图表架构选择

### 5.1 基础架构
- y=患者（按随访时长排序），x=时间；横条=随访时长；点标记=事件；箭头=仍在随访。

### 5.2 高质量架构
- 按随访时长排序泳道，形成“瀑布”观感。
- 形状/颜色编码事件类型 + 图例；箭头表示删失/进行中。
- 可按亚组分面或着色泳道（疗效分层）。
- 起点对齐到入组(0)或关键基线事件。

## 6. 配色选择

### 6.1 默认配色
泳道用中性单色；事件标记用 `cat_main` 区分类型（应答/进展/死亡），见 [[分类变量配色]]。形状与颜色双重编码。

### 6.2 色盲友好配色
不同形状(▲应答 / ✕进展 / ■死亡 / →进行中)做冗余，配 Okabe-Ito。

### 6.3 医学研究推荐配色
事件类型颜色全文一致；死亡用深/黑、进行中用灰箭头。

## 7. R 实现方案

### 7.1 推荐包
ggplot2（`geom_segment` 泳道 + `geom_point` 事件 + `arrow`）；ggswim（专用，需另装）。

### 7.2 关键参数
按 duration 排序设 y；`geom_segment(linewidth=)` 作条；`geom_point(shape=)` 标事件；`arrow()` 标进行中。

### 7.3 可执行模板
**`templates/r/swimmer.R`**。核心：
```r
geom_segment(aes(0, y, xend = duration, yend = y), linewidth = 3) +
geom_point(aes(response, y), shape = 17) + geom_point(aes(progression, y), shape = 4)
```

## 8. Python 实现方案

### 8.1 推荐包
matplotlib（`barh` 泳道 + `scatter` 事件 + `annotate` 箭头）

### 8.2 关键参数
`ax.barh(y, duration)`；`ax.scatter(t, y, marker=)`；`ax.annotate("", arrowprops=)` 标进行中；自定义图例。

### 8.3 可执行模板
**`templates/python/swimmer.py`**。核心见文件 `# >>> PARAM`（每行一患者：duration/response/progression/death/ongoing）。

## 9. 示例图像

### 9.1 网络优秀示例
参考肿瘤临床试验常见 swimmer plot（应答/进展/持续治疗标记）范式。

### 9.2 本库模板 demo（合成患者数据，双后端对齐）
Python（matplotlib）：

![[tpl_swimmer_py.png]]

R（ggplot2）：

![[tpl_swimmer_r.png]]

> 16 名患者按随访时长排序：▲应答、✕进展、■死亡、→仍在随访；个体异质性与事件时序一目了然。双后端一致。

## 10. 常见错误
- 患者过多导致泳道密不可读。
- 事件标记只靠颜色无形状（色盲不可辨）。
- 缺图例，读者不懂标记含义。
- 时间起点不统一（有的从入组、有的从确诊）。
- 用 swimmer 代替群体生存统计下结论。

## 11. 自动返修规则
- 患者 > ~60 → 提示抽样/分面或改 KM。
- 标记仅颜色编码 → 自动加形状冗余 + 图例。
- 时间起点不一致 → 提示统一对齐。
- 泳道重叠 → 增大行距/缩标记。

## 12. 与其他图表的关系
- vs [[KM生存曲线_KaplanMeier]]/[[竞争风险累积发病图_CompetingRisk]]：swimmer 病例级叙事，KM/CIF 群体概率。
- vs [[折线趋势图_Line]]（spaghetti）：spaghetti 看连续指标轨迹，swimmer 看离散事件时序。
- 与 [[CONSORT流程图_Consort]] 互补：流程图给入排总量，swimmer 给个体随访。

## 13. 质量检查清单
- [ ] 患者数适中、泳道可读？
- [ ] 事件用形状+颜色双编码 + 图例？
- [ ] 时间起点统一、坐标有单位？
- [ ] 排序（按时长）增强可读？
- [ ] 未把描述性图当统计结论？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建卡 + 双后端可执行模板 + demo 图，状态 tested | R 端事件图例未显式映射 | 加亚组分面 + 持续应答区段着色 + ggswim 备选 |

相关：[[KM生存曲线_KaplanMeier]] · [[竞争风险累积发病图_CompetingRisk]] · [[折线趋势图_Line]] · [[CONSORT流程图_Consort]]
