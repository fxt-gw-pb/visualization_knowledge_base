---
chart_name: 竞争风险累积发病图
chart_name_en: Cumulative incidence (competing risks)
chart_family: 生存分析图
data_type:
  - time_to_event
  - competing_event
  - categorical_group
recommended_backend:
  r: survival (broom)
  python: lifelines
difficulty: advanced
priority: high
status: tested
tags:
  - dataviz
  - chart
  - competing-risks
  - cumulative-incidence
  - survival
  - rwd
  - r
  - python
---

# 竞争风险累积发病图 Cumulative incidence (competing risks)

> 当存在**竞争事件**（发生它就不可能再发生目标事件，如“死于其他原因”阻断了“目标事件”）时，用累积发病函数(CIF)而非 1−KM 来估计目标事件的累积风险。RWD 老年/多病共存队列常见。

## 1. 图表定位

回答“**考虑竞争事件后，目标事件随时间的累积发生概率**”。CIF 正确扣除被竞争事件“抢走”的人群，避免 1−KM 高估。

## 2. 适用场景

- 结局有竞争风险：如“心血管死亡”vs“非心血管死亡”、“再入院”vs“死亡”。
- 老年/重病/长随访 RWD 队列（竞争死亡不可忽略）。
- 按暴露/治疗分组比较目标事件的累积发病。

## 3. 不适用场景

- 无竞争事件（仅一种事件 + 删失）→ 用 [[KM生存曲线_KaplanMeier]]（1−KM 即可）。
- 想要协变量调整的竞争风险效应 → Fine-Gray(sdHR) 或 cause-specific Cox + [[森林图_ForestPlot]]（本卡是未调整 CIF）。
- 把 1−KM 当 CIF 用（**经典错误**，竞争风险下高估）。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| time | continuous | 到首个事件/删失时间 | 必需 |
| event | categorical | 0=删失, 1=目标事件, 2=竞争事件(可多) | 必需 |
| group | categorical | 分组 | 比较时必需 |

每人一条记录；event 是**多类别**（非二分）。

## 5. 图表架构选择

### 5.1 基础架构
- x=时间，y=累积发病概率(0–1)；阶梯曲线；按组上色，只画**目标事件**的 CIF。
- 各组 CIF 起点 0、随时间单调不减。

### 5.2 高质量架构
- 可叠竞争事件 CIF（不同线型）说明竞争比重。
- 配 Gray's test p 值（组间 CIF 差异）。
- risk table / 数量标注；末端样本少处谨慎解读。
- 多事件时堆叠 CIF（各状态概率和=1−生存）。

## 6. 配色选择

### 6.1 默认配色
分组用 [[医学二分类配色]]（暴露暖/对照冷）或 `cat_main`；目标事件实线、竞争事件虚线/浅色区分。

### 6.2 色盲友好配色
Okabe-Ito + 线型冗余（目标实/竞争虚）。

### 6.3 医学研究推荐配色
暴露组暖色突出；竞争事件用弱化样式避免喧宾夺主。

## 7. R 实现方案

### 7.1 推荐包
本库默认：`survival`（event 设为因子的多状态 `survfit`）+ `broom` 整理。进阶：`cmprsk`(`cuminc`+Gray test)、`tidycmprsk`、`survminer::ggcompetingrisks`（需另装）。

### 7.2 关键参数
`event` 转因子(0=censor)；`survfit(Surv(time,event)~group)` 多状态；`broom::tidy()` 取目标 state；`geom_step`。

### 7.3 可执行模板
**`templates/r/cif.R`**（survival + broom，免 cmprsk）。核心：
```r
df$event <- factor(df$event, 0:2, c("censor","event1","event2"))
fit <- survfit(Surv(time, event) ~ group, data = df)
td <- subset(broom::tidy(fit), state == "event1")   # 目标事件 CIF
```

## 8. Python 实现方案

### 8.1 推荐包
lifelines（`AalenJohansenFitter`）

### 8.2 关键参数
`AalenJohansenFitter().fit(T, event, event_of_interest=1)`；并列时间需轻微抖动；取 `cumulative_density_`。

### 8.3 可执行模板
**`templates/python/cif.py`**。核心：
```python
ajf = AalenJohansenFitter(seed=7)
ajf.fit(t + jitter, event, event_of_interest=1)
ax.step(ajf.cumulative_density_.index, ajf.cumulative_density_.iloc[:,0], where="post")
```

## 9. 示例图像

### 9.1 网络优秀示例
参考 cmprsk `cuminc` / tidycmprsk 文档的竞争风险 CIF 范式。

### 9.2 本库模板 demo（合成竞争风险数据，双后端对齐）
Python（lifelines Aalen-Johansen）：

![[tpl_cif_py.png]]

R（survival 多状态 + broom）：

![[tpl_cif_r.png]]

> 目标事件 CIF：暴露组累积发病明显高于非暴露组；曲线已扣除竞争事件影响（非 1−KM）。双后端一致。

## 10. 常见错误
- 用 1−KM 当 CIF（竞争风险下系统性高估目标事件风险）——最常见错误。
- 把竞争事件当普通删失处理。
- 多组只比目标事件不报 Gray's test。
- 末端样本极少仍下强结论。
- 把未调整 CIF 当作效应估计（需 Fine-Gray/cause-specific 模型）。

## 11. 自动返修规则
- 检测到结局其实只有一种事件 → 提示改用 [[KM生存曲线_KaplanMeier]]。
- 用了 1−KM → 警告并切换 CIF。
- 缺组间检验 → 提示加 Gray's test。
- 时间并列导致估计器报错 → 自动轻微抖动。

## 12. 与其他图表的关系
- vs [[KM生存曲线_KaplanMeier]]：无竞争用 KM，有竞争用 CIF。
- vs [[森林图_ForestPlot]]：CIF 是未调整曲线，调整效应用 Fine-Gray/cause-specific Cox 的 sdHR/HR 画森林。
- 与 [[CONSORT流程图_Consort]]：交代竞争事件与删失的人数流转。

## 13. 质量检查清单
- [ ] 确有竞争事件（否则用 KM）？
- [ ] 用 CIF 而非 1−KM？
- [ ] 竞争事件按竞争处理（非普通删失）？
- [ ] 组间差异有检验（Gray's test）？
- [ ] 末端样本量足够支撑结论？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建卡 + 双后端可执行模板（R survival/broom、Py lifelines）+ demo 图，状态 tested | 未加 Gray's test / risk table | 加 Gray test + 堆叠 CIF + Fine-Gray 森林联动 |

相关：[[KM生存曲线_KaplanMeier]] · [[森林图_ForestPlot]] · [[CONSORT流程图_Consort]] · [[_生存分析图族索引|生存分析图族索引]]
