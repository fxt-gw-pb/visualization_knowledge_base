---
chart_name: 折线趋势图
chart_name_en: Line plot
chart_family: 时间趋势图
data_type:
  - continuous_time
  - continuous
recommended_backend:
  r: ggplot2
  python: matplotlib/seaborn
difficulty: basic
priority: high
status: tested
tags:
  - dataviz
  - chart
  - line
  - trend
  - longitudinal
  - r
  - python
---

# 折线趋势图 Line plot

> 展示连续/有序变量（多为时间、随访期）上指标的变化。涵盖：单组趋势、均值±CI 趋势带、个体轨迹（spaghetti）。

## 1. 图表定位

回答“**指标随时间/随访怎么变**”：上升/下降/平台/波动；组间趋势差异；个体异质性。

## 2. 适用场景

- 时间序列、随访期（Framingham PERIOD=1/2/3）上的指标变化。
- 组间趋势比较（均值±CI 趋势带）。
- 个体纵向轨迹（spaghetti plot）。
- 强调“连续/有序 + 变化方向”。

## 3. 不适用场景

- x 是无序分类 → 用柱状/点图，别用线“连接”无序类别（暗示不存在的连续性）。
- 线太多成“意大利面团” → 高亮重点 + 灰化其余，或分面。
- 单时点比较 → 箱线/点估计。
- 只有两点还强调“趋势” → [[点估计置信区间图_PointRange]] 或斜率图更诚实。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 必需 |
|---|---|---|---|
| time | continuous/ordered | 时间或有序期（x）| 必需 |
| value | continuous | 指标（y）| 必需 |
| id | id | 个体标识（spaghetti）| 个体轨迹时必需 |
| group | categorical | 分组（颜色/分面）| 可选 |

长格式（每行 = 一个 id 在一个时间点）。Framingham 已是长格式（RANDID × PERIOD）。

## 5. 图表架构选择

### 5.1 基础架构
- x 时间，y 指标；几何 = line（+ point 标测量时点）。
- 多组用颜色 + 线型。

### 5.2 高质量架构
- **均值±CI 趋势带**：`stat_summary` 或 `lineplot(errorbar="ci")`，灰带表示不确定性。
- **个体轨迹 + 组均值**：浅灰细线画每个 id，粗线叠组均值。
- 直接标注线末端组名（[[图例设计]]，少用图例）。
- 关键时点/事件加竖线注释。

## 6. 配色选择
- 分组 Okabe-Ito + 线型冗余（[[色盲友好与打印友好原则]]）。
- 个体轨迹用浅灰，均值用强调色，避免喧宾夺主。
- 医学分组 [[医学二分类配色]]。

## 7. R 实现方案

### 7.1 推荐包
ggplot2、ggrepel（末端标注）

### 7.2 关键参数
`geom_line(aes(group=id))`、`stat_summary(fun=mean, geom="line")` + `stat_summary(fun.data=mean_cl_normal, geom="ribbon")`、`scale_x_continuous(breaks=)`。

### 7.3 基础代码模板（均值±CI 趋势带）
```r
ggplot(df, aes(PERIOD, BMI, color = sex, fill = sex)) +
  stat_summary(fun.data = mean_cl_normal, geom = "ribbon", alpha = .2, color = NA) +
  stat_summary(fun = mean, geom = "line", linewidth = 1) +
  stat_summary(fun = mean, geom = "point") +
  scale_color_manual(values = c("#0072B2","#D55E00")) +
  scale_fill_manual(values = c("#0072B2","#D55E00")) +
  scale_x_continuous(breaks = 1:3, labels = c("Exam 1","Exam 2","Exam 3")) +
  labs(x = NULL, y = "Mean BMI (kg/m²)", color = "Sex", fill = "Sex") +
  theme_pub()
```

### 7.4 发表级代码模板（个体轨迹 spaghetti + 组均值）
```r
ggplot(df, aes(PERIOD, BMI, group = RANDID)) +
  geom_line(alpha = .06, color = "grey40") +                      # 个体轨迹（淡）
  stat_summary(aes(group = sex, color = sex), fun = mean,
               geom = "line", linewidth = 1.2) +                  # 组均值（强调）
  scale_color_manual(values = c("#0072B2","#D55E00")) +
  scale_x_continuous(breaks = 1:3) +
  labs(x = "Exam period", y = "BMI (kg/m²)", color = "Sex") +
  theme_pub()
```

