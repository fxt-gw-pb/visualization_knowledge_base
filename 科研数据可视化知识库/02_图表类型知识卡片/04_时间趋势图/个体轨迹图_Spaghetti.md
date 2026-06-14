---
chart_name: 个体轨迹图
chart_name_en: Spaghetti plot (individual trajectories)
chart_family: 时间趋势图
data_type:
  - longitudinal
  - repeated_measures
recommended_backend:
  r: ggplot2
  python: matplotlib
difficulty: intermediate
priority: high
status: tested
tags:
  - dataviz
  - chart
  - spaghetti
  - trajectory
  - longitudinal
  - mixed-model
  - ehr
  - r
  - python
---

# 个体轨迹图 Spaghetti plot

> 纵向/重复测量数据里，把**每个个体随时间的轨迹**画成一根细线，再叠上**组均值±CI**的粗线。回答“个体怎么变、组间趋势差不差”，兼顾个体异质性与总体趋势——EHR 纵向随访的本命图（Framingham PERIOD 1–3 正是此结构）。

## 1. 图表定位

回答“**随访期间指标怎么演变**”：细线展示个体异质性与轨迹形态，粗线给可推断的组均值趋势。比只画组均值更诚实(暴露个体变异)，比只画个体更可读(给出趋势)。

## 2. 适用场景

- 纵向队列/RCT 的重复测量(生物标志物、量表分随时间)。
- 混合效应模型(LMM)结果的可视化伴随图。
- EHR 多次就诊指标轨迹、治疗前后变化。

## 3. 不适用场景

- 横断面(每人一个时点) → [[散点图_Scatter]]/[[箱线图_Boxplot]]。
- 个体数极多(成百上千) → 细线糊成一团，改抽样/分位带/[[山峦图_Ridgeline]]或热力轨迹(lasagna)。
- 只关心组均值 → [[折线趋势图_Line]] 足够。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| id | 标识 | 个体 ID(每人多行) | 必需 |
| time | 数值/有序 | 时间/随访期 | 必需 |
| value | 连续 | 指标值 | 必需 |
| group | 分类 | 组别(可选) | 可选 |

**长格式**(每人每时点一行)。注意缺失/不等间隔随访的处理。

## 5. 图表架构选择

### 5.1 基础架构
- x=时间；y=指标；`group=id` 画细线(低透明)；叠组均值粗线 + 95%CI 带。
- 组别用颜色区分。

### 5.2 高质量架构
- 个体线足够淡(alpha 0.1–0.3)避免压过均值。
- 均值线建议用**混合模型**拟合(处理不等间隔/缺失/个体相关)，而非简单逐点均值。
- 可高亮少数典型个体；不等间隔随访按真实时间放点。

## 6. 配色选择

### 6.1 默认配色
组别用 `cat_main`(Okabe-Ito)；个体线=组色低透明，均值线=组色实粗。见 [[分类变量配色]]。

### 6.2 色盲友好配色
Okabe-Ito 天然色盲友好；组少时辅以线型区分均值线。

### 6.3 医学研究推荐配色
处理/对照用 [[医学二分类配色]]；个体线统一淡灰也可(只让均值线带组色)。

## 7. R 实现方案

### 7.1 推荐包
ggplot2(`geom_line(aes(group=id))` + `stat_summary`/`geom_ribbon`)；均值轨迹可用 `lme4/nlme` 拟合。

### 7.2 关键参数
个体线 `linewidth=.25, alpha=.22`；均值 `group_by(grp,time) summarise(mean, se)` + `geom_ribbon` + 粗 `geom_line`。

### 7.3 可执行模板
**`templates/r/spaghetti.R`**(个体细线 + 组均值±CI)。换数据：长格式 `df(id,visit,y,grp)`；均值改用混合模型预测即可升级。

## 8. Python 实现方案

### 8.1 推荐包
matplotlib(分组画线) + pandas(聚合)；混合模型用 `statsmodels.mixedlm`。

### 8.2 关键参数
`groupby(id)` 画细线；`groupby(group,time)` 求 `mean/se` → `fill_between` + 粗线。

### 8.3 可执行模板
**`templates/python/spaghetti.py`**。换真实数据改 `df`(长格式)。

## 9. 示例图像

### 9.1 网络优秀示例
参考纵向数据分析教材(Fitzmaurice 等)与 `ggplot2` 纵向轨迹范式。

### 9.2 本库模板 demo（合成数据，双后端对齐）
Python（matplotlib）：

![[tpl_spaghetti_py.png]]

R（ggplot2）：

![[tpl_spaghetti_r.png]]

> 治疗组个体轨迹整体下行、对照组基本平稳；粗均值线 + CI 带清晰显示组间随时间的分化；个体细线保留了异质性；双后端一致。

## 10. 常见错误
- 个体线太深，盖住均值趋势。
- 用简单逐点均值代替混合模型(忽略缺失/不等间隔/个体内相关)。
- 个体太多仍硬画细线，糊成黑团。
- 不等间隔随访被当等距画(扭曲斜率)。
- 只画均值不画个体(掩盖异质性)，或只画个体不给趋势。

## 11. 自动返修规则
- 个体线过深 → 自动降 alpha。
- 个体数过多 → 提示抽样/分位带/lasagna 替代。
- 检测到不等间隔 → 按真实时间定位 x。
- 缺均值趋势 → 自动叠加组均值±CI(建议混合模型)。

## 12. 与其他图表的关系
- 是 [[折线趋势图_Line]] 的“保留个体”版本；个体过多时退化为分位带或热力轨迹。
- 与 [[Swimmer图_Swimmer]]：Swimmer 是事件时间线，Spaghetti 是连续指标轨迹。
- 常作混合模型(LMM)结果的伴随可视化。

## 13. 质量检查清单
- [ ] 个体线透明度合适(不盖均值)？
- [ ] 叠加了组均值±CI？
- [ ] 均值是否用了合适模型(混合模型优先)？
- [ ] 不等间隔随访按真实时间？
- [ ] 个体过多时换了表达方式？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-14 | v0.1 | 建卡 + 双后端可执行模板(个体细线 + 组均值±CI) + demo 图，状态 tested | 均值用逐点聚合(非混合模型) | 接 lme4/mixedlm 拟合均值轨迹 + lasagna 变体 |

相关：[[折线趋势图_Line]] · [[Swimmer图_Swimmer]] · [[山峦图_Ridgeline]] · [[分类变量配色]]
