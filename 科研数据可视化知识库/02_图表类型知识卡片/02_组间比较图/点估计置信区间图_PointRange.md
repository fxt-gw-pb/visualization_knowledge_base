---
chart_name: 点估计置信区间图
chart_name_en: Point-range plot
chart_family: 组间比较图
data_type:
  - categorical_group
  - estimate_ci
recommended_backend:
  r: ggplot2
  python: matplotlib
difficulty: basic
priority: high
status: tested
tags:
  - dataviz
  - chart
  - pointrange
  - estimate
  - ci
  - r
  - python
---

# 点估计 + 置信区间图 Point-range plot

> 用“点（估计值）+ 线（CI/SE/SD）”表达各组的**集中趋势与不确定性**。是“柱状图 + 误差棒”的更诚实替代（不强制 y 从 0、不用面积误导）。

## 1. 图表定位

回答“**各组的均值（或其他估计量）是多少，置信区间多宽，组间是否分离**”。聚焦估计与不确定性，而非整组分布。

## 2. 适用场景

- 比较各组均值/比例/率及其 95% CI。
- 多模型/多亚组的效应估计并列。
- 想强调“估计 + 不确定性”而非全分布。
- 森林图的“非模型版”近亲（[[森林图_ForestPlot]]）。

## 3. 不适用场景

- 需要展示分布形态/离群 → [[箱线图_Boxplot]] / [[小提琴图_Violin]]。
- 样本量极小、估计极不稳 → 直接画原始点。
- 想表达长度/计数总量 → 柱状图（但注意别用误差棒柱状图代替分布）。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 必需 |
|---|---|---|---|
| group | categorical | 分组（y 或 x）| 必需 |
| estimate | continuous | 点估计（均值/比例/效应）| 必需 |
| conf.low / conf.high | continuous | CI 上下界 | 必需 |
| facet/model | categorical | 多模型/亚组 | 可选 |

可由原始数据 `stat_summary` 现算，或预先汇总成上表。

## 5. 图表架构选择

### 5.1 基础架构
- 类别轴（常横向，便于读长标签）+ 估计值轴；
- 几何 = pointrange（点 + 误差线）；
- 参考线：差值/效应类 = 0；比值类 = 1（log 轴）。

### 5.2 高质量架构
- 按估计值排序类别（便于阅读）。
- 多模型并列用 `position_dodge` 或分面。
- 明确标注误差度量（95% CI / SE / SD）（[[标签与注释设计]]）。
- 类别多 → 横向。

## 6. 配色选择
- 单组用单色；多模型/多组用 Okabe-Ito（[[分类变量配色]]）。
- 效应方向语义 → [[模型效应方向配色]]（有害红、保护蓝、无效灰）。
- 医学分组 [[医学二分类配色]]。

## 7. R 实现方案

### 7.1 推荐包
ggplot2、（Hmisc 提供 mean_cl_normal/boot）

### 7.2 关键参数
`stat_summary(fun.data=mean_cl_normal, geom="pointrange")` 或预算后 `geom_pointrange(aes(ymin=, ymax=))`；`coord_flip()`；`geom_hline/vline` 参考线；`position_dodge()`。

### 7.3 基础代码模板（从原始数据现算均值±CI）
```r
ggplot(df, aes(grp, BMI)) +
  stat_summary(fun.data = mean_cl_normal, geom = "pointrange",
               size = .5, color = "#0072B2") +
  labs(x = NULL, y = "Mean BMI (95% CI)") +
  coord_flip() +
  theme_pub()
```

### 7.4 发表级代码模板（预汇总 + 多组 + 排序）
```r
summ <- df |>
  dplyr::group_by(grp) |>
  dplyr::summarise(est = mean(BMI), se = sd(BMI)/sqrt(dplyr::n())) |>
  dplyr::mutate(lo = est - 1.96*se, hi = est + 1.96*se,
                grp = forcats::fct_reorder(grp, est))
ggplot(summ, aes(est, grp, color = grp)) +
  geom_pointrange(aes(xmin = lo, xmax = hi), size = .5) +
  scale_color_manual(values = okabe_ito) +
  labs(x = "Mean BMI (95% CI)", y = NULL) +
  theme_pub() + theme(legend.position = "none")
```

