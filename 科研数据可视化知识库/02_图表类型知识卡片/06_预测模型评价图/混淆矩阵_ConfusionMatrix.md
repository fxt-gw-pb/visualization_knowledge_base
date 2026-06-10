---
chart_name: 混淆矩阵热图
chart_name_en: Confusion matrix
chart_family: 预测模型评价图
data_type:
  - predicted_class
  - actual_class
recommended_backend:
  r: ggplot2
  python: scikit-learn/seaborn
difficulty: basic
priority: high
status: tested
tags:
  - dataviz
  - chart
  - confusion-matrix
  - classification
  - model-evaluation
  - r
  - python
---

# 混淆矩阵热图 Confusion matrix

> 把分类模型的预测类别 × 真实类别交叉计数画成热图，直观看 TP/FP/FN/TN 与各类别的对错分布。分类模型评价的基础图。

## 1. 图表定位

回答“**模型把谁分对了、把谁错分成了谁**”。在某个决策阈值下，展示真阳/假阳/假阴/真阴；多分类则看类别间混淆方向。

## 2. 适用场景

- 二分类/多分类模型在固定阈值下的评价（疾病有/无、分期）。
- 想看**错误类型**（漏诊 FN vs 误诊 FP）哪个更严重——EHR 临床决策关键。
- 配合行/列归一看灵敏度、特异度、PPV、NPV。

## 3. 不适用场景

- 评价跨所有阈值的整体判别 → [[ROC曲线_ROC]]（不依赖单一阈值）。
- 评价概率是否可信 → [[校准曲线_Calibration]]。
- 评价临床净获益 → [[决策曲线_DCA]]。
- 类别极多（>~10）→ 矩阵太大，改 top 混淆对列表或层次聚类。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| y_true | categorical | 真实类别 | 必需 |
| y_pred | categorical | 预测类别（已按阈值二值化）| 必需 |

注意：predict_proba 需先按阈值转成类别。

## 5. 图表架构选择

### 5.1 基础架构
- 行=真实、列=预测（或反之，**标清楚**）；格内=计数。
- 对角=正确，非对角=错误。

### 5.2 高质量架构
- 同时标**计数 + 行归一百分比**（行归一=各真实类别的召回视角）。
- 颜色映射用单色顺序（按比例），不抢注释。
- 类别不平衡时优先看归一值而非原始计数。
- 可在标题/旁注附 Sensitivity/Specificity/PPV/NPV。

## 6. 配色选择

### 6.1 默认配色
单色顺序色阶（`seq_blues`，比例越高越深），见 [[连续变量配色]]。避免发散色（这里无正负语义）。

### 6.2 色盲友好配色
单色顺序天然安全；注释文字保证对比度（深底白字）。

### 6.3 医学研究推荐配色
中性单色即可；如需强调漏诊，可单独高亮 FN 格。

## 7. R 实现方案

### 7.1 推荐包
ggplot2（`table()` → `geom_tile`）；caret（`confusionMatrix` 出指标）。

### 7.2 关键参数
`table(actual, pred)`；行归一 `ave(n, actual, FUN=sum)`；`geom_tile`+`geom_text`+`scale_fill_gradient`+`coord_equal`。

### 7.3 可执行模板
**`templates/r/confusion.R`**。核心：
```r
cm <- table(actual, pred); d <- as.data.frame(cm)
ggplot(d, aes(Predicted, Actual, fill = pct)) + geom_tile() +
  geom_text(aes(label = sprintf("%d\n%.0f%%", n, pct*100)))
```

## 8. Python 实现方案

### 8.1 推荐包
scikit-learn（`confusion_matrix`/`ConfusionMatrixDisplay`）+ seaborn

### 8.2 关键参数
`confusion_matrix(y_true,y_pred)`；行归一；`sns.heatmap(annot=, cmap=, square=True)`。

### 8.3 可执行模板
**`templates/python/confusion.py`**。核心：
```python
cm = confusion_matrix(y_true, y_pred)
sns.heatmap(cm/cm.sum(1,keepdims=True), annot=count_pct, fmt="", cmap=pal("seq_blues"), square=True)
```

## 9. 示例图像

### 9.1 网络优秀示例
参考 sklearn `ConfusionMatrixDisplay` 范式（计数 + 归一）。

### 9.2 本库模板 demo（合成预测，双后端对齐）
Python（sklearn + seaborn）：

![[tpl_confusion_py.png]]

R（ggplot2）：

![[tpl_confusion_r.png]]

> 行归一显示 Event 召回 ~78%、No event 特异 ~88%；颜色深浅=各真实类别内的比例。双后端一致。

## 10. 常见错误
- 行/列谁是真实谁是预测没标清。
- 类别不平衡只看原始计数（大类主导观感）。
- 只给计数不给比例（无法读召回/精确率）。
- 用发散配色暗示不存在的“正负”。
- 把多阈值评价压成单一混淆矩阵下结论（应配 ROC）。

## 11. 自动返修规则
- 类别不平衡 → 默认显示行归一百分比。
- 类别 > ~10 → 改 top 混淆对或聚类排序。
- 注释与底色对比不足 → 自动切深底白字。
- 缺指标 → 旁注 Sens/Spec/PPV/NPV。

## 12. 与其他图表的关系
- vs [[ROC曲线_ROC]]：混淆矩阵=单阈值快照，ROC=全阈值判别力。
- vs [[校准曲线_Calibration]]：前者看分类对错，后者看概率可信度。
- vs [[决策曲线_DCA]]：DCA 把阈值与临床获益挂钩。

## 13. 质量检查清单
- [ ] 行/列（真实/预测）标注清楚？
- [ ] 同时给计数与归一比例？
- [ ] 单色顺序配色、注释可读？
- [ ] 不平衡数据下结论基于归一值？
- [ ] 是否需补 Sens/Spec/PPV/NPV？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建卡 + 双后端可执行模板 + demo 图，状态 tested | — | 可加多分类示例 + 指标旁注 |

相关：[[ROC曲线_ROC]] · [[校准曲线_Calibration]] · [[决策曲线_DCA]] · [[连续变量配色]]
