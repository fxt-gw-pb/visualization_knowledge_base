---
chart_name: 密度图
chart_name_en: Density plot
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
  - density
  - kde
  - distribution
  - r
  - python
---

# 密度图 Density plot

> 用核密度估计（KDE）给连续变量一条**平滑的分布曲线**，比直方图更适合**多组分布叠加对比**。

## 1. 图表定位

回答“**这个连续变量的平滑分布形态是什么 / 几组之间分布怎么错开**”。不受分箱位置影响，曲线连续。

## 2. 适用场景

- 平滑展示单变量分布形态（峰、偏、尾）。
- **多组分布叠加对比**（2–4 组）——密度图比叠直方图清晰得多。
- 样本量中等以上；想强调形态而非精确计数。

## 3. 不适用场景

- 样本量很小 → KDE 过度平滑/出假峰，改直方/点 + rug。
- 组 > 4 叠一起 → 仍乱，改 [[山峦图_Ridgeline]]（纵向错开）。
- 需要精确频数 → [[直方图_Histogram]]。
- 边界有硬截断（如 ≥0 的浓度）→ KDE 会漏到负区，需设 `cut=0` 或边界校正。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| value | continuous | 连续变量 | 必需 |
| group | categorical | 分组（叠加/分面）| 多组对比时必需 |

## 5. 图表架构选择

### 5.1 基础架构
- x：连续变量；y：密度；曲线下面积=1（每组各自归一时用 `common_norm=False`）。

### 5.2 高质量架构
- 多组 → 半透明填充 + 描边；强调“各组形态”而非“各组占比”时按组归一。
- 带宽（bw / adjust）是关键：过小毛刺，过大糊形态。
- 可叠 rug 或与直方组合。
- 组多 → [[山峦图_Ridgeline]]。

## 6. 配色选择

### 6.1 默认配色
分类 `cat_main`（Okabe-Ito），填充降 alpha（~.35），见 [[分类变量配色]]。

### 6.2 色盲友好配色
Okabe-Ito / Set2；叠加用半透明，必要时加线型冗余。

### 6.3 医学研究推荐配色
病例/对照用 [[医学二分类配色]]（病例朱红、对照蓝）。

## 7. R 实现方案

### 7.1 推荐包
ggplot2

### 7.2 关键参数
`geom_density(alpha=, adjust=)`、`scale_fill_manual`、按组 `color`。

### 7.3 可执行模板
**`templates/r/density.R`**。核心：
```r
ggplot(df, aes(val, fill = grp, color = grp)) +
  geom_density(alpha = .35) +
  scale_fill_manual(values = pal("cat_main")) + scale_color_manual(values = pal("cat_main"))
```

## 8. Python 实现方案

### 8.1 推荐包
seaborn

### 8.2 关键参数
`sns.kdeplot(hue=, fill=True, alpha=, common_norm=False, bw_adjust=, cut=)`。

### 8.3 可执行模板
**`templates/python/density.py`**。核心：
```python
sns.kdeplot(data=df, x="val", hue="grp", fill=True, alpha=.35, common_norm=False, palette=palette, ax=ax)
```

## 9. 示例图像

### 9.1 网络优秀示例
参考 seaborn `kdeplot` / data-to-viz 的多组密度叠加范式。

### 9.2 本库模板 demo（合成数据，双后端对齐）
Python（seaborn）：

![[tpl_density_py.png]]

R（ggplot2）：

![[tpl_density_r.png]]

> 三组均值依次右移，密度曲线清晰错开；双后端一致。`common_norm=False` 保证各组曲线各自归一、形态可比。

## 10. 常见错误
- 带宽默认过平滑，掩盖双峰。
- 多组不归一（`common_norm=True`）导致小组被压扁、形态不可比。
- 有硬边界变量漏到不可能区间（未设 `cut=0`）。
- 组太多仍硬叠。

## 11. 自动返修规则
- 组 > 4 → 改 [[山峦图_Ridgeline]] 或分面。
- 出现可疑双峰 → 提示减小带宽核对，或叠直方。
- 边界变量（非负）→ 自动 `cut=0` / 边界校正。
- 各组样本量差异大 → 默认 `common_norm=False`。

## 12. 与其他图表的关系
- vs [[直方图_Histogram]]：直方=分箱计数，密度=平滑形态；常叠加。
- vs [[山峦图_Ridgeline]]：多组（>4）纵向错开更清楚。
- vs [[小提琴图_Violin]]：小提琴=密度的镜像 + 箱线，更适合按类别并排。

## 13. 质量检查清单
- [ ] 带宽合理，未过平滑/欠平滑？
- [ ] 多组是否各自归一、半透明可辨？
- [ ] 边界变量是否处理？
- [ ] 轴标签有单位？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建卡 + 双后端可执行模板 + demo 图，状态 tested | — | 可补 Framingham 分组实测 |

相关：[[直方图_Histogram]] · [[山峦图_Ridgeline]] · [[小提琴图_Violin]] · [[分类变量配色]]
