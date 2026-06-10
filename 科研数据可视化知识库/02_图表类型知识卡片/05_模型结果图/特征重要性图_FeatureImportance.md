---
chart_name: 特征重要性图
chart_name_en: Feature importance / SHAP summary
chart_family: 模型结果图
data_type:
  - feature_matrix
  - model
recommended_backend:
  r: pROC (置换重要性)
  python: shap (beeswarm)
difficulty: intermediate
priority: high
status: tested
tags:
  - dataviz
  - chart
  - feature-importance
  - shap
  - interpretability
  - machine-learning
  - ehr
  - r
  - python
---

# 特征重要性图 Feature importance / SHAP summary

> 把机器学习模型“**哪些变量重要、怎么影响预测**”可视化。EHR/RWD 预测建模的可解释性核心：从“黑箱准不准”到“黑箱在看什么”。

## 1. 图表定位

回答“**模型里哪些特征贡献最大、方向如何**”。两层：① 全局重要性排序（条形）；② SHAP beeswarm——每点一个样本，位置=对预测的贡献(SHAP 值)，颜色=该特征取值高低，兼看“重要性 + 方向 + 异质性”。

## 2. 适用场景

- 树模型/集成模型（RF、XGBoost、LightGBM）在 EHR 上的可解释性汇报。
- 需要向临床说明“模型为何这样预测”——SHAP beeswarm 是当前金标准。
- 特征筛选、模型审计、发现意外的强预测因子（可能是数据泄漏/混杂）。

## 3. 不适用场景

- 只要线性效应方向与显著性 → [[森林图_ForestPlot]]（OR/HR + CI）更直接。
- 把重要性当**因果**解释（重要性=预测贡献 ≠ 因果效应，尤其有共线/混杂时）。
- 样本/特征极多导致 SHAP 计算昂贵 → 抽样或用近似(TreeSHAP)。
- 想要逐样本个体解释 → SHAP force/waterfall（本卡是群体 summary）。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| X | feature matrix | 特征矩阵（样本×特征）| 必需 |
| model | fitted | 训练好的模型 | 必需 |
| y | outcome | 结局（训练用）| 训练时需 |

SHAP beeswarm 需要模型 + 背景数据 X。

## 5. 图表架构选择

### 5.1 基础架构
- **置换重要性/不纯度重要性条形图**：特征按重要性排序，横条。
- **SHAP beeswarm**：y=特征（按平均|SHAP|排序），x=SHAP 值，点=样本，色=特征值。

### 5.2 高质量架构
- 优先 SHAP beeswarm（信息最全）；条形图作补充或当 SHAP 不可得时的退路。
- 置换重要性比不纯度重要性更可靠（不偏向高基数特征）。
- 限制显示 top N（如 10）避免拥挤。
- 注明重要性定义（AUC 下降 / 平均|SHAP|）。

## 6. 配色选择

### 6.1 默认配色
- 条形图：单色（`med_case_control` low）。
- SHAP beeswarm：特征值用**连续发散色**（低→高，shap 默认蓝→红），语义见 [[连续变量配色]]/[[发散变量配色]]。

### 6.2 色盲友好配色
beeswarm 蓝→红对多数色觉安全；条形单色无障碍。

### 6.3 医学研究推荐配色
保持 SHAP 蓝(低)→红(高)惯例，便于读者迁移经验。

## 7. R 实现方案

### 7.1 推荐包
本库默认：base `glm` + pROC **置换重要性**（无 RF 包依赖）。进阶：`ranger`/`randomForest`（重要性）、`fastshap`/`shapviz`（R 端 SHAP，需另装）。

### 7.2 关键参数
打乱单列 → 重算 AUC → 下降量=重要性；多次重复取均值；`geom_col` 横向排序。

### 7.3 可执行模板
**`templates/r/importance.R`**（glm + pROC 置换重要性条形）。核心：
```r
imp <- sapply(feats, function(f){ d2<-df; d2[[f]]<-sample(d2[[f]])
  base_auc - auc(df$y, predict(fit,newdata=d2,type="response")) })
```

## 8. Python 实现方案

### 8.1 推荐包
shap（旗舰 beeswarm）+ scikit-learn（树模型 / `permutation_importance`）。

### 8.2 关键参数
`shap.TreeExplainer(model)(X)`；二分类取阳性类 `exp[...,1]`；`shap.plots.beeswarm(exp, max_display=)`。

### 8.3 可执行模板
**`templates/python/importance.py`**（RandomForest + SHAP beeswarm）。核心：
```python
exp = shap.TreeExplainer(model)(X)
if exp.values.ndim == 3: exp = exp[..., 1]
shap.plots.beeswarm(exp, max_display=10, show=False)
```

## 9. 示例图像

### 9.1 网络优秀示例
参考 shap 官方 beeswarm / summary_plot 范式。

### 9.2 本库模板 demo（合成 EHR 数据，双后端互补）
Python（SHAP beeswarm，旗舰）：

![[tpl_importance_py.png]]

R（glm + pROC 置换重要性条形）：

![[tpl_importance_r.png]]

> 合成 EHR：Glucose、Age、Smoker 为最强预测因子（与生成机制一致）；SHAP beeswarm 还显示高血糖/高龄把预测推高（红点在右）。
> 注：双后端此处**互补而非等价**——Python 给逐样本 SHAP，R 给全局置换重要性；R 端 SHAP 可用 fastshap/shapviz 扩展。

## 10. 常见错误
- 用不纯度重要性且有高基数特征 → 重要性虚高（改置换/SHAP）。
- 把重要性/SHAP 当因果效应解读。
- 在测试集外/数据泄漏特征上得到“超强预测因子”不警觉。
- beeswarm 显示过多特征导致拥挤。
- 不交代重要性的定义口径。

## 11. 自动返修规则
- 特征 > ~15 → 只显 top N。
- 检测到疑似泄漏特征（重要性异常压倒性）→ 提示核查。
- 不纯度重要性 + 高基数特征 → 建议改置换/SHAP。
- 类别不平衡 → SHAP 取阳性类并注明。

## 12. 与其他图表的关系
- vs [[森林图_ForestPlot]]：森林=线性模型系数 + CI（可推断）；重要性/SHAP=任意模型预测贡献（含非线性/交互）。
- 配合 [[混淆矩阵_ConfusionMatrix]]/[[ROC曲线_ROC]]/[[决策曲线_DCA]]：先证明模型有用，再解释模型在看什么。
- SHAP 依赖图(dependence)可进一步看单特征的非线性形状（规划中）。

## 13. 质量检查清单
- [ ] 重要性口径写明（AUC 下降 / 平均|SHAP|）？
- [ ] 用了更稳健的置换/SHAP（而非纯不纯度）？
- [ ] top N 限制、不拥挤？
- [ ] 未把重要性误读为因果？
- [ ] beeswarm 配色遵循低蓝高红？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建卡 + Python SHAP beeswarm + R 置换重要性模板 + demo 图，状态 tested | 双后端互补非等价；R 暂无原生 SHAP | 加 SHAP dependence 图 + R 端 shapviz 模板 |

相关：[[森林图_ForestPlot]] · [[ROC曲线_ROC]] · [[决策曲线_DCA]] · [[连续变量配色]] · [[发散变量配色]]
