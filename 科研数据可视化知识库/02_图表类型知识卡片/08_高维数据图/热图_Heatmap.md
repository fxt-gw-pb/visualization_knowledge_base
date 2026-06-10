---
chart_name: 热图
chart_name_en: Heatmap
chart_family: 高维数据图
data_type:
  - matrix
  - continuous
recommended_backend:
  r: ComplexHeatmap/pheatmap
  python: seaborn
difficulty: intermediate
priority: high
status: tested
tags:
  - dataviz
  - chart
  - heatmap
  - matrix
  - r
  - python
---

# 热图 Heatmap

> 用颜色编码矩阵每个格子的数值，配聚类与注释，看高维数据的模式/聚团/相关。涵盖：聚类热图、注释热图、相关矩阵热图、混淆矩阵热图。

## 1. 图表定位

回答“**一个矩阵里哪里高哪里低、行列怎么聚团、与分组注释如何对应**”。把高维表格变成可一眼扫描的颜色块。

## 2. 适用场景

- 表达矩阵/指标矩阵（样本×特征）的模式与聚类。
- 相关矩阵（变量两两相关，−1~1，发散色）。
- 混淆矩阵（分类结果）。
- 临床/组学注释热图（顶部/侧边注释条 + 聚类）。

## 3. 不适用场景

- 只有两个连续变量 → [[散点图_Scatter]]。
- 行列极多且无聚类结构 → 一片噪点（先降维/筛 top features）。
- 精确读数需求高 → 热图读数不精确，配数值标注或换表。
- 类别少的占比 → 柱状/堆叠。

## 4. 数据结构要求

| 输入 | 形态 | 说明 |
|---|---|---|
| 数值矩阵 | 行×列 | 表达量/指标；常按行 z-score 标准化 |
| 行/列注释 | 向量/表 | 分组、临床变量（注释条）|
| 相关矩阵 | 方阵 | `cor()`，中心 0 用发散色 |

## 5. 图表架构选择

### 5.1 基础架构
- 行 × 列网格，颜色 = 值；
- 可选行/列聚类树（dendrogram）；
- 颜色映射：连续用 viridis（[[连续变量配色]]）；有正负（z-score/相关/logFC）用发散 RdBu 中心 0（[[发散变量配色]]）。

### 5.2 高质量架构（ComplexHeatmap）
- 多层行/列注释条（分组、临床变量）。
- 按变量/ k-means 拆块（split）。
- 离群值截断/分位映射，避免色阶被拉爆。
- 标签过密 → 只标 top features / 隐藏部分。

## 6. 配色选择
- 连续单向：viridis（[[连续变量配色]]）。
- z-score/相关/logFC：发散 RdBu 或 Crameri vik，**中心对 0**（[[发散变量配色]]）。
- 注释条分类色：Okabe-Ito / 医学二分类（[[医学二分类配色]]）。
- 混淆矩阵：单色顺序（Blues）+ 数值标注。

## 7. R 实现方案

### 7.1 推荐包
ComplexHeatmap（复杂注释）、pheatmap（快速）、circlize（colorRamp2）、corrplot（相关）

### 7.2 关键参数
见 [[ComplexHeatmap模板]]：`Heatmap(col=colorRamp2(...), top_annotation=, column_split=, row_km=, clustering_method=)`；pheatmap `scale="row"`。

### 7.3 基础代码模板（相关矩阵）
```r
num <- df[, c("TOTCHOL","BMI","GLUCOSE","TIMEDTH")]
M <- cor(num, use = "pairwise.complete.obs")
pheatmap::pheatmap(M, display_numbers = TRUE,
                   color = colorRampPalette(c("#2166AC","white","#B2182B"))(100),
                   breaks = seq(-1, 1, length.out = 101))   # 中心 0
```

### 7.4 发表级代码模板（注释聚类热图）
见 [[ComplexHeatmap模板]] 第 2 节（z-score + 注释条 + 拆块 + 截断）。

