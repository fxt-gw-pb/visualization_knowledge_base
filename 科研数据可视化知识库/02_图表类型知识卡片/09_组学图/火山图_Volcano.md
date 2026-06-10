---
chart_name: 火山图
chart_name_en: Volcano plot
chart_family: 组学图
data_type:
  - effect_size
  - pvalue
recommended_backend:
  r: ggplot2
  python: matplotlib/seaborn
difficulty: intermediate
priority: high
status: tested
tags:
  - dataviz
  - chart
  - volcano
  - omics
  - differential-expression
  - r
  - python
---

# 火山图 Volcano plot

> 把每个特征（基因/蛋白/代谢物）的**效应量（log2 fold change）与显著性（−log10 p）**画成散点，一眼看出哪些上调/下调且显著。组学差异分析标配。

## 1. 图表定位

回答“**成千上万个特征里，哪些既变化大又统计显著**”。x=变化方向与幅度，y=显著性；右上=显著上调，左上=显著下调。

## 2. 适用场景

- 差异表达/差异丰度分析结果（RNA-seq、蛋白、代谢、甲基化）。
- 同时按效应阈值（|log2FC|）与显著阈值（adj.p）筛选并可视化。
- 想标注 top 命中特征。

## 3. 不适用场景

- 特征很少（< ~50）→ 火山图稀疏，直接表格/森林更清楚。
- 没有效应量或没有 p 值（缺一个轴）→ 不成立。
- 想看表达模式聚类 → [[热图_Heatmap]]；看样本分群 → [[PCA图_PCA]]。
- 未做多重检验校正就标显著 → 先校正（FDR/BH），用 adj.p。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| log2fc | continuous | log2 fold change（效应量）| 必需 |
| padj | continuous(0–1) | 校正后 p 值（FDR/BH）| 必需 |
| label | text | 特征名（标注 top 用）| 可选 |

每行一个特征。p 用**校正后**值。

## 5. 图表架构选择

### 5.1 基础架构
- x：log2FC；y：−log10(padj)；阈值线：水平=p 阈，竖直=±FC 阈。
- 三类着色：上调 / 下调 / 不显著。

### 5.2 高质量架构
- 点半透明 + 小尺寸防 overplot（特征极多）。
- 标注 top N 命中（按 padj 或 |log2FC| 排序）用 `ggrepel`/`adjustText` 防重叠。
- 极小 padj 截断（避免 y 轴被个别点拉爆）并注明。
- 图例标各类计数。

## 6. 配色选择

### 6.1 默认配色
**效应方向**语义：上调暖色、下调冷色、不显著灰——用 [[模型效应方向配色]]（`effect_dir`：harm 红=上调、protect 蓝=下调、ns 灰）。

### 6.2 色盲友好配色
红/蓝/灰本身色盲安全；再以位置（左右）冗余编码方向。

### 6.3 医学研究推荐配色
固定“上调红/下调蓝”惯例，全文一致；勿用红绿。

## 7. R 实现方案

### 7.1 推荐包
ggplot2（+ ggrepel 标注）；EnhancedVolcano（封装，可选）。

### 7.2 关键参数
按阈值生成 `sig` 因子 → `geom_point(color=sig)`；`geom_hline/vline`；`scale_color_manual`。

### 7.3 可执行模板
**`templates/r/volcano.R`**（改 `FC_THR`/`P_THR`）。核心：
```r
df$sig <- with(df, ifelse(padj<P_THR & log2fc> FC_THR,"up",
                   ifelse(padj<P_THR & log2fc< -FC_THR,"down","ns")))
ggplot(df, aes(log2fc, -log10(padj), color=sig)) + geom_point(size=.7, alpha=.5) +
  scale_color_manual(values=c(down=pal("effect_dir")["protect"], ns=pal("effect_dir")["ns"], up=pal("effect_dir")["harm"]))
```

## 8. Python 实现方案

### 8.1 推荐包
matplotlib/seaborn（+ adjustText 标注）

### 8.2 关键参数
分类着色循环绘制（ns 先画在底层）；`axhline/axvline` 阈值线；`-np.log10(padj)`。

### 8.3 可执行模板
**`templates/python/volcano.py`**。核心见文件 `# >>> PARAM`（`effect_dir` 配色 + 阈值线 + 图例计数）。

## 9. 示例图像

### 9.1 网络优秀示例
参考 EnhancedVolcano / 经典 RNA-seq volcano 范式。

### 9.2 本库模板 demo（合成数据，双后端对齐）
Python（matplotlib）：

![[tpl_volcano_py.png]]

R（ggplot2）：

![[tpl_volcano_r.png]]

> 4000 个合成特征：显著上调（红）/下调（蓝）/不显著（灰）按 |log2FC|>1 且 padj<0.05 分类，阈值线清晰；双后端一致。
> 组学数据需另引公开数据集，本卡用合成数据演示范式（license 干净）。

## 10. 常见错误
- 用未校正 p（应 FDR/BH 后的 padj）。
- 点不透明 + 太大 → 中间糊成一团。
- y 轴被极小 p 拉爆，多数点压在底部。
- 标注过多 top 基因互相重叠。
- 上调/下调配色随意（破坏“红上蓝下”惯例）。

## 11. 自动返修规则
- overplot → 减小点径 + 降 alpha。
- 极端 −log10p → 截断并注明。
- 标注重叠 → ggrepel/adjustText 自动避让，或只标 top N。
- 用了原始 p → 提示改 adj.p。

## 12. 与其他图表的关系
- vs [[热图_Heatmap]]：火山看“哪些差异显著”，热图看“差异特征的表达模式/聚类”，常配套。
- vs [[PCA图_PCA]]：PCA 看样本整体分群，火山看特征级差异。
- vs MA 图：MA=均值 vs log2FC（规划中），火山=显著性 vs log2FC。

## 13. 质量检查清单
- [ ] 用校正后 p（adj.p）？
- [ ] 阈值线（FC、p）画出并注明阈值？
- [ ] overplot 处理（小点/透明）？
- [ ] 配色遵循“上调红/下调蓝/不显著灰”？
- [ ] 标注（若有）不重叠？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建卡 + 双后端可执行模板 + demo 图（合成数据），状态 tested | 缺真实组学数据集 | 引入公开 RNA-seq 集做实测 + top 基因标注 |

相关：[[热图_Heatmap]] · [[PCA图_PCA]] · [[模型效应方向配色]] · [[_组学图族索引|组学图族索引]]
