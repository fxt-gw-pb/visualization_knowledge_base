---
chart_name: ROC 曲线
chart_name_en: ROC curve
chart_family: 预测模型评价图
data_type:
  - predicted_probability
  - binary_outcome
recommended_backend:
  r: pROC
  python: scikit-learn
difficulty: intermediate
priority: high
status: tested
tags:
  - dataviz
  - chart
  - roc
  - auc
  - model-evaluation
  - r
  - python
---

# ROC 曲线 ROC curve

> 在所有阈值下画“灵敏度 vs 1−特异度”，AUC 概括整体判别力。二分类预测模型评价的标准图。PR 曲线作为不平衡场景的补充。

## 1. 图表定位

回答“**模型区分阳/阴的能力有多强（与阈值无关）**”。AUC = 随机取一阳一阴、模型给阳更高分的概率。

## 2. 适用场景

- 二分类预测模型评价（logistic、ML 分类器）。
- 多模型判别力对比（同图叠加，标 AUC）。
- 配 PR 曲线评估不平衡数据。
- Framingham：预测 DEATH 的模型 ROC。

## 3. 不适用场景

- 严重类别不平衡且关注阳性类 → ROC 过于乐观，**优先看 PR 曲线**。
- 关注校准（概率是否准）→ ROC 不管校准，看 [[校准曲线_Calibration]]。
- 多分类 → 需 one-vs-rest 多条或宏平均。
- 想要临床净获益 → 决策曲线（DCA）。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 必需 |
|---|---|---|---|
| y_true | binary | 真实标签（0/1）| 必需 |
| y_score | continuous | 预测概率/打分 | 必需 |
| model | categorical | 多模型标识 | 可选 |

**必须用 hold-out/交叉验证的预测**，不能训练集自评。

## 5. 图表架构选择

### 5.1 基础架构
- x = 1−特异度（FPR），y = 灵敏度（TPR）；
- 阶梯/曲线 + 对角参考线（随机）；
- 正方形（`aspect=equal`）；
- 图例标 AUC。

### 5.2 高质量架构
- AUC + 95% CI（bootstrap 或 DeLong）。
- 多模型 ≤ 4 条，颜色 + 线型；多了分面。
- 可标“最优阈值”点（Youden）。
- DeLong 检验比较两 AUC（标 p）。

## 6. 配色选择
- 多模型 Okabe-Ito + 线型（[[分类变量配色]] / [[色盲友好与打印友好原则]]）。
- 对角线浅灰虚线。

## 7. R 实现方案

### 7.1 推荐包
pROC、ggplot2、（plotROC 可选）

### 7.2 关键参数
`pROC::roc(y, score)`、`auc()`、`ci.auc()`、`ggroc()`、`roc.test()`（DeLong 比较）。

### 7.3 基础代码模板
```r
library(pROC)
r <- roc(df$DEATH, df$pred, quiet = TRUE)
plot(r, legacy.axes = TRUE, print.auc = TRUE)         # x=1-spec
```

### 7.4 发表级代码模板（多模型 + CI）
```r
library(pROC); library(ggplot2)
r1 <- roc(df$DEATH, df$pred_m1); r2 <- roc(df$DEATH, df$pred_m2)
ci1 <- ci.auc(r1)                                     # AUC 95%CI
ggroc(list(`Model A` = r1, `Model B` = r2), legacy.axes = TRUE, linewidth = 1) +
  geom_abline(slope = 1, intercept = 1, linetype = 2, color = "grey60") +  # legacy.axes 下对角
  scale_color_manual(values = c("#0072B2","#D55E00")) +
  coord_equal() +
  labs(x = "1 − Specificity", y = "Sensitivity", color = NULL) +
  annotate("text", x = .6, y = .2,
           label = sprintf("AUC A = %.3f (%.3f–%.3f)", ci1[2], ci1[1], ci1[3])) +
  theme_pub()
roc.test(r1, r2)        # DeLong 比较两 AUC
```

## 8. Python 实现方案

### 8.1 推荐包
scikit-learn（`RocCurveDisplay`）、matplotlib、（scipy bootstrap）

