#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Framingham MVP 图（Python 后端）。
输出到 科研数据可视化知识库/07_示例图像库/Framingham测试图/ ，每图存 PNG(300dpi)+PDF。
依赖：numpy pandas matplotlib seaborn scikit-learn statsmodels lifelines scipy
数据：data_example/Framingham_data(1)_副本.csv （长格式，PERIOD 1/2/3）
"""
import os, warnings
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import matplotlib as mpl, matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV  = os.path.join(ROOT, "data_example", "Framingham_data(1)_副本.csv")
OUT  = os.path.join(ROOT, "科研数据可视化知识库", "07_示例图像库", "Framingham测试图")
os.makedirs(OUT, exist_ok=True)
np.random.seed(2026)

# ---------- 发表级样式（见 matplotlib通用主题.md） ----------
mpl.rcParams.update({
    "figure.dpi": 120, "savefig.dpi": 300, "pdf.fonttype": 42, "ps.fonttype": 42,
    "font.family": "sans-serif", "font.sans-serif": ["Arial","Helvetica","DejaVu Sans"],
    "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
    "axes.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#ECECEC", "grid.linewidth": 0.5,
    "xtick.direction": "in", "ytick.direction": "in",
    "legend.frameon": False, "savefig.bbox": "tight",
})
OKABE = ["#E69F00","#56B4E9","#009E73","#0072B2","#D55E00","#CC79A7","#F0E442","#999999"]
MED   = {"No HTN":"#0072B2","HTN":"#D55E00"}

def save(fig, name):
    for ext in ("png","pdf"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"))
    plt.close(fig); print("  ->", name)

# ---------- 数据 ----------
df = pd.read_csv(CSV, index_col=0)
df["hyp_f"]   = df.PREVHYP.map({0:"No HTN",1:"HTN"})
df["smoke_f"] = df.CURSMOKE.map({0:"Non-smoker",1:"Smoker"})
df["sex_f"]   = df.SEX.map({0:"Male",1:"Female"})          # 编码已确认：0=男 1=女（4 项证据交叉验证，见 变量字典.md）
SEXPAL = {"Male":"#0072B2","Female":"#D55E00"}            # 性别无好坏，用对等中性两色（色盲安全）
df["age_f"]   = df.AGE_group.map({1:"Age grp 1",2:"Age grp 2",3:"Age grp 3"})
base = df[df.PERIOD==1].copy()
print(f"loaded: {len(df)} rows, baseline {len(base)}")

# ========== 1. 分布：TOTCHOL 直方+密度 ==========
def f_dist():
    fig, ax = plt.subplots(figsize=(3.6,2.9))
    sns.histplot(base.TOTCHOL.dropna(), bins=40, stat="density",
                 color="#56B4E9", edgecolor="white", alpha=.8, ax=ax)
    sns.kdeplot(base.TOTCHOL.dropna(), color="#0072B2", lw=1.6, ax=ax)
    ax.set_xlabel("Total cholesterol (mg/dL)"); ax.set_ylabel("Density")
    ax.set_title("Distribution of total cholesterol (baseline)")
    save(fig, "fig_dist_totchol_py")
f_dist()

# ========== 2. 箱线：BMI by PREVHYP + p ==========
def f_box():
    d = base.dropna(subset=["BMI"])
    fig, ax = plt.subplots(figsize=(3.4,3.1))
    order=["No HTN","HTN"]
    sns.boxplot(data=d, x="hyp_f", y="BMI", order=order, showfliers=False,
                hue="hyp_f", palette=MED, width=.55, linewidth=1, legend=False, ax=ax)
    sns.stripplot(data=d, x="hyp_f", y="BMI", order=order, color="#333333",
                  size=1.3, alpha=.15, ax=ax)
    a=d[d.hyp_f=="No HTN"].BMI; b=d[d.hyp_f=="HTN"].BMI
    p=stats.mannwhitneyu(a,b).pvalue
    y=d.BMI.quantile(.995); ax.plot([0,0,1,1],[y,y*1.02,y*1.02,y],lw=.8,c="k")
    ax.text(.5,y*1.03, "p < 0.001" if p<1e-3 else f"p = {p:.3f}", ha="center", fontsize=8)
    ax.set_xlabel(None); ax.set_ylabel("BMI (kg/m²)")
    ax.set_title("BMI by hypertension status")
    save(fig, "fig_box_prevhyp_bmi_py")
f_box()

# ========== 3. 小提琴：TOTCHOL by SEX (split by smoke) ==========
def f_violin():
    d = base.dropna(subset=["TOTCHOL"])
    fig, ax = plt.subplots(figsize=(3.6,3.0))
    sns.violinplot(data=d, x="sex_f", y="TOTCHOL", hue="smoke_f", split=True,
                   inner="quartile", cut=0, density_norm="width",
                   palette={"Non-smoker":"#0072B2","Smoker":"#D55E00"}, ax=ax)
    ax.set_xlabel(None); ax.set_ylabel("Total cholesterol (mg/dL)")
    ax.set_title("Cholesterol by sex and smoking"); ax.legend(title=None, fontsize=7)
    save(fig, "fig_violin_sex_totchol_py")
f_violin()

# ========== 4. 雨云：BMI by AGE_group (手搓半violin+box+点) ==========
def f_raincloud():
    d = base.dropna(subset=["BMI"]); groups=["Age grp 1","Age grp 2","Age grp 3"]
    fig, ax = plt.subplots(figsize=(3.8,3.2))
    for i,g in enumerate(groups):
        vals=d[d.age_f==g].BMI.values
        # 半小提琴（KDE）
        kde=stats.gaussian_kde(vals); xs=np.linspace(vals.min(),vals.max(),120); ys=kde(xs)
        ys=ys/ys.max()*0.35
        ax.fill_betweenx(xs, i, i+ys, color=OKABE[i], alpha=.5, lw=0)
        # 箱
        q1,med,q3=np.percentile(vals,[25,50,75])
        ax.add_patch(plt.Rectangle((i-0.08,q1),0.16,q3-q1,fill=True,fc="white",ec="k",lw=.8,zorder=3))
        ax.plot([i-0.08,i+0.08],[med,med],c="k",lw=1.2,zorder=4)
        # 雨点
        jit=i-0.18+np.random.uniform(-0.06,0.06,len(vals))
        ax.scatter(jit, vals, s=2, color=OKABE[i], alpha=.2, zorder=2)
    ax.set_xticks(range(3)); ax.set_xticklabels(groups)
    ax.set_ylabel("BMI (kg/m²)"); ax.set_xlabel(None)
    ax.set_title("Raincloud: BMI by age group")
    save(fig, "fig_raincloud_age_bmi_py")
f_raincloud()

# ========== 5. 散点：BMI vs TOTCHOL + 回归 + r ==========
def f_scatter():
    d = base.dropna(subset=["BMI","TOTCHOL"])
    fig, ax = plt.subplots(figsize=(3.5,3.2))
    sns.regplot(data=d, x="BMI", y="TOTCHOL",
                scatter_kws=dict(alpha=.12, s=8, color="#0072B2"),
                line_kws=dict(color="#D55E00", lw=1.6), ax=ax)
    r,p=stats.pearsonr(d.BMI,d.TOTCHOL)
    ax.text(.04,.95,f"r = {r:.2f}\np < 0.001" if p<1e-3 else f"r = {r:.2f}\np = {p:.3f}",
            transform=ax.transAxes, va="top", fontsize=8)
    ax.set_xlabel("BMI (kg/m²)"); ax.set_ylabel("Total cholesterol (mg/dL)")
    ax.set_title("BMI vs cholesterol (baseline)")
    save(fig, "fig_scatter_bmi_totchol_py")
f_scatter()

# ========== 6. 点估计+CI：BMI by AGE_group ==========
def f_pointrange():
    d=base.dropna(subset=["BMI"])
    g=d.groupby("age_f").BMI.agg(["mean","sem","count"]).reset_index()
    g["lo"]=g["mean"]-1.96*g["sem"]; g["hi"]=g["mean"]+1.96*g["sem"]
    fig, ax = plt.subplots(figsize=(3.5,2.6))
    ax.errorbar(g["mean"], range(len(g)), xerr=[g["mean"]-g["lo"],g["hi"]-g["mean"]],
                fmt="o", color="#0072B2", capsize=3, ms=5)
    ax.set_yticks(range(len(g))); ax.set_yticklabels(g["age_f"])
    for i,row in g.iterrows():
        ax.text(g["hi"].max()*1.001, i, f"  n={int(row['count'])}", va="center", fontsize=7, color="grey")
    ax.set_xlabel("Mean BMI (95% CI), kg/m²"); ax.set_ylabel(None)
    ax.set_title("Mean BMI by age group")
    save(fig, "fig_pointrange_age_bmi_py")
f_pointrange()

# ========== 7. 折线趋势：BMI ~ PERIOD by SEX (mean±CI) ==========
def f_line():
    fig, ax = plt.subplots(figsize=(3.8,2.9))
    sns.lineplot(data=df, x="PERIOD", y="BMI", hue="sex_f", errorbar=("ci",95),
                 marker="o", palette=SEXPAL, ax=ax)
    ax.set_xticks([1,2,3]); ax.set_xticklabels(["Exam 1","Exam 2","Exam 3"])
    ax.set_xlabel(None); ax.set_ylabel("Mean BMI (kg/m²)")
    ax.set_title("BMI trend across exams"); ax.legend(title=None, fontsize=8)
    save(fig, "fig_line_bmi_period_py")
f_line()

# ========== 8/9/10 模型：logistic 预测 DEATH ==========
import statsmodels.formula.api as smf
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss
dmod = base.dropna(subset=["BMI","TOTCHOL","GLUCOSE"]).copy()
model = smf.logit("DEATH ~ C(SEX) + BMI + CURSMOKE + PREVHYP + C(AGE_group) + TOTCHOL + GLUCOSE", dmod).fit(disp=0)
dmod["pred"] = model.predict(dmod)

# 8. 森林图（OR）
def f_forest():
    params=model.params; ci=model.conf_int()
    terms=[t for t in params.index if t!="Intercept"]
    labmap={"C(SEX)[T.1]":"Female (vs male)","BMI":"BMI (per unit)","CURSMOKE":"Current smoker",
            "PREVHYP":"Hypertension","C(AGE_group)[T.2]":"Age grp 2","C(AGE_group)[T.3]":"Age grp 3",
            "TOTCHOL":"Total chol (per unit)","GLUCOSE":"Glucose (per unit)"}
    rows=[]
    for t in terms:
        rows.append((labmap.get(t,t), np.exp(params[t]), np.exp(ci.loc[t,0]), np.exp(ci.loc[t,1])))
    rdf=pd.DataFrame(rows, columns=["term","OR","lo","hi"])[::-1].reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(5.2, 0.42*len(rdf)+1.0))
    y=np.arange(len(rdf))
    for i,row in rdf.iterrows():
        c = "#B2182B" if row.lo>1 else ("#2166AC" if row.hi<1 else "#999999")
        ax.plot([row.lo,row.hi],[i,i],c=c,lw=1.4); ax.plot(row.OR,i,"s",c=c,ms=6)
    ax.axvline(1, ls="--", c="grey", lw=.8)
    ax.set_xscale("log"); ax.set_xticks([0.5,1,2,4]); ax.set_xticklabels([0.5,1,2,4])
    ax.set_yticks(y); ax.set_yticklabels(rdf.term); ax.set_ylim(-0.6,len(rdf)-0.4)
    ax.set_xlabel("Odds ratio for death (95% CI)"); ax.grid(False)
    for i,row in rdf.iterrows():
        ax.text(1.02, i+0.30, f"{row.OR:.2f} ({row.lo:.2f}–{row.hi:.2f})",
                transform=ax.get_yaxis_transform(), fontsize=6.5, color="#333")
    ax.set_title("Multivariable logistic model: predictors of death")
    save(fig, "fig_forest_death_or_py")
f_forest()

# 9. ROC + AUC + bootstrap CI
def f_roc():
    y=dmod.DEATH.values; s=dmod.pred.values
    fpr,tpr,_=roc_curve(y,s); auc=roc_auc_score(y,s)
    aucs=[]
    for _ in range(800):
        idx=np.random.randint(0,len(y),len(y))
        if len(np.unique(y[idx]))<2: continue
        aucs.append(roc_auc_score(y[idx],s[idx]))
    lo,hi=np.percentile(aucs,[2.5,97.5])
    fig, ax = plt.subplots(figsize=(3.4,3.4))
    ax.plot(fpr,tpr,color="#0072B2",lw=1.8)
    ax.plot([0,1],[0,1],ls="--",c="grey",lw=.8)
    ax.text(.45,.12,f"AUC = {auc:.3f}\n(95% CI {lo:.3f}–{hi:.3f})",fontsize=8)
    ax.set_xlabel("1 − Specificity"); ax.set_ylabel("Sensitivity"); ax.set_aspect("equal")
    ax.set_title("ROC: predicting death"); ax.grid(False)
    save(fig, "fig_roc_death_py")
f_roc()

# 10. 校准曲线 + Brier
def f_calib():
    y=dmod.DEATH.values; s=dmod.pred.values
    pt,pp=calibration_curve(y,s,n_bins=10,strategy="quantile")
    import statsmodels.api as sm
    lo=sm.nonparametric.lowess(y,s,frac=.6)
    fig, ax = plt.subplots(figsize=(3.4,3.4))
    ax.plot([0,1],[0,1],ls="--",c="grey",lw=.8)
    ax.plot(lo[:,0],lo[:,1],color="#0072B2",lw=1.5,label="loess")
    ax.scatter(pp,pt,color="#D55E00",s=16,zorder=3,label="binned")
    ax.plot(s,np.full(len(s),-0.02),"|",color="k",alpha=.05)
    ax.text(.05,.9,f"Brier = {brier_score_loss(y,s):.3f}",transform=ax.transAxes,fontsize=8)
    ax.set_xlim(-0.03,1); ax.set_ylim(-0.05,1); ax.set_aspect("equal"); ax.grid(False)
    ax.set_xlabel("Predicted probability"); ax.set_ylabel("Observed frequency")
    ax.set_title("Calibration: death model"); ax.legend(fontsize=7)
    save(fig, "fig_calibration_death_py")
f_calib()

# ========== 11. 相关矩阵热图 ==========
def f_heat():
    corr=base[["TOTCHOL","BMI","GLUCOSE","TIMEDTH"]].corr()
    fig, ax = plt.subplots(figsize=(3.4,3.0))
    sns.heatmap(corr, cmap="RdBu_r", center=0, vmin=-1, vmax=1, annot=True, fmt=".2f",
                square=True, linewidths=.5, cbar_kws=dict(shrink=.8), ax=ax)
    ax.set_title("Correlation matrix (baseline)")
    save(fig, "fig_heatmap_corr_py")
f_heat()

# ========== 12. KM by PREVHYP + risk table ==========
def f_km():
    from lifelines import KaplanMeierFitter
    from lifelines.statistics import logrank_test
    from lifelines.plotting import add_at_risk_counts
    fig, ax = plt.subplots(figsize=(4.2,4.2))
    kmfs=[]
    for label,c in [("No HTN","#0072B2"),("HTN","#D55E00")]:
        g=base[base.hyp_f==label]
        kmf=KaplanMeierFitter(label=label); kmf.fit(g.TIMEDTH,g.DEATH)
        kmf.plot_survival_function(ax=ax,ci_show=True,color=c); kmfs.append(kmf)
    m=base.hyp_f=="HTN"
    res=logrank_test(base.TIMEDTH[m],base.TIMEDTH[~m],base.DEATH[m],base.DEATH[~m])
    ax.text(.04,.06,f"log-rank p < 0.001" if res.p_value<1e-3 else f"log-rank p = {res.p_value:.3f}",
            transform=ax.transAxes,fontsize=8)
    add_at_risk_counts(*kmfs, ax=ax)
    ax.set_xlabel("Time (days)"); ax.set_ylabel("Survival probability")
    ax.set_title("Kaplan–Meier by hypertension"); ax.grid(False)
    save(fig, "fig_km_prevhyp_py")
f_km()

# ========== 13. Figure 1 多面板（baseline） ==========
def f_fig1():
    fig=plt.figure(figsize=(7.2,5.4),constrained_layout=True)
    axd=fig.subplot_mosaic([["A","B"],["C","D"]])
    # A 年龄组人数
    base.age_f.value_counts().sort_index().plot(kind="bar",ax=axd["A"],color="#56B4E9",edgecolor="white")
    axd["A"].set_xlabel(None); axd["A"].set_ylabel("Count"); axd["A"].set_title("Age groups",fontsize=9)
    axd["A"].tick_params(axis="x",rotation=0)
    # B BMI by PREVHYP
    sns.boxplot(data=base.dropna(subset=["BMI"]),x="hyp_f",y="BMI",order=["No HTN","HTN"],
                hue="hyp_f",palette=MED,legend=False,showfliers=False,width=.5,ax=axd["B"])
    axd["B"].set_xlabel(None); axd["B"].set_ylabel("BMI (kg/m²)"); axd["B"].set_title("BMI by HTN",fontsize=9)
    # C 吸烟率 by sex（百分比堆叠）
    ct=pd.crosstab(base.sex_f,base.smoke_f,normalize="index")
    ct.plot(kind="bar",stacked=True,ax=axd["C"],color=["#0072B2","#D55E00"],width=.6)
    axd["C"].set_xlabel(None); axd["C"].set_ylabel("Proportion"); axd["C"].set_title("Smoking by sex",fontsize=9)
    axd["C"].tick_params(axis="x",rotation=0); axd["C"].legend(title=None,fontsize=6,loc="lower right")
    # D 相关热图
    sns.heatmap(base[["TOTCHOL","BMI","GLUCOSE"]].corr(),cmap="RdBu_r",center=0,vmin=-1,vmax=1,
                annot=True,fmt=".2f",square=True,cbar=False,ax=axd["D"])
    axd["D"].set_title("Correlations",fontsize=9)
    for k,ax in axd.items():
        ax.text(-0.12,1.06,k,transform=ax.transAxes,fontweight="bold",fontsize=12)
    fig.suptitle("Figure 1. Baseline characteristics (Framingham)",fontsize=11,fontweight="bold")
    save(fig,"fig1_baseline_multipanel_py")
f_fig1()

# ========== 14. Figure 2 多面板（model） ==========
def f_fig2():
    from sklearn.metrics import roc_curve, roc_auc_score
    from lifelines import KaplanMeierFitter
    fig=plt.figure(figsize=(7.2,5.6),constrained_layout=True)
    axd=fig.subplot_mosaic([["A","B"],["C","D"]])
    # A 森林（简版，重画）
    params=model.params; ci=model.conf_int()
    terms=[t for t in params.index if t!="Intercept"]
    rdf=pd.DataFrame([(t,np.exp(params[t]),np.exp(ci.loc[t,0]),np.exp(ci.loc[t,1])) for t in terms],
                     columns=["term","OR","lo","hi"])[::-1].reset_index(drop=True)
    for i,row in rdf.iterrows():
        c="#B2182B" if row.lo>1 else ("#2166AC" if row.hi<1 else "#999999")
        axd["A"].plot([row.lo,row.hi],[i,i],c=c,lw=1.2); axd["A"].plot(row.OR,i,"s",c=c,ms=4)
    axd["A"].axvline(1,ls="--",c="grey",lw=.7); axd["A"].set_xscale("log")
    axd["A"].set_xticks([0.5,1,2,4]); axd["A"].set_xticklabels([0.5,1,2,4])
    axd["A"].set_yticks(range(len(rdf))); axd["A"].set_yticklabels(rdf.term,fontsize=6)
    axd["A"].set_xlabel("OR (95% CI)"); axd["A"].set_title("Predictors of death",fontsize=9); axd["A"].grid(False)
    # B ROC
    y=dmod.DEATH.values; s=dmod.pred.values; fpr,tpr,_=roc_curve(y,s)
    axd["B"].plot(fpr,tpr,color="#0072B2",lw=1.6); axd["B"].plot([0,1],[0,1],ls="--",c="grey",lw=.7)
    axd["B"].text(.4,.1,f"AUC = {roc_auc_score(y,s):.3f}",fontsize=8)
    axd["B"].set_xlabel("1 − Spec"); axd["B"].set_ylabel("Sens"); axd["B"].set_aspect("equal")
    axd["B"].set_title("ROC",fontsize=9); axd["B"].grid(False)
    # C 校准
    pt,pp=calibration_curve(y,s,n_bins=10,strategy="quantile")
    axd["C"].plot([0,1],[0,1],ls="--",c="grey",lw=.7); axd["C"].scatter(pp,pt,color="#D55E00",s=12)
    axd["C"].set_xlabel("Predicted"); axd["C"].set_ylabel("Observed"); axd["C"].set_aspect("equal")
    axd["C"].set_title(f"Calibration (Brier {brier_score_loss(y,s):.3f})",fontsize=9); axd["C"].grid(False)
    # D KM
    for label,c in [("No HTN","#0072B2"),("HTN","#D55E00")]:
        g=base[base.hyp_f==label]; k=KaplanMeierFitter(label=label); k.fit(g.TIMEDTH,g.DEATH)
        k.plot_survival_function(ax=axd["D"],ci_show=False,color=c)
    axd["D"].set_xlabel("Time (days)"); axd["D"].set_ylabel("Survival"); axd["D"].set_title("KM by HTN",fontsize=9)
    axd["D"].legend(fontsize=6); axd["D"].grid(False)
    for k,ax in axd.items():
        ax.text(-0.14,1.06,k,transform=ax.transAxes,fontweight="bold",fontsize=12)
    fig.suptitle("Figure 2. Model performance (death outcome)",fontsize=11,fontweight="bold")
    save(fig,"fig2_model_multipanel_py")
f_fig2()

print("\nALL PYTHON FIGURES DONE ->", OUT)