## 8. Python 实现方案

### 8.1 推荐包
matplotlib、seaborn

### 8.2 关键参数
`sns.lineplot(estimator="mean", errorbar=("ci",95), hue=, units=id, estimator=None)`；个体轨迹用 `units=` + `estimator=None`。

### 8.3 基础代码模板（均值±CI）
```python
fig, ax = plt.subplots(figsize=(4, 3))
sns.lineplot(data=df, x="PERIOD", y="BMI", hue="sex",
             errorbar=("ci", 95), marker="o",
             palette={"0":"#0072B2","1":"#D55E00"}, ax=ax)
ax.set_xticks([1,2,3]); ax.set_xticklabels(["Exam 1","Exam 2","Exam 3"])
ax.set_xlabel(None); ax.set_ylabel("Mean BMI (kg/m²)")
```

### 8.4 发表级代码模板（spaghetti + 均值）
```python
fig, ax = plt.subplots(figsize=(4, 3))
sns.lineplot(data=df, x="PERIOD", y="BMI", units="RANDID",     # 个体轨迹
             estimator=None, lw=.4, alpha=.06, color="grey", ax=ax)
sns.lineplot(data=df, x="PERIOD", y="BMI", hue="sex", estimator="mean",
             errorbar=None, lw=2, palette={"0":"#0072B2","1":"#D55E00"}, ax=ax)
ax.set_xticks([1,2,3]); ax.set_ylabel("BMI (kg/m²)")
```

## 9. 示例图像

### 9.1 网络优秀示例
见 [[Line_优秀示例]]（含 spaghetti + 均值范式、趋势带）。
本库自制范式图（合成数据，均值±95%CI 带）：

![[demo_line.png]]

### 9.2 Framingham 数据测试示例
✅ 已跑通（BMI 随 PERIOD 的均值±95%CI 趋势，分性别；数据天然长格式 3 期）。代码见 [[R测试记录]] / [[Python测试记录]]。

R（ggplot2 stat_summary 均值+ribbon）：

![[fig_line_bmi_period_r.png]]

Python（seaborn lineplot errorbar=ci）：

![[fig_line_bmi_period_py.png]]

> 结论：两性别 BMI 随随访期均略升，CI 带随后期样本减少而变宽。Exam 2/3 样本递减（3777/3176），解读末期需谨慎。

## 10. 常见错误
- 连接无序分类，暗示假连续性。
- 线太多无法分辨。
- 个体轨迹太密遮盖均值。
- 缺不确定性（只画均值线，无 CI）。
- 时间轴标签不清（PERIOD 没说明是访视期）。

## 11. 自动返修规则
- 线 > ~8 → 高亮重点 + 灰化其余 / 分面 / 直接标注末端。
- 个体轨迹密 → 降 alpha、抽样、或只画均值±CI。
- 缺不确定性 → 加 CI 带（`mean_cl_normal` / `errorbar="ci"`）。
- 末端拥挤 → 直接标注组名替代图例。
- 时点少（=2）→ 改斜率图/点估计。

## 12. 与其他图表的关系
- vs 斜率图：两时点强调变化方向 → slope chart。
- vs [[点估计置信区间图_PointRange]]：离散时点的均值±CI，可点估计呈现。
- vs 面积图：强调累积/占比 → area。
- spaghetti 是 line plot 的“个体版”。

## 13. 质量检查清单
- [ ] x 是有序/连续（不是无序分类被连线）？
- [ ] 有不确定性表达（CI 带）？
- [ ] 线数量可辨？
- [ ] 时间轴标签清楚？
- [ ] 颜色/线型色盲友好？
- [ ] 适合论文导出？

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建立初稿 | 缺实测图 | 跑 BMI~PERIOD 趋势，数据天然适配 |

相关：[[点估计置信区间图_PointRange]] · [[散点图_Scatter]] · [[医学二分类配色]] · [[图例设计]] · [[seaborn统计图模板]]
