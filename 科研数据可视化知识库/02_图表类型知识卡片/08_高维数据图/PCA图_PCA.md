---
chart_name: PCA 图
chart_name_en: PCA plot
chart_family: 高维数据图
data_type:
  - high_dimensional
  - categorical_group
recommended_backend:
  r: ggplot2 (prcomp)
  python: scikit-learn + matplotlib
difficulty: intermediate
priority: high
status: tested
tags:
  - dataviz
  - chart
  - pca
  - dimensionality-reduction
  - high-dimensional
  - r
  - python
---

# PCA 图 PCA plot

> 用主成分分析把高维特征压到前两三个主成分（PC），散点展示**样本间整体相似性/分群**，并报告各 PC 解释的方差比例。

## 1. 图表定位

回答“**这些样本在高维空间里是否成组/有梯度/有离群**”。线性降维，PC1/PC2 是方差最大的正交方向；轴标签必须带解释方差%。

## 2. 适用场景

- 高维数据（组学表达谱、多指标）的样本级总览/质控。
- 看分组（处理/对照、亚型）是否在主成分空间分离。
- 发现批次效应、离群样本。
- 线性结构为主、需可解释（PC 载荷可追溯）。

## 3. 不适用场景

- 强非线性流形结构 → PCA 压不开，改 UMAP/t-SNE（规划中）。
- 想看“特征级差异显著性” → [[火山图_Volcano]]。
- 想看表达模式聚类 → [[热图_Heatmap]]。
- 样本量很小或特征远多于样本且无正则 → 解释需谨慎。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| 特征矩阵 | numeric（样本×特征）| 数值特征（需标准化）| 必需 |
| group | categorical | 样本分组（着色）| 推荐 |

每行一个样本。**建模前标准化**（scale），否则量纲大的特征主导。

## 5. 图表架构选择

### 5.1 基础架构
- x=PC1、y=PC2 散点；按 group 着色；轴标签含解释方差%（如 `PC1 (48.3%)`）。
- 过原点的虚线参考轴。

### 5.2 高质量架构
- 加组别置信椭圆（如 95%）辅助看分离。
- 必要时画碎石图（scree）说明取几个 PC。
- 离群样本标注；可叠载荷向量（biplot，慎防杂乱）。
- 多 PC → 配对散点矩阵或 PC3。

## 6. 配色选择

### 6.1 默认配色
样本分组用分类色 `cat_main`（Okabe-Ito），见 [[分类变量配色]]。连续协变量着色则用顺序色阶 [[连续变量配色]]。

### 6.2 色盲友好配色
Okabe-Ito；点形状叠加作冗余；椭圆描边区分。

### 6.3 医学研究推荐配色
亚型/处理组用 Okabe-Ito；批次用中性色叠加形状以区别于生物分组。

## 7. R 实现方案

### 7.1 推荐包
ggplot2 + `prcomp`（base）；factoextra（封装 scree/biplot/椭圆，可选）。

### 7.2 关键参数
`prcomp(X, center=TRUE, scale.=TRUE)`；方差比 `sdev^2/sum(sdev^2)`；`geom_point(color=grp)` + 可选 `stat_ellipse()`。

### 7.3 可执行模板
**`templates/r/pca.R`**。核心：
```r
pc <- prcomp(X, center = TRUE, scale. = TRUE)
ev <- pc$sdev^2 / sum(pc$sdev^2) * 100
ggplot(d, aes(PC1, PC2, color = grp)) + geom_point() +
  labs(x = sprintf("PC1 (%.1f%%)", ev[1]), y = sprintf("PC2 (%.1f%%)", ev[2]))
```

## 8. Python 实现方案

### 8.1 推荐包
scikit-learn（`StandardScaler` + `PCA`）+ matplotlib

### 8.2 关键参数
`PCA(n_components=2)`；`explained_variance_ratio_`；标准化后再 fit_transform。

### 8.3 可执行模板
**`templates/python/pca.py`**。核心：
```python
Z = PCA(n_components=2).fit(StandardScaler().fit_transform(X))
ev = Z.explained_variance_ratio_ * 100   # 轴标签用
```

## 9. 示例图像

### 9.1 网络优秀示例
参考 factoextra / sklearn PCA 经典样本散点（带方差% + 椭圆）范式。

### 9.2 本库模板 demo（合成数据，双后端对齐）
Python（sklearn + matplotlib）：

![[tpl_pca_py.png]]

R（prcomp + ggplot2）：

![[tpl_pca_r.png]]

> 三类样本在 PC1/PC2 上清晰分离，轴标签含解释方差%（PC1≈48%、PC2≈28%）；双后端一致。
> 高维/组学需另引公开数据集，本卡用合成多元数据演示范式。

## 10. 常见错误
- 未标准化 → 大量纲特征主导，分群假象。
- 轴标签不写解释方差%（无法判断 PC 重要性）。
- 在强非线性数据上硬用 PCA 并下分群结论。
- 椭圆/biplot 叠太多导致杂乱。
- 用 PCA 分离差当“无差异”结论（PCA 是无监督探索，不是检验）。

## 11. 自动返修规则
- 未标准化 → 自动 scale 并提示。
- 轴缺方差% → 自动补 `explained_variance_ratio_`。
- 前两 PC 解释方差很低 → 提示看 scree / 增维或换非线性方法。
- 点重叠 → 透明度 + 椭圆辅助。

## 12. 与其他图表的关系
- vs UMAP/t-SNE（规划中）：PCA 线性可解释，UMAP/t-SNE 善捕非线性局部结构。
- vs [[热图_Heatmap]]：PCA 看样本整体分群，热图看特征×样本模式。
- vs [[火山图_Volcano]]：PCA 样本级总览，火山特征级差异。

## 13. 质量检查清单
- [ ] 特征已标准化？
- [ ] 轴标签含解释方差%？
- [ ] 分组着色色盲友好？
- [ ] 是否需要椭圆/scree 辅助说明？
- [ ] 结论未把“分离差”当“无差异检验”？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建卡 + 双后端可执行模板 + demo 图（合成数据），状态 tested | 缺真实高维数据集 | 引公开组学集 + 加置信椭圆/scree 变体；扩 UMAP/t-SNE 卡 |

相关：[[热图_Heatmap]] · [[火山图_Volcano]] · [[分类变量配色]] · [[_高维数据图族索引|高维数据图族索引]]
