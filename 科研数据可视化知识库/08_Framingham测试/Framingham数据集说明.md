---
title: Framingham 数据集说明
type: dataset-doc
status: active
updated: 2026-06-10
tags: [dataviz, framingham, dataset]
---

# Framingham 数据集说明

> 本库测试区用的数据集说明。**以实际 CSV 为准**（不是 prompt 第九节假设的经典教学版）。

## 1. 数据来源与文件

- 文件：`可视化/data_example/Framingham_data(1)_副本.csv`
- 背景：Framingham Heart Study（弗雷明汉心脏研究）——经典心血管流行病学队列。本 CSV 是其**纵向教学子集**（变量经过裁剪/重编码）。
- 规模：**11168 行 × 12 列**；**4215 名受试者**；每人最多 3 个随访期。

> [!important] 数据不随本（公开）仓库分发
> 这是真实人群的健康记录，且其公开再分发许可不明确，因此**已从 git 追踪与历史中移除**（`data_example/*.csv` 列入 `.gitignore`）。
> - 你**本地仍保留**该文件，复现脚本照常可跑。
> - 他人复现：需自行获取数据并放到 `data_example/Framingham_data(1)_副本.csv`。原始 Framingham 数据须经 [BioLINCC](https://biolincc.nhlbi.nih.gov/studies/framcohort/) / dbGaP 申请并签数据使用协议（DUA）；教学子集常见于公开课程材料，使用前请自行确认其许可。
> - 不依赖真实数据也能用：`templates/` 全部用**合成数据**，可直接出范式图。

## 2. 关键结构特征（务必先理解）

### 2.1 长格式（long format）
- 每个受试者（`RANDID`）有多行，每行对应一个体检随访期 `PERIOD`：
  - PERIOD=1：4215 行（基线，每人都有）
  - PERIOD=2：3777 行
  - PERIOD=3：3176 行
- **作图/建模前必须决定**：用基线（`PERIOD==1`）截面，还是全随访纵向。
  - 截面分析（分布、组间、相关、logistic、生存）→ 多用 **基线 `PERIOD==1`**。
  - 纵向趋势（BMI 随访变化、spaghetti）→ 用全部 3 期（[[折线趋势图_Line]]）。

### 2.2 结局变量是“每人固定”的
- `DEATH`、`TIMEDTH` 是受试者级结局（随访期内重复出现同值），不是每期独立事件。
- 生存分析（[[KM生存曲线_KaplanMeier]]）需**每人取一条记录**（如 PERIOD==1）构造 `Surv(TIMEDTH, DEATH)`。

## 3. 变量总览（详见 [[变量字典]]）

| 变量 | 类型 | 含义（按命名推断）|
|---|---|---|
| RANDID | id | 受试者随机编号 |
| SEX | 二分类(0/1) | 性别：**0=Male，1=Female**（已由数据 4 项证据确认，见 [[变量字典]]）|
| TOTCHOL | 连续 | 总胆固醇 (mg/dL) |
| CURSMOKE | 二分类(0/1) | 当前是否吸烟 |
| BMI | 连续 | 体质指数 (kg/m²) |
| GLUCOSE | 连续 | 血糖 (mg/dL) |
| PREVHYP | 二分类(0/1) | 是否既往/患高血压（prevalent hypertension）|
| PERIOD | 有序(1/2/3) | 随访期 |
| DEATH | 二分类(0/1) | 随访结束前是否死亡 |
| TIMEDTH | 时间(天) | 到死亡/删失时间 |
| AGE_group | 有序(1/2/3) | 年龄组（**分组阈值待确认**）|

> ⚠️ 第一列是无名行号（CSV 首列空表头），导入时忽略。

## 4. 适合做什么

| 分析 | 适合度 | 说明 |
|---|---|---|
| 分布图 | ✅ 高 | TOTCHOL/BMI/GLUCOSE 连续变量 |
| 组间比较 | ✅ 高 | 按 SEX/CURSMOKE/PREVHYP/AGE_group 比连续指标 |
| 相关性 | ✅ 中 | TOTCHOL/BMI/GLUCOSE 间相关（变量数偏少）|
| 时间趋势 | ✅ 高 | 长格式 3 期，BMI/TOTCHOL 随 PERIOD 变化（天然适配）|
| 模型结果（OR/HR）| ✅ 高 | logistic 预测 DEATH/PREVHYP；Cox 预测死亡 |
| 预测评价（ROC/校准）| ✅ 中 | 预测 DEATH，但预测变量较少，AUC 别期望太高 |
| 生存分析 | ✅ 高 | TIMEDTH + DEATH，按组画 KM |
| 高维/组学 | ⚠️ 低 | 变量太少，热图只能做小相关矩阵 |

## 5. 缺失值情况（全数据）

| 变量 | 缺失行数 | 占比 |
|---|---|---|
| GLUCOSE | 1393 | ~12.5%（最高）|
| TOTCHOL | 400 | ~3.6% |
| BMI | 48 | ~0.4% |
| 其余 | 0 | — |

- 缺失处理：作图前明确是**完整案例**还是**填补**；GLUCOSE 缺失较多，相关/建模注意 `use="pairwise"` 或多重填补。
- 可视化缺失模式：R `naniar`/`VIM`，Python `missingno`（见 [[Python绘图资源索引]]）。

## 6. 待确认事项（给数据提供者）

1. ✅ **SEX 编码方向 — 已解决**：0=Male，1=Female（数据 4 项证据交叉验证，见 [[变量字典]]）。
2. **AGE_group 分界**：1/2/3 对应的年龄区间（如 <50 / 50–60 / >60？）。基线分布：组1=3057、组2=1050、组3=108。⏳ 仍待确认。
3. **单位确认**：TOTCHOL/GLUCOSE 是否 mg/dL；TIMEDTH 是否“天”（按命名与数值范围高度可能，仍建议确认）。
4. **PREVHYP 定义**：prevalent（既往患病）还是随访新发。

> 不确定项在图注里如实标注，不臆测。SEX 已可放心标 Male/Female。

相关：[[变量字典]] · [[可测试图表任务清单]] · [[数据可视化知识库总览]]
