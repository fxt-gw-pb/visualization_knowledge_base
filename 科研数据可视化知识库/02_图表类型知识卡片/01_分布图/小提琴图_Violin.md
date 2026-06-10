---
chart_name: 小提琴图
chart_name_en: Violin plot
chart_family: 分布图
data_type:
  - continuous
  - categorical_group
recommended_backend:
  r: ggplot2
  python: seaborn
difficulty: basic
priority: high
status: tested
tags:
  - dataviz
  - chart
  - violin
  - distribution
  - r
  - python
---

# 小提琴图 Violin plot

> 用核密度估计（KDE）展示**连续变量的完整分布形态**，比箱线图多了“形状”信息（双峰、偏态一眼可见）。

## 1. 图表定位

回答“**这组连续变量长什么形状，组间形状差异如何**”。在箱线五数概括之外，补上密度形态。

## 2. 适用场景

- 想看分布形态：是否双峰/多峰、是否偏态、尾部如何。
- 组间比较且每组样本量较大（KDE 才稳）。
- violin + 内嵌 box/quartile，一图兼顾形态与五数。

## 3. 不适用场景

- 样本量小 → KDE 不可靠，宽度具误导性（退回 box + jitter，见 [[箱线图_Boxplot]]）。
- 离散/计数少量取值 → 密度平滑失真。
- 只需中位数/IQR 比较 → 箱线更简洁。
- 受众不熟悉 violin → 可能误读宽度为频数绝对量。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 必需 |
|---|---|---|---|
| group | categorical | 分组（x）| 必需 |
| value | continuous | 连续变量（y）| 必需 |
| subgroup | categorical | 分面/split | 可选 |

## 5. 图表架构选择

### 5.1 基础架构
- x 分组，y 连续；几何 = violin。
- `scale` 参数定宽度含义：`"area"`(等面积)/`"width"`(等宽)/`"count"`(宽度∝n)。

### 5.2 高质量架构
- violin + 内嵌 box（`inner="box"`）或 quartile 线。
- violin + jitter/sina 点（点叠在密度上 = sina plot）。
- 两组对比可用 **split violin**（左右半边各一组）。
- 样本不大但想要形态 → 直接用 [[雨云图_Raincloud]]（半 violin 更诚实）。

## 6. 配色选择

### 6.1 默认配色
Okabe-Ito 分类（[[分类变量配色]]）；填充半透明，描边深色。

### 6.2 色盲友好配色
同箱线；split violin 两半用红/蓝（[[色盲友好与打印友好原则]]）。

### 6.3 医学研究推荐配色
病例/对照 [[医学二分类配色]]。

## 7. R 实现方案

### 7.1 推荐包
ggplot2、ggpubr、ggdist、ggbeeswarm、see（split violin）

### 7.2 关键参数
`geom_violin(trim=, scale=, bw=)`、内嵌 `geom_boxplot(width=.1)`、`geom_quasirandom()`。`trim=FALSE` 保留尾部，`scale="width"` 等宽便于形态对比。

### 7.3 基础代码模板
```r
ggplot(df, aes(grp, value, fill = grp)) +
  geom_violin(trim = FALSE, scale = "width", alpha = .8) +
  scale_fill_manual(values = okabe_ito) +
  labs(x = NULL, y = "BMI (kg/m²)") +
  theme_pub() + theme(legend.position = "none")
```

### 7.4 发表级代码模板
```r
ggplot(df, aes(grp, value, fill = grp)) +
  geom_violin(trim = FALSE, scale = "width", alpha = .75, color = NA) +
  geom_boxplot(width = .12, outlier.shape = NA, fill = "white") +   # 内嵌箱
  geom_quasirandom(size = .6, alpha = .35, color = "grey25") +       # sina 点
  scale_fill_manual(values = c(No = "#0072B2", Yes = "#D55E00")) +
  labs(x = NULL, y = "BMI (kg/m²)") +
  theme_pub() + theme(legend.position = "none")
```

## 8. Python 实现方案

### 8.1 推荐包
seaborn、matplotlib、plotnine

### 8.2 关键参数
`sns.violinplot(inner="box"/"quartile", cut=0, bw_adjust=, split=True, density_norm="width")`、叠点用 `stripplot`。`cut=0` 不外推到数据范围外。

### 8.3 基础代码模板
```python
fig, ax = plt.subplots(figsize=(3.5, 3))
sns.violinplot(data=df, x="grp", y="BMI", palette=okabe,
               inner="box", cut=0, ax=ax)
ax.set_xlabel(None); ax.set_ylabel("BMI (kg/m²)")
```

### 8.4 发表级代码模板
```python
fig, ax = plt.subplots(figsize=(3.5, 3))
sns.violinplot(data=df, x="grp", y="BMI", hue="sex", split=True,   # split violin
               palette={"0":"#0072B2","1":"#D55E00"}, cut=0,
               inner="quartile", density_norm="width", ax=ax)
sns.stripplot(data=df, x="grp", y="BMI", color="#333", size=2, alpha=.3, ax=ax)
ax.set_ylabel("BMI (kg/m²)"); ax.set_xlabel(None)
```

## 9. 示例图像

### 9.1 网络优秀示例
见 [[Raincloud_优秀示例]]（含 violin/sina/raincloud 对比）。
本库自制范式图（合成数据，C 组双峰可见）：

![[demo_violin.png]]

### 9.2 Framingham 数据测试示例
✅ 已跑通（按性别 × 吸烟状态看 TOTCHOL 分布形态；SEX 已确认 0=男/1=女）。代码见 [[R测试记录]] / [[Python测试记录]]。

R（ggplot2 violin + dodge box）：

![[fig_violin_sex_totchol_r.png]]

Python（seaborn split violin）：

![[fig_violin_sex_totchol_py.png]]

> 结论：一图对比 Male/Female × 吸烟两因素的胆固醇分布形态，n 足够支撑 KDE。Python 的 split violin 更紧凑；R 用 dodge 并列两半 violin 表达等价信息。

## 10. 常见错误
- 样本量小仍用 violin → 宽度误导。
- 不标内嵌箱/中位数 → 丢失数值参考。
- `scale="count"` 时读者误以为是绝对频数。
- 尾部外推超出数据范围（没设 `trim`/`cut`）。
- 颜色过多。

## 11. 自动返修规则
- 每组 n < ~30 → 退回 box + jitter（[[箱线图_Boxplot]]）。
- 尾部失真 → `trim=FALSE`→TRUE 或 `cut=0` 限制范围。
- 想要绝对可比 → `scale="width"` 等宽。
- 元素拥挤 → 改半 violin（[[雨云图_Raincloud]]）。
- 形态需配数值 → 内嵌 box 或标中位数。

## 12. 与其他图表的关系
- vs [[箱线图_Boxplot]]：violin 给形态，box 给五数；二者常合体。
- vs [[雨云图_Raincloud]]：雨云= 半 violin + box + 点，避免对称 violin 的“镜像幻觉”。
- vs 密度图：violin 是“竖起来按组排列的密度”。

## 13. 质量检查清单
- [ ] 样本量足以支撑 KDE？
- [ ] 有中位数/箱参考？
- [ ] 宽度含义（area/width/count）明确？
- [ ] 颜色色盲友好？
- [ ] 轴有单位？
- [ ] 适合论文导出？

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建立初稿 | 缺实测图 | 跑 PREVHYP×BMI，升 tested |

相关：[[箱线图_Boxplot]] · [[雨云图_Raincloud]] · [[分类变量配色]] · [[seaborn统计图模板]] · [[ggplot2参数系统]]
