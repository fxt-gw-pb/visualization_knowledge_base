---
title: ComplexHeatmap 模板
type: code-template
status: active
backend: r
updated: 2026-06-10
tags:
  - dataviz
  - r
  - complexheatmap
  - pheatmap
  - heatmap
  - template
---

# ComplexHeatmap 模板

> R 端热图天花板。简单聚类热图用 pheatmap；多层注释/拆分/并排用 ComplexHeatmap。配合 [[热图_Heatmap]] 卡片。

## 1. pheatmap 快速版

```r
library(pheatmap)
mat <- scale(t(as.matrix(df_numeric)))   # 行 z-score（按特征标准化）
pheatmap(mat,
         color = colorRampPalette(c("#2166AC","white","#B2182B"))(100), # 发散 div_rdbu
         scale = "none",                  # 已手动 z-score
         clustering_distance_rows = "euclidean",
         clustering_method = "ward.D2",
         show_rownames = TRUE, show_colnames = FALSE,
         annotation_col = ann_df,         # 列注释（如 group）
         filename = "heatmap.pdf", width = 6, height = 8)
```

## 2. ComplexHeatmap 注释版

```r
library(ComplexHeatmap); library(circlize)

# 连续值色映射（中心 0，发散）
col_fun <- colorRamp2(c(-2, 0, 2), c("#2166AC", "white", "#B2182B"))  # >>> PARAM

# 顶部列注释（临床/分组）
top_ann <- HeatmapAnnotation(
  Group = ann$group, Sex = ann$sex,
  col = list(Group = c(case = "#D55E00", control = "#0072B2"),   # 医学二分类配色
             Sex   = c(`0` = "#0072B2", `1` = "#E69F00")),
  annotation_name_side = "left"
)

Heatmap(mat,
        name = "z-score",
        col = col_fun,
        top_annotation = top_ann,
        cluster_rows = TRUE, cluster_columns = TRUE,
        clustering_method_rows = "ward.D2",
        show_row_names = TRUE, row_names_gp = gpar(fontsize = 7),
        show_column_names = FALSE,
        column_split = ann$group,           # 按组拆列块
        row_km = 3,                          # 行 k-means 拆块
        heatmap_legend_param = list(title = "z-score"))
```

## 3. 关键参数（旋钮）

| 参数 | 作用 |
|---|---|
| `col` / `colorRamp2` | 连续→颜色映射；发散中心对 0（[[发散变量配色]]）|
| `cluster_rows/columns` | 是否聚类 |
| `clustering_method` | "ward.D2"/"complete"/"average" |
| `column_split` / `row_km` / `row_split` | 按变量或 k-means 拆块 |
| `top/left_annotation` | 多层注释条 |
| `show_row/column_names` | 标签过密时关掉（返修）|

## 4. 数据预处理要点

- 表达/指标矩阵常做 **z-score（按行/特征标准化）**，否则量纲大的特征吃掉色阶。
- 离群值截断：`mat[mat >  3] <-  3; mat[mat < -3] <- -3`（或分位映射），避免色阶被拉爆。
- 缺失值：先决定填补或 `na_col`。

## 5. 常见错误（→ 返修，见 [[热图_Heatmap]]）

- ❌ 不标准化导致单特征主导色阶 → z-score / 分位映射。
- ❌ 行/列标签过密 → 聚类 + 只标 top features / 隐藏部分。
- ❌ 发散色中心不在 0。
- ❌ 用 rainbow 连续色（改 viridis 或发散 RdBu）。

## 6. 导出

```r
pdf("heatmap.pdf", width = 6, height = 8); draw(ht); dev.off()
```
见 [[R导出规范]]。

相关：[[热图_Heatmap]] · [[发散变量配色]] · [[连续变量配色]] · [[R导出规范]]
