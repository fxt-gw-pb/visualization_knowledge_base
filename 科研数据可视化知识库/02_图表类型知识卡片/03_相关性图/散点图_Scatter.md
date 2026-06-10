---
chart_name: 散点图
chart_name_en: Scatter plot
chart_family: 相关性图
data_type:
  - continuous
  - continuous
recommended_backend:
  r: ggplot2
  python: seaborn/matplotlib
difficulty: basic
priority: high
status: tested
tags:
  - dataviz
  - chart
  - scatter
  - correlation
  - r
  - python
---

# 散点图 Scatter plot

> 两个连续变量的关系图。科研里看相关、趋势、聚集、离群的第一选择。可叠回归线/LOESS + CI 表达趋势。

## 1. 图表定位

回答“**两个连续变量怎么联动**”：正/负相关、线性/非线性、强弱、离群点、亚群结构。

## 2. 适用场景

- 两连续变量关系（sysBP vs diaBP、BMI vs TOTCHOL）。
- 加回归/LOESS 看趋势与拟合。
- 用第三维（颜色/大小/形状）编码分组或连续量（→ 气泡图）。
- 看离群点、聚集、非线性。

## 3. 不适用场景

- 点极多严重重叠（overplotting）→ 改 hexbin / 2D 密度 / 抽样。
- 一个轴是分类 → 用 [[箱线图_Boxplot]] / strip / [[点估计置信区间图_PointRange]]。
- 想看单变量分布 → 直方/密度（分布族）。
- 想强调因果/时间顺序 → 时间用 [[折线趋势图_Line]]。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 必需 |
|---|---|---|---|
| x | continuous | 自变量 | 必需 |
| y | continuous | 因变量 | 必需 |
| color/group | categorical/continuous | 分组或第三维 | 可选 |
| size | continuous | 气泡大小（第四维）| 可选 |

## 5. 图表架构选择

### 5.1 基础架构
- x、y 连续；几何 = point。
- 可选：回归线（`lm`）或 LOESS + 置信带。

### 5.2 高质量架构
- 重叠多 → `alpha` + 边缘分布（marginal hist/density）或 hexbin。
- 分组 → 颜色 + 形状（色盲冗余）+ 每组拟合线。
- 想报相关 → 标注 r/ρ 与 p（[[标签与注释设计]]）。
- 第三连续维 → 颜色 viridis；第四维 → 点大小（→ 气泡图）。

参见 [[坐标轴设计]]（轴不必从 0、带单位）。

## 6. 配色选择
- 分组：Okabe-Ito（[[分类变量配色]]）+ 形状冗余。
- 连续第三维：viridis（[[连续变量配色]]），colorbar 带单位。
- 医学分组：[[医学二分类配色]]。

## 7. R 实现方案

### 7.1 推荐包
ggplot2、ggpubr、ggExtra（边缘分布）、hexbin

### 7.2 关键参数
`geom_point(alpha=, size=, shape=)`、`geom_smooth(method="lm"/"loess", se=TRUE)`、`ggpubr::stat_cor()`、`ggExtra::ggMarginal()`、`geom_hex()`。

### 7.3 基础代码模板
```r
ggplot(df, aes(sysBP, diaBP)) +
  geom_point(alpha = .4, size = 1, color = "#0072B2") +
  geom_smooth(method = "lm", se = TRUE, color = "#D55E00") +
  labs(x = "Systolic BP (mmHg)", y = "Diastolic BP (mmHg)") +
  theme_pub()
```

### 7.4 发表级代码模板
```r
library(ggpubr); library(ggExtra)
p <- ggplot(df, aes(sysBP, diaBP, color = sex)) +
  geom_point(alpha = .35, size = .9) +
  geom_smooth(method = "lm", se = TRUE) +
  stat_cor(method = "pearson", label.x.npc = "left") +     # 标 r 与 p
  scale_color_manual(values = c("#0072B2","#D55E00")) +
  labs(x = "Systolic BP (mmHg)", y = "Diastolic BP (mmHg)", color = "Sex") +
  theme_pub()
ggMarginal(p, type = "density", groupColour = TRUE)        # 边缘密度
```

