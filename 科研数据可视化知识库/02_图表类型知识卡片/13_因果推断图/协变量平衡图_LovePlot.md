---
chart_name: 协变量平衡图
chart_name_en: Covariate balance (Love plot)
chart_family: 因果推断图
data_type:
  - covariate_smd
  - treatment_group
recommended_backend:
  r: ggplot2
  python: matplotlib
difficulty: intermediate
priority: high
status: tested
tags:
  - dataviz
  - chart
  - love-plot
  - smd
  - balance
  - psm
  - iptw
  - causal-inference
  - rwd
  - r
  - python
---

# 协变量平衡图 Covariate balance (Love plot)

> 把每个协变量在**匹配/加权前 vs 后**的**标准化均差(SMD)**画成点，一眼看出倾向评分匹配(PSM)/逆概率加权(IPTW)有没有真的把两组拉平。RWD 因果推断的“**可比性合规证据**”。

## 1. 图表定位

回答“**调整之后，处理组与对照组的基线还差多少**”。横轴是 |SMD|，每个协变量两点（前/后），加一条 0.1 阈值线——后点几乎都落到阈值内 = 平衡达成，效应估计才可信。

## 2. 适用场景

- PSM / IPTW / 精确匹配 / 标准化后的**平衡诊断**（观察性研究标配，几乎必报）。
- 比较多种调整方案（不同卡钳、不同权重）谁拉得更平。
- 向审稿人证明“混杂已在可观测层面调平”。

## 3. 不适用场景

- 还没做任何调整（只有一组 SMD）→ 那是基线 Table 1 的事，不必画 Love plot。
- 协变量极少（2–3 个）→ 直接表格列 SMD 更省。
- 想证明“无未观测混杂”→ Love plot 管不了，需敏感性分析（E-value 等）。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| covariate | 分类 | 协变量名 | 必需 |
| smd_before | 数值≥0 | 调整前 \|SMD\| | 必需 |
| smd_after | 数值≥0 | 调整后 \|SMD\| | 必需 |

SMD（连续变量）`= (mean_t − mean_c) / sqrt((s_t²+s_c²)/2)`；二分类用比例与 `sqrt(p(1−p))`。取绝对值。

## 5. 图表架构选择

### 5.1 基础架构
- y=协变量（按调整前 |SMD| 降序，影响最大的在顶）；x=|SMD|；前/后两组点 + 连线。
- 0.1 处加竖虚线（平衡阈值）。

### 5.2 高质量架构
- x 从 0 起；点配连线引导视线（前→后收缩）。
- 多方案对比 → 多组点/颜色；点多时可只标越界者。
- 可加 0.25（宽松阈值）第二条线；交互项/样条项也应纳入平衡评估。

## 6. 配色选择

### 6.1 默认配色
调整前用中性灰（`effect_dir` 的 ns），调整后用醒目主色（`med_case_control` low 蓝）——“灰→蓝收缩到阈值内”的叙事。见 [[医学二分类配色]]。

### 6.2 色盲友好配色
前/后用形状冗余（空心/实心）+ Okabe-Ito 两色；阈值线灰。

### 6.3 医学研究推荐配色
全文统一“前灰后彩”，阈值线 0.1 黑/灰虚线。

## 7. R 实现方案

### 7.1 推荐包
`cobalt::love.plot()`（最省，直接吃 MatchIt/WeightIt 对象）；本机无 cobalt → 手算 SMD + ggplot。

### 7.2 关键参数
长表 `pivot_longer(before/after)` → `geom_point(aes(color=stage)) + geom_line(aes(group=covar)) + geom_vline(0.1)`。

### 7.3 可执行模板
**`templates/r/love.R`**（手算 SMD，免 cobalt/MatchIt）。换数据只改 `d`（covar/before/after 三列），可由 `cobalt::bal.tab` 导出。

## 8. Python 实现方案

### 8.1 推荐包
matplotlib（手绘点线）；SMD 可由自写函数或 `dowhy`/`econml` 配套工具算。

### 8.2 关键参数
按 before 排序 → `scatter(before)` + `scatter(after)` + 灰连线 + `axvline(0.1)`。

### 8.3 可执行模板
**`templates/python/love.py`**。换真实数据：对每个协变量算匹配前后 |SMD| 填入 `smd_before/smd_after`。

## 9. 示例图像

### 9.1 网络优秀示例
参考 `cobalt` 文档的 love.plot 范式（Noah Greifer）。

### 9.2 本库模板 demo（合成数据，双后端对齐）
Python（matplotlib）：

![[tpl_love_py.png]]

R（ggplot2）：

![[tpl_love_r.png]]

> 调整前多个协变量 |SMD| 远超 0.1（最大达 0.51），调整后全部收缩到阈值内 → 两组基线可比；双后端一致。

## 10. 常见错误
- 用 p 值（t 检验/卡方）判平衡——受样本量影响，大样本里微小差异也“显著”，应改用 SMD。
- 只报调整后、不报调整前——无法看出调整的贡献。
- 漏掉交互项/多项式项/样条项的平衡（PS 模型里有就得查）。
- 没画阈值线，读者无从判断“够不够平”。
- SMD 没取绝对值，正负混排难读。

## 11. 自动返修规则
- 缺阈值线 → 自动补 0.1（可选 0.25）。
- 未排序 → 按调整前 |SMD| 降序。
- 只有一组 SMD → 提示补“调整后”或改用 Table 1。
- 检测到用 p 值判平衡 → 提示换 SMD。

## 12. 与其他图表的关系
- 前置 [[倾向评分重叠图_PSOverlap]]：先证重叠（正性）再证平衡，二者缺一不可。
- 后续 [[森林图_ForestPlot]]：平衡达成后报调整后效应(ATE/ATT)的点估计+CI。
- 与 Table 1 互补：表给数值，Love plot 给“前后收缩”的视觉证据。

## 13. 质量检查清单
- [ ] 含 0.1 阈值线？
- [ ] 同时有调整前/后？
- [ ] 按调整前 |SMD| 排序？
- [ ] 纳入了 PS 模型里的全部项（含交互/样条）？
- [ ] 用 SMD 而非 p 值判平衡？

（通用清单见 [[科研图表质量检查清单]]）

## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-06-14 | v0.1 | 建卡 + 双后端可执行模板（手算 SMD，免 cobalt）+ demo 图，状态 tested | 未做多方案对比 | 加多权重方案叠加 + IPTW 后生存曲线联动 |

相关：[[倾向评分重叠图_PSOverlap]] · [[限制性立方样条_RCS]] · [[森林图_ForestPlot]] · [[缺失数据图_Missingness]]
