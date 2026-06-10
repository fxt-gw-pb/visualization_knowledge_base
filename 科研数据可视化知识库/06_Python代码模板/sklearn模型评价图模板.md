---
title: sklearn 模型评价图模板
type: code-template
status: active
backend: python
updated: 2026-06-10
tags:
  - dataviz
  - python
  - sklearn
  - roc
  - calibration
  - template
---

# sklearn 模型评价图模板

> scikit-learn 的 `*Display` 类一行出评价图，可叠多模型同图。配合 [[ROC曲线_ROC]] / [[校准曲线_Calibration]]。

## 1. ROC 曲线（含多模型对比）

```python
from sklearn.metrics import RocCurveDisplay, roc_auc_score
import matplotlib.pyplot as plt
set_pub_style()                                  # matplotlib通用主题

fig, ax = plt.subplots(figsize=(3.5, 3.5))
for name, model in models.items():               # >>> PARAM 多模型 dict
    RocCurveDisplay.from_estimator(model, X_test, y_test, name=name, ax=ax)
ax.plot([0,1],[0,1], ls="--", c="grey", lw=.8)   # 随机对角线（参考线）
ax.set_xlabel("1 − Specificity (FPR)"); ax.set_ylabel("Sensitivity (TPR)")
ax.set_aspect("equal")                           # ROC 正方形
fig.savefig("roc.pdf")
# 从预测概率直接画： RocCurveDisplay.from_predictions(y_test, y_score, name="...")
```

> AUC 自动进图例；如需 CI，bootstrap 重抽 AUC 取 2.5/97.5 分位（[[ROC曲线_ROC]]）。

## 2. PR 曲线（类别不平衡时补充 ROC）

```python
from sklearn.metrics import PrecisionRecallDisplay
fig, ax = plt.subplots(figsize=(3.5, 3.5))
PrecisionRecallDisplay.from_estimator(model, X_test, y_test, ax=ax)
ax.set_xlabel("Recall"); ax.set_ylabel("Precision")
# 基线 = 阳性率： ax.axhline(y_test.mean(), ls="--", c="grey")
```

## 3. 混淆矩阵热图

```python
from sklearn.metrics import ConfusionMatrixDisplay
ConfusionMatrixDisplay.from_estimator(model, X_test, y_test,
    cmap="Blues", normalize="true", values_format=".2f")  # 行归一化看灵敏度
```

## 4. 校准曲线

```python
from sklearn.calibration import CalibrationDisplay
fig, ax = plt.subplots(figsize=(3.5, 3.5))
CalibrationDisplay.from_estimator(model, X_test, y_test,
    n_bins=10, strategy="quantile", ax=ax)       # >>> PARAM 分箱
ax.plot([0,1],[0,1], ls="--", c="grey")          # 完美校准对角线
ax.set_xlabel("Predicted probability"); ax.set_ylabel("Observed frequency")
ax.set_aspect("equal")
```
详见 [[校准曲线_Calibration]]（loess 平滑替代分箱、Brier score）。

## 5. 关键参数（旋钮）

| 参数 | 作用 |
|---|---|
| `from_estimator` vs `from_predictions` | 有模型对象 vs 只有预测概率 |
| `ax` | 叠多模型到同一 Axes |
| `name` | 图例标签（带 AUC）|
| `normalize`（混淆矩阵）| "true"/"pred"/"all" |
| `n_bins`/`strategy`（校准）| 分箱数与方式（uniform/quantile）|

## 6. 评价前置（先评对再画）

- 用**测试集 / 交叉验证**，别在训练集上画评价图。
- 概率要**校准过**再谈校准曲线（[[校准曲线_Calibration]]）。
- 类别不平衡：ROC 可能过于乐观，**补 PR 曲线**。

## 7. 常见错误（→ 返修）

- ❌ 训练集上画 ROC → 过于乐观，用 hold-out/CV。
- ❌ 多模型线缠绕 → 标 AUC、限 ≤4 条或分面（[[ROC曲线_ROC]]）。
- ❌ ROC 非正方形 → `set_aspect("equal")`。
- ❌ 不平衡只看 ROC → 补 PR。
- ❌ 漏对角参考线。

相关：[[ROC曲线_ROC]] · [[校准曲线_Calibration]] · [[matplotlib通用主题]] · [[Python导出规范]]
