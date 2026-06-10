---
chart_name: 雨云图
chart_name_en: Raincloud plot
chart_family: 分布图
data_type:
  - continuous
  - categorical_group
recommended_backend:
  r: ggdist + ggplot2
  python: matplotlib/ptitprince
difficulty: intermediate
priority: high
status: tested
tags:
  - dataviz
  - chart
  - raincloud
  - distribution
  - r
  - python
---

# 雨云图 Raincloud plot

> “半小提琴（云）+ 箱线（伞）+ 原始抖动点（雨）”三合一。当前最被推荐的分布比较图：既显形态、又显概括、又显原始数据，且避免对称 violin 的镜像冗余。

## 1. 图表定位

回答“**组间连续变量分布的形态、概括统计、以及每一个原始观测**”——一张图把分布信息几乎说全。

## 2. 适用场景

- 论文/汇报想一图说清分布 + 概括 + 原始点。
- 中小样本（点不太多时尤其漂亮）。
- 需要透明展示数据（避免 box/violin 隐藏个体）。
- 组数适中（2–6）。

## 3. 不适用场景

- 点极多（上万）→ 雨点糊成一片（抽样或换 [[小提琴图_Violin]]）。
- 组数极多 → 拥挤（分面或精选）。
- 受众完全不熟 → 需图注解释三部分。
- 版面极小 → 元素多，需要足够空间。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 必需 |
|---|---|---|---|
| group | categorical | 分组 | 必需 |
| value | continuous | 连续变量 | 必需 |
| subgroup | categorical | 分面 | 可选 |

## 5. 图表架构选择

### 5.1 基础架构（横向最常见）
- 半小提琴（density）在一侧；
- 箱线在中间；
- 抖动原始点在另一侧；
- 通常 `coord_flip` 横向，组沿 y 排列。

### 5.2 高质量架构
- 用 ggdist `stat_halfeye`（云）+ `stat_dots`（点）或 `geom_boxplot`。
- 点用 beeswarm/sina 减少重叠。
- 偏移量调好，三部分不打架。

## 6. 配色选择
- 分类 Okabe-Ito（[[分类变量配色]]）；云半透明、点更透明、箱描边深。
- 医学二分类 [[医学二分类配色]]。
- 色盲友好 + 形状冗余（[[色盲友好与打印友好原则]]）。

## 7. R 实现方案

### 7.1 推荐包
ggdist、ggplot2、gghalves、ggbeeswarm

### 7.2 关键参数
`stat_halfeye(adjust=, width=, justification=, .width=)`、`stat_dots(side=, dotsize=)`、`geom_boxplot(width=.12)`、偏移 `position_nudge`。

### 7.3 基础/发表级代码模板
```r
library(ggdist); library(ggplot2)
ggplot(df, aes(grp, value, fill = grp)) +
  stat_halfeye(adjust = .6, width = .6, justification = -.2,
               .width = 0, point_colour = NA) +              # 云
  geom_boxplot(width = .12, outlier.shape = NA, alpha = .6) + # 伞
  stat_dots(side = "left", justification = 1.1, dotsize = .4,
            binwidth = NA, color = "grey25") +                # 雨
  scale_fill_manual(values = okabe_ito) +
  coord_flip() +                                              # 横向
  labs(x = NULL, y = "BMI (kg/m²)") +
  theme_pub() + theme(legend.position = "none")
```

## 8. Python 实现方案

### 8.1 推荐包
matplotlib（手搓）、ptitprince（PtitPrince，raincloud 封装）、seaborn（half-violin 组合）

### 8.2 关键参数
ptitprince `pt.RainCloud(x, y, data, orient="h", bw=, width_viol=, point_size=)`；或手搓：half violin（`violinplot` 取一半）+ `boxplot` + `stripplot`。

### 8.3 代码模板
```python
# 方案 A：ptitprince（注意维护状态/seaborn 兼容，见 Python绘图资源索引）
import ptitprince as pt
fig, ax = plt.subplots(figsize=(4, 3.2))
pt.RainCloud(x="grp", y="BMI", data=df, palette=okabe,
             orient="h", width_viol=.6, point_size=2, ax=ax)
ax.set_xlabel("BMI (kg/m²)")
```
```python
# 方案 B：纯 matplotlib/seaborn 手搓（更可控、依赖少）
fig, ax = plt.subplots(figsize=(4, 3.2))
parts = ax.violinplot([g.BMI.values for _,g in df.groupby("grp")],
                      showextrema=False, vert=False)
for b in parts['bodies']:                          # 只留半边
    b.get_paths()[0].vertices[:,1] = np.clip(
        b.get_paths()[0].vertices[:,1], np.mean(b.get_paths()[0].vertices[:,1]), np.inf)
sns.boxplot(data=df, x="BMI", y="grp", width=.15, showfliers=False, ax=ax)
sns.stripplot(data=df, x="BMI", y="grp", size=2, alpha=.4, color="grey", ax=ax)
```

## 9. 示例图像

### 9.1 网络优秀示例
见 [[Raincloud_优秀示例]]（含 Allen et al. raincloud 原始范式、ggdist gallery）。
本库自制范式图（合成数据，云+箱+雨三层）：

![[demo_raincloud.png]]

### 9.2 Framingham 数据测试示例
✅ 已跑通（按 AGE_group 比较 BMI）。代码见 [[R测试记录]] / [[Python测试记录]]。

R（ggdist：stat_halfeye + boxplot + quasirandom）：

![[fig_raincloud_age_bmi_r.png]]

Python（matplotlib 手搓 半KDE + box + 雨点）：

![[fig_raincloud_age_bmi_py.png]]

> 结论：三个年龄组 BMI 分布形态相近、中位数随年龄略升。R 的 ggdist 路径最简洁；Python 手搓可控但代码更长。

## 10. 常见错误
- 点太多糊成一片（不抽样）。
- 三部分偏移没调好，互相重叠。
- 横向时轴标签/方向混乱。
- 用对称 violin 替代半 violin（镜像冗余）。
- 颜色过多。

## 11. 自动返修规则
- 点 > ~500/组 → 抽样或降 alpha 或改 sina。
- 元素重叠 → 加大 `justification`/`position_nudge` 偏移。
- 组多 → 分面或横向 + 排序。
- 受众不熟 → 图注标注云/箱/雨三部分含义。
- 偏态强 → 半 violin 已能显示，无需 log；必要时 log 轴并标注。

## 12. 与其他图表的关系
- vs [[小提琴图_Violin]]：雨云用半 violin，避免对称镜像，且强制显示原始点。
- vs [[箱线图_Boxplot]]：雨云 = 箱线 + 形态 + 原始点的超集。
- vs 蜂群图：雨云包含点层，可用 beeswarm 实现“雨”。

## 13. 质量检查清单
- [ ] 云/箱/雨三部分清晰不打架？
- [ ] 点数量合适（不糊）？
- [ ] 颜色色盲友好？
- [ ] 轴有单位、方向清楚？
- [ ] 图注说明三部分？
- [ ] 适合论文导出？

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建立初稿 | 缺实测图；ptitprince 兼容性待验 | 跑 AGE_group×BMI，优先 R/ggdist 路径 |

相关：[[箱线图_Boxplot]] · [[小提琴图_Violin]] · [[分类变量配色]] · [[ggplot2参数系统]]