### 8.2 关键参数
见 [[sklearn模型评价图模板]]：`RocCurveDisplay.from_estimator/from_predictions(name=, ax=)`、`roc_auc_score`。

### 8.3 基础代码模板
```python
from sklearn.metrics import RocCurveDisplay
fig, ax = plt.subplots(figsize=(3.5,3.5))
RocCurveDisplay.from_predictions(df.DEATH, df.pred, name="Model", ax=ax)
ax.plot([0,1],[0,1], ls="--", c="grey"); ax.set_aspect("equal")
```

### 8.4 发表级代码模板（多模型 + bootstrap CI）
```python
from sklearn.metrics import RocCurveDisplay, roc_auc_score
import numpy as np
fig, ax = plt.subplots(figsize=(3.6,3.6))
for name, s in preds.items():                         # preds: dict[name -> y_score]
    RocCurveDisplay.from_predictions(y_true, s, name=name, ax=ax)
ax.plot([0,1],[0,1], ls="--", c="grey", lw=.8)
ax.set_xlabel("1 − Specificity"); ax.set_ylabel("Sensitivity"); ax.set_aspect("equal")
# bootstrap AUC 95% CI
def boot_auc(y, s, n=1000):
    rng=np.random.default_rng(2026); aucs=[]
    y=np.asarray(y); s=np.asarray(s)
    for _ in range(n):
        idx=rng.integers(0,len(y),len(y))
        if len(np.unique(y[idx]))<2: continue
        aucs.append(roc_auc_score(y[idx], s[idx]))
    return np.percentile(aucs,[2.5,97.5])
```

## 9. 示例图像

### 9.1 网络优秀示例
见 [[ROC_优秀示例]]（含多模型 ROC + AUC CI、sklearn 范式）。
本库自制范式图（合成数据，正方形 + 对角线 + AUC）：

![[demo_roc.png]]

### 9.2 Framingham 数据测试示例
✅ 已跑通（logistic 预测 DEATH 的 ROC + AUC + bootstrap 95%CI）。代码见 [[Python测试记录]] 与 [[sklearn模型评价图模板]]。

R（pROC + AUC 95%CI）：

![[fig_roc_death_r.png]]

Python（sklearn roc_curve + bootstrap CI）：

![[fig_roc_death_py.png]]

> 结论：模型 AUC≈0.765（95% CI≈0.749–0.782）。R（pROC DeLong CI）与 Python（bootstrap CI）数值一致。⚠️ 此处为同数据训练+评价的**流程演示**，非外部验证；正式评价须 hold-out / 交叉验证（见本卡片第 10 节）。

## 10. 常见错误
- 训练集上画 ROC（过于乐观）。
- 不平衡只看 ROC（应补 PR）。
- 非正方形、轴标签是 TPR/FPR 不友好。
- 多模型缠绕、不标 AUC。
- 漏对角参考线。
- AUC 不给 CI。

## 11. 自动返修规则
- 多模型缠绕 → ≤4 条、颜色+线型、或分面。
- 不平衡 → 自动补 PR 曲线。
- 非方形 → `coord_equal`/`set_aspect("equal")`。
- 无 CI → bootstrap/DeLong 补 AUC CI。
- 用训练集 → 提示改 hold-out/CV。

## 12. 与其他图表的关系
- vs PR 曲线：不平衡数据 PR 更敏感；二者同族（本卡片含 PR）。
- vs [[校准曲线_Calibration]]：ROC 看判别（区分能力），校准看概率准不准——**互补，缺一不可**。
- vs 混淆矩阵：ROC 跨所有阈值，混淆矩阵是某一阈值的快照。

## 13. 质量检查清单
- [ ] 用的是测试集/CV 预测？
- [ ] 正方形 + 对角参考线？
- [ ] AUC（+CI）标注？
- [ ] 不平衡时是否补 PR？
- [ ] 多模型可分辨？
- [ ] 适合论文导出？

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建立初稿 | 缺实测图 | 跑 DEATH logistic ROC + CI |

相关：[[校准曲线_Calibration]] · [[森林图_ForestPlot]] · [[sklearn模型评价图模板]] · [[分类变量配色]]