## 8. Python 实现方案

### 8.1 推荐包
seaborn（`heatmap`/`clustermap`）、matplotlib

### 8.2 关键参数
`sns.heatmap(cmap=, center=0, vmin=, vmax=, annot=)`、`sns.clustermap(z_score=0/1, method=, col_colors=)`。

### 8.3 基础代码模板（相关矩阵）
```python
num = df[["TOTCHOL","BMI","GLUCOSE","TIMEDTH"]]
corr = num.corr()
fig, ax = plt.subplots(figsize=(3.5,3))
sns.heatmap(corr, cmap="RdBu_r", center=0, vmin=-1, vmax=1,
            annot=True, fmt=".2f", square=True, ax=ax)
```

### 8.4 发表级代码模板（聚类 + 注释 + 截断）
```python
mat = (df_feat - df_feat.mean()) / df_feat.std()      # 行/列 z-score
mat = mat.clip(-3, 3)                                  # 截断离群，防色阶拉爆
col_colors = df["grp"].map({"case":"#D55E00","control":"#0072B2"})
g = sns.clustermap(mat, cmap="RdBu_r", center=0, vmin=-3, vmax=3,
                   method="ward", col_colors=col_colors,
                   xticklabels=False, figsize=(6,7))
```

## 9. 示例图像

### 9.1 网络优秀示例
见 [[Heatmap_优秀示例]]（含 ComplexHeatmap 注释范式、相关矩阵热图）。
本库自制范式图（合成数据，发散色中心 0 + 数值标注）：

![[demo_heatmap.png]]

### 9.2 Framingham 数据测试示例
✅ 已跑通（TOTCHOL/BMI/GLUCOSE/TIMEDTH 相关矩阵热图，发散色中心 0）。代码见 [[R测试记录]] / [[Python测试记录]]。

R（pheatmap）：

![[fig_heatmap_corr_r.png]]

Python（seaborn heatmap）：

![[fig_heatmap_corr_py.png]]

> 结论：变量间相关均较弱；TIMEDTH 与各指标弱负相关。仅 4 个变量，矩阵小、未聚类直接标数值。两后端一致。

## 10. 常见错误
- 不标准化 → 单一量纲大的特征吃掉整个色阶。
- 离群值把色阶拉爆，主体一片同色。
- 发散数据中心不在 0。
- 行列标签过密无法读。
- 用 rainbow 连续色。
- 聚类方法/距离不说明。

## 11. 自动返修规则
- 色阶被离群值拉爆 → 截断（clip）/分位映射/z-score。
- 标签过密 → 聚类 + 只标 top features / 隐藏部分。
- 发散数据 → 强制 center=0 + 对称范围。
- 无结构噪点 → 先筛 top variable features / 降维。
- 连续色是 rainbow → 换 viridis；有正负换 RdBu。

## 12. 与其他图表的关系
- vs 相关散点矩阵（pairplot）：热图压缩为颜色，pairplot 显示散点细节。
- vs [[散点图_Scatter]]：两变量关系用散点，多变量相关用热图矩阵。
- 混淆矩阵热图属 [[ROC曲线_ROC]] 同族评价图。
- 与 PCA/UMAP（降维）配合看高维结构。

## 13. 质量检查清单
- [ ] 是否需要/已做标准化？
- [ ] 离群值是否截断？
- [ ] 发散数据中心对 0？
- [ ] 标签可读（或合理隐藏）？
- [ ] 颜色色盲友好（非 rainbow）？
- [ ] 聚类方法注明？
- [ ] 适合论文导出？

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建立初稿 | 缺实测图 | 跑相关矩阵 + 注释聚类热图 |

相关：[[散点图_Scatter]] · [[ROC曲线_ROC]] · [[连续变量配色]] · [[发散变量配色]] · [[ComplexHeatmap模板]] · [[医学二分类配色]]