## 8. Python 实现方案

### 8.1 推荐包
seaborn、matplotlib、（hexbin 内置）

### 8.2 关键参数
`sns.scatterplot(alpha=, size=, hue=, style=)`、`sns.regplot/lmplot(order=, lowess=, ci=)`、`sns.jointplot(kind="scatter"/"hex"/"kde")`、`ax.hexbin()`。

### 8.3 基础代码模板
```python
fig, ax = plt.subplots(figsize=(3.5, 3.2))
sns.regplot(data=df, x="sysBP", y="diaBP",
            scatter_kws=dict(alpha=.35, s=10, color="#0072B2"),
            line_kws=dict(color="#D55E00"), ax=ax)
ax.set_xlabel("Systolic BP (mmHg)"); ax.set_ylabel("Diastolic BP (mmHg)")
```

### 8.4 发表级代码模板
```python
g = sns.jointplot(data=df, x="sysBP", y="diaBP", hue="sex",
                  palette={"0":"#0072B2","1":"#D55E00"},
                  alpha=.35, height=3.6, marginal_kws=dict(fill=True))
g.plot_joint(sns.regplot, scatter=False)        # 叠回归
from scipy.stats import pearsonr
r,p = pearsonr(df.sysBP, df.diaBP)
g.ax_joint.text(.05,.95, f"r={r:.2f}, p={p:.1e}", transform=g.ax_joint.transAxes, va="top")
# 重叠太多改 hexbin： sns.jointplot(..., kind="hex")
```

## 9. 示例图像

### 9.1 网络优秀示例
见 [[Scatter_优秀示例]]（含带边缘分布的散点、hexbin 范式）。
本库自制范式图（合成数据，散点+回归+r）：

![[demo_scatter.png]]

### 9.2 Framingham 数据测试示例
✅ 已跑通（BMI vs TOTCHOL + 回归 + Pearson r）。代码见 [[R测试记录]] / [[Python测试记录]]。
> 注意：本数据含 TOTCHOL/BMI/GLUCOSE，**不含 sysBP/diaBP**（经典教学版才有），故选 BMI×TOTCHOL，见 [[变量字典]]。

R（ggpubr ggscatter + stat_cor）：

![[fig_scatter_bmi_totchol_r.png]]

Python（seaborn regplot）：

![[fig_scatter_bmi_totchol_py.png]]

> 结论：BMI 与总胆固醇弱正相关（r≈0.13）。n=4000+ 点重叠严重，已用 alpha≈0.12 降透明度；若仍糊可改 hexbin。

## 10. 常见错误
- overplotting 不处理 → 一团黑。
- 把分类变量当 x（应改箱线/strip）。
- 轴缺单位。
- 回归线外推超数据范围。
- 报了相关却没说方法（Pearson/Spearman）与 p。

## 11. 自动返修规则
- 点重叠严重 → alpha↓ / jitter / hexbin / 2D 密度 / 抽样。
- 想表达趋势 → 加 lm/LOESS + CI 带。
- 非线性 → LOESS 或变换（log）。
- 分组难分 → 颜色 + 形状 + 每组拟合。
- 边缘分布有信息 → 加 marginal hist/density。

## 12. 与其他图表的关系
- vs 气泡图：散点加“大小”第四维 = 气泡图。
- vs 相关热图：多对变量的相关用 [[热图_Heatmap]] 相关矩阵。
- vs [[折线趋势图_Line]]：x 是时间且有序 → 折线。
- vs 成对图（pairplot）：多变量两两散点矩阵。

## 13. 质量检查清单
- [ ] overplotting 已处理？
- [ ] 趋势/相关表达清楚（线 + r/p + 方法）？
- [ ] 轴有单位？
- [ ] 颜色/形状色盲友好？
- [ ] 回归未不当外推？
- [ ] 适合论文导出？

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建立初稿 | 真实数据无 sysBP/diaBP，需选 BMI×TOTCHOL 等 | 跑 BMI×TOTCHOL，升 tested |

相关：[[热图_Heatmap]] · [[折线趋势图_Line]] · [[连续变量配色]] · [[分类变量配色]] · [[seaborn统计图模板]]
