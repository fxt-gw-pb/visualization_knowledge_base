---
chart_name: 决策曲线分析
chart_name_en: Decision curve analysis (DCA)
chart_family: 预测模型评价图
data_type:
  - predicted_probability
  - binary_outcome
recommended_backend:
  r: ggplot2
  python: matplotlib
difficulty: intermediate
priority: high
status: tested
tags:
  - dataviz
  - chart
  - dca
  - net-benefit
  - clinical-utility
  - model-evaluation
  - r
  - python
---

# 决策曲线分析 Decision curve analysis (DCA)

> 在不同“治疗阈值概率”下，比较**用模型决策 vs 全部治疗 vs 全不治疗**的**净获益(net benefit)**。回答“这个预测模型临床上到底有没有用”，而非只看判别/校准。

## 1. 图表定位

回答“**在临床可接受的阈值范围内，按模型决策能比默认策略多带来多少净获益**”。净获益把假阳性的代价按阈值折算，贴近真实临床决策。

## 2. 适用场景

- 评估临床预测模型/标志物的**实用价值**（RWD 预测建模标配，常与 ROC/校准三件套同报）。
- 比较多个模型/变量组合谁在相关阈值区间净获益更高。
- 向临床读者说明“用了这个模型该不该干预”。

## 3. 不适用场景

- 只关心判别力 → [[ROC曲线_ROC]]；只关心概率准不准 → [[校准曲线_Calibration]]。
- 没有可解释的“治疗阈值”语境（纯排序任务）→ DCA 意义弱。
- 结局非二分类 → 需对应扩展（生存 DCA 等），非本基础卡。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| y_true | binary | 真实结局(0/1) | 必需 |
| y_prob | continuous(0–1) | 模型预测概率 | 必需 |

净获益公式：`NB = TP/n − FP/n × (pt/(1−pt))`，`pt` 为阈值概率。

## 5. 图表架构选择

### 5.1 基础架构
- x=阈值概率 pt；y=净获益；三条线：模型、Treat all（斜降）、Treat none（y=0）。
- 阈值范围取临床合理区间（如 1%–60%）。

### 5.2 高质量架构
- 模型曲线高于 all/none 的区间=模型“有用”的阈值范围，可阴影标注。
- 多模型对比 → 多条彩色线（[[分类变量配色]]）。
- y 轴下限略低于 0 以显示劣于 none 的区段。
- 可加平滑/自助 CI（高级）。

## 6. 配色选择

### 6.1 默认配色
模型用醒目主色（`med_case_control` low 蓝）；Treat all 用中性灰；Treat none 黑色虚线。多模型用 `cat_main`。见 [[分类变量配色]]。

### 6.2 色盲友好配色
线型冗余（实/虚）+ Okabe-Ito；参考线灰/黑。

### 6.3 医学研究推荐配色
约定俗成：模型彩色实线、all 灰、none 黑虚线，全文一致。

## 7. R 实现方案

### 7.1 推荐包
ggplot2（净获益手算）；rmda / dcurves（专用包，需另装）。

### 7.2 关键参数
`nb(t)=TP/n − FP/n×t/(1−t)`；treat-all `=prev−(1−prev)×t/(1−t)`；`geom_line`+线型映射。

### 7.3 可执行模板
**`templates/r/dca.R`**（纯 base 计算 + ggplot，免 dcurves）。核心：
```r
nb <- function(t){ tp<-sum(prob>=t & y==1); fp<-sum(prob>=t & y==0); tp/n - fp/n*(t/(1-t)) }
```

## 8. Python 实现方案

### 8.1 推荐包
matplotlib（净获益手算）

### 8.2 关键参数
同公式向量化；三线绘制；y 下限留负区。

### 8.3 可执行模板
**`templates/python/dca.py`**。核心：
```python
def net_benefit(y,p,t):
    tp=((p>=t)&(y==1)).sum(); fp=((p>=t)&(y==0)).sum(); return tp/len(y)-fp/len(y)*(t/(1-t))
```

## 9. 示例图像

### 9.1 网络优秀示例
参考 Vickers 的 DCA 原始范式 / rmda、dcurves 文档图。

### 9.2 本库模板 demo（合成预测，双后端对齐）
Python（matplotlib）：

![[tpl_dca_py.png]]

R（ggplot2）：

![[tpl_dca_r.png]]

> 在中低阈值区间，模型净获益高于 Treat all / Treat none，说明该阈值范围内用模型决策有获益；双后端一致。

## 10. 常见错误
- 阈值范围取得不合临床（如画到 90%）。
- 不画 Treat all / Treat none 参照（无法判断“是否有用”）。
- 把 DCA 当判别/校准替代（三者互补，不可互替）。
- y 轴砍掉负区，掩盖模型劣于默认策略的区段。
- 概率未校准就做 DCA（净获益对校准敏感，先看 [[校准曲线_Calibration]]）。

## 11. 自动返修规则
- 缺参照线 → 自动补 Treat all / none。
- 阈值范围异常 → 收敛到临床合理区间并提示。
- 概率明显未校准 → 提示先校准再 DCA。
- 多模型 → 自动分配 Okabe-Ito 颜色 + 图例。

## 12. 与其他图表的关系
- 与 [[ROC曲线_ROC]] + [[校准曲线_Calibration]] 组成预测模型评价“三件套”：判别 / 校准 / 临床获益。
- vs [[混淆矩阵_ConfusionMatrix]]：混淆矩阵单阈值对错，DCA 跨阈值净获益。

## 13. 质量检查清单
- [ ] 含 Treat all / Treat none 参照？
- [ ] 阈值范围临床合理？
- [ ] y 轴保留负区？
- [ ] 概率已校准（或注明）？
- [ ] 多模型配色/线型可辨？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-10 | v0.1 | 建卡 + 双后端可执行模板（纯计算，免 dcurves）+ demo 图，状态 tested | 未加自助 CI | 加多模型对比 + bootstrap CI + 生存 DCA 变体 |

相关：[[ROC曲线_ROC]] · [[校准曲线_Calibration]] · [[混淆矩阵_ConfusionMatrix]] · [[森林图_ForestPlot]]
