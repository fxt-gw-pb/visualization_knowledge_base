---
title: Python 测试记录
type: test-log
status: active
backend: python
updated: 2026-06-10
tags: [dataviz, framingham, python, test]
---

# Python 测试记录

> 每个 Python 跑图测试一节，套用统一模板。⏳ = 待跑。
> 数据：`可视化/data_example/Framingham_data(1)_副本.csv`。

## 0. 环境与数据载入（所有测试共用）

```python
import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
import statsmodels.formula.api as smf
from sklearn.metrics import RocCurveDisplay, roc_auc_score
# set_pub_style() 见 [[matplotlib通用主题]]

df = pd.read_csv("data_example/Framingham_data(1)_副本.csv", index_col=0)
df["smoke_f"] = df.CURSMOKE.map({0:"Non-smoker",1:"Smoker"})
df["hyp_f"]   = df.PREVHYP.map({0:"No HTN",1:"HTN"})
df["sex_f"]   = df.SEX.map({0:"Male",1:"Female"})  # 编码已确认：0=男 1=女
base = df[df.PERIOD==1].copy()
np.random.seed(2026)
```

> ✅ **已执行（2026-06-10）**。完整生产脚本是 `可视化/scripts/framingham_figs.py`（14 图）；本文件保留作分节说明与可复制片段。
> 环境：conda `viz` → `/opt/anaconda3/envs/viz/bin/python`。运行：`/opt/anaconda3/envs/viz/bin/python scripts/framingham_figs.py`。
> 输出图存 `07_示例图像库/Framingham测试图/`（PNG 300dpi + PDF），已内嵌各卡片第 9.2 节。

---

## 测试模板（复制用）

```markdown
## 测试 N：<图名>
### 数据字段 / 图表目标
### Python 实现（代码块）
### 输出图像
### 质量检查
- [ ] 类型合适 / 配色合理 / 坐标轴清楚 / 图例清楚 / 导出合格 / 可用于论文
### 发现的问题 / 返修记录
```

---

## 测试 1：PREVHYP × BMI 箱线图 ⭐ ⏳
```python
fig, ax = plt.subplots(figsize=(3.5,3))
order = ["No HTN","HTN"]
sns.boxplot(data=base, x="hyp_f", y="BMI", order=order, showfliers=False,
            palette={"No HTN":"#0072B2","HTN":"#D55E00"}, width=.55, ax=ax)
sns.stripplot(data=base, x="hyp_f", y="BMI", order=order,
              color="#333", size=1.5, alpha=.2, ax=ax)
ax.set_xlabel(None); ax.set_ylabel("BMI (kg/m²)")
fig.savefig("07_示例图像库/Framingham测试图/fig_box_prevhyp_bmi_py_v1.pdf", bbox_inches="tight")
```
⏳ 待跑。关联 [[箱线图_Boxplot]]。

---

## 测试 2：相关矩阵热图 ⭐ ⏳
```python
corr = base[["TOTCHOL","BMI","GLUCOSE","TIMEDTH"]].corr()
fig, ax = plt.subplots(figsize=(3.5,3))
sns.heatmap(corr, cmap="RdBu_r", center=0, vmin=-1, vmax=1,
            annot=True, fmt=".2f", square=True, ax=ax)
fig.savefig("07_示例图像库/Framingham测试图/fig_heatmap_corr_py_v1.pdf", bbox_inches="tight")
```
⏳ 待跑。关联 [[热图_Heatmap]]。

---

## 测试 3：BMI ~ PERIOD 趋势 ⭐ ⏳
```python
fig, ax = plt.subplots(figsize=(4,3))
sns.lineplot(data=df, x="PERIOD", y="BMI", hue="sex_f",
             errorbar=("ci",95), marker="o", ax=ax)
ax.set_xticks([1,2,3]); ax.set_xticklabels(["Exam 1","Exam 2","Exam 3"])
ax.set_xlabel(None); ax.set_ylabel("Mean BMI (kg/m²)")
fig.savefig("07_示例图像库/Framingham测试图/fig_line_bmi_period_py_v1.pdf", bbox_inches="tight")
```
⏳ 待跑。关联 [[折线趋势图_Line]]。

---

## 测试 4：DEATH logistic + ROC ⭐ ⏳
```python
d = base.dropna(subset=["BMI","TOTCHOL","GLUCOSE"])
m = smf.logit("DEATH ~ C(SEX) + BMI + CURSMOKE + PREVHYP + C(AGE_group) + TOTCHOL", d).fit()
d["pred"] = m.predict(d)
fig, ax = plt.subplots(figsize=(3.5,3.5))
RocCurveDisplay.from_predictions(d.DEATH, d.pred, name="logistic", ax=ax)
ax.plot([0,1],[0,1], ls="--", c="grey"); ax.set_aspect("equal")
ax.set_xlabel("1 − Specificity"); ax.set_ylabel("Sensitivity")
fig.savefig("07_示例图像库/Framingham测试图/fig_roc_death_py_v1.pdf", bbox_inches="tight")
# OR 表 → 森林图： np.exp(m.params), m.conf_int() 取 exp（见 森林图_ForestPlot）
```
⏳ 待跑。**注意**：同数据训练+评价仅演示流程；正式用 hold-out/CV（[[ROC曲线_ROC]]）。

---

## 测试 5：PREVHYP KM ⭐ ⏳
```python
fig, ax = plt.subplots(figsize=(4,4))
kmfs=[]
for label,g in base.groupby("hyp_f"):
    kmf = KaplanMeierFitter(label=label)
    kmf.fit(g.TIMEDTH, g.DEATH); kmf.plot_survival_function(ax=ax, ci_show=True)
    kmfs.append(kmf)
from lifelines.plotting import add_at_risk_counts
add_at_risk_counts(*kmfs, ax=ax)
ax.set_xlabel("Time (days)"); ax.set_ylabel("Survival probability")
m_ = base.hyp_f=="HTN"
res = logrank_test(base.TIMEDTH[m_], base.TIMEDTH[~m_], base.DEATH[m_], base.DEATH[~m_])
ax.text(.05,.05, f"log-rank p = {res.p_value:.3g}", transform=ax.transAxes)
fig.savefig("07_示例图像库/Framingham测试图/fig_km_prevhyp_py_v1.pdf", bbox_inches="tight")
```
⏳ 待跑。关联 [[KM生存曲线_KaplanMeier]]。

---

相关：[[可测试图表任务清单]] · [[R测试记录]] · [[测试结论与返修记录]] · [[变量字典]]