## 8. Python 实现方案

### 8.1 推荐包
matplotlib、seaborn（`pointplot`）

### 8.2 关键参数
`sns.pointplot(errorbar=("ci",95), join=False, capsize=)`，或 `ax.errorbar(x, y, xerr=, fmt="o")` 手控。

### 8.3 基础代码模板
```python
fig, ax = plt.subplots(figsize=(3.5, 3))
sns.pointplot(data=df, x="BMI", y="grp", errorbar=("ci",95),
              linestyle="none", color="#0072B2", capsize=.2, ax=ax)
ax.set_xlabel("Mean BMI (95% CI)"); ax.set_ylabel(None)
```

### 8.4 发表级代码模板（预汇总 + 排序 + 参考线）
```python
g = (df.groupby("grp")["BMI"].agg(["mean","sem"]).reset_index())
g["lo"] = g["mean"] - 1.96*g["sem"]; g["hi"] = g["mean"] + 1.96*g["sem"]
g = g.sort_values("mean")
fig, ax = plt.subplots(figsize=(3.5, 3))
ax.errorbar(g["mean"], range(len(g)), xerr=[g["mean"]-g["lo"], g["hi"]-g["mean"]],
            fmt="o", color="#0072B2", capsize=3)
ax.set_yticks(range(len(g))); ax.set_yticklabels(g["grp"])
ax.set_xlabel("Mean BMI (95% CI)")
```

## 9. 示例图像

### 9.1 网络优秀示例
见 [[PointRange_优秀示例]]（含 dot-and-whisker 系数图范式）。
本库自制范式图（合成数据，按效应排序 + 方向着色 + 参考线 0）：

![[demo_pointrange.png]]

### 9.2 Framingham 数据测试示例
✅ 已跑通（各 AGE_group 的 BMI 均值±95%CI，标注各组 n）。代码见 [[Python测试记录]]。

R（ggplot2 geom_pointrange + n 标注）：

![[fig_pointrange_age_bmi_r.png]]

Python（matplotlib errorbar）：

![[fig_pointrange_age_bmi_py.png]]

> 结论：BMI 均值随年龄组上升，组 3 因 n 小（108）CI 最宽——point-range 诚实展示了这一不确定性，比柱状±SD 更合适。R 与 Python 一致。

## 10. 常见错误
- 误差棒不说明是 CI/SE/SD（[[术语表]]）。
- 比值类用线性轴（应 log + 参考线 1）。
- 类别不排序，难读。
- 用柱状图 + 误差棒代替（应优先 point-range）。
- 缺参考线。

## 11. 自动返修规则
- 类别多 → 横向 + 按估计值排序。
- 多模型重叠 → `position_dodge` 或分面。
- 比值类 → log 轴 + 参考线 1。
- 误差含义不明 → 图注/标题注明（95% CI 等）。
- CI 极宽个别项压缩主体 → 截断轴并标注。

## 12. 与其他图表的关系
- vs [[森林图_ForestPlot]]：森林图 = 模型效应（OR/HR）的 point-range + 左表。
- vs [[箱线图_Boxplot]]：箱线给分布，point-range 给估计+不确定性。
- vs 柱状图 + 误差棒：point-range 更诚实（不靠面积、不强制 0）。

## 13. 质量检查清单
- [ ] 误差度量已注明？
- [ ] 有参考线（0 或 1）？
- [ ] 类别排序合理？
- [ ] 比值类用 log？
- [ ] 颜色/方向语义正确？
- [ ] 适合论文导出？

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建立初稿 | 缺实测图 | 跑 AGE_group×BMI 均值±CI |

相关：[[森林图_ForestPlot]] · [[箱线图_Boxplot]] · [[折线趋势图_Line]] · [[模型效应方向配色]] · [[标签与注释设计]]
