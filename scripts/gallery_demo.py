#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例图库 demo —— 每种图类型一张“教科书级”范式图，用合成数据生成，license 完全干净
（基于各开源 gallery 的通用画法思路重绘，非抓取网络图片）。
输出 PNG(200dpi) 到 07_示例图像库/示例图库demo/，供示例卡片内嵌作参考范式。
"""
import os, warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import matplotlib as mpl, matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,"科研数据可视化知识库","07_示例图像库","示例图库demo")
os.makedirs(OUT,exist_ok=True); np.random.seed(7)
mpl.rcParams.update({"figure.dpi":110,"savefig.dpi":200,"font.size":9,
    "font.family":"sans-serif","font.sans-serif":["Arial","DejaVu Sans"],
    "axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,
    "grid.color":"#EEEEEE","grid.linewidth":.5,"xtick.direction":"in",
    "ytick.direction":"in","legend.frameon":False,"savefig.bbox":"tight"})
OK=["#E69F00","#56B4E9","#009E73","#0072B2","#D55E00","#CC79A7"]
def save(fig,n): fig.savefig(os.path.join(OUT,n+".png")); plt.close(fig); print("  ->",n)

# 合成数据
N=200
g3=pd.DataFrame({"grp":np.repeat(["A","B","C"],N),
    "val":np.concatenate([np.random.normal(0,1,N),np.random.normal(.8,1.2,N),
                          np.concatenate([np.random.normal(-.5,.5,N//2),np.random.normal(2,.6,N-N//2)])])})

# 1 boxplot demo
def d_box():
    fig,ax=plt.subplots(figsize=(3.4,2.9))
    sns.boxplot(data=g3,x="grp",y="val",hue="grp",palette=OK[:3],legend=False,showfliers=False,width=.55,ax=ax)
    sns.stripplot(data=g3,x="grp",y="val",color="#333",size=2,alpha=.25,ax=ax)
    ax.set_title("Boxplot + jittered points"); ax.set_xlabel(None); ax.set_ylabel("Value")
    save(fig,"demo_boxplot")
d_box()

# 2 violin demo
def d_violin():
    fig,ax=plt.subplots(figsize=(3.4,2.9))
    sns.violinplot(data=g3,x="grp",y="val",hue="grp",palette=OK[:3],legend=False,inner="box",cut=0,ax=ax)
    ax.set_title("Violin (shows bimodality in C)"); ax.set_xlabel(None); ax.set_ylabel("Value")
    save(fig,"demo_violin")
d_violin()

# 3 raincloud demo
def d_rain():
    fig,ax=plt.subplots(figsize=(3.8,3.0)); groups=["A","B","C"]
    for i,gname in enumerate(groups):
        v=g3[g3.grp==gname].val.values
        k=stats.gaussian_kde(v); xs=np.linspace(v.min(),v.max(),120); ys=k(xs); ys=ys/ys.max()*.35
        ax.fill_betweenx(xs,i,i+ys,color=OK[i],alpha=.5,lw=0)
        q1,m,q3=np.percentile(v,[25,50,75])
        ax.add_patch(plt.Rectangle((i-.07,q1),.14,q3-q1,fill=True,fc="white",ec="k",lw=.8,zorder=3))
        ax.plot([i-.07,i+.07],[m,m],c="k",lw=1.2,zorder=4)
        ax.scatter(i-.17+np.random.uniform(-.05,.05,len(v)),v,s=3,color=OK[i],alpha=.25,zorder=2)
    ax.set_xticks(range(3)); ax.set_xticklabels(groups); ax.set_ylabel("Value"); ax.set_xlabel(None)
    ax.set_title("Raincloud (cloud + box + rain)")
    save(fig,"demo_raincloud")
d_rain()

# 4 scatter + reg demo
def d_scatter():
    x=np.random.normal(0,1,400); y=1.2*x+np.random.normal(0,1,400)
    fig,ax=plt.subplots(figsize=(3.4,3.0))
    sns.regplot(x=x,y=y,scatter_kws=dict(alpha=.3,s=12,color="#0072B2"),line_kws=dict(color="#D55E00"),ax=ax)
    r,_=stats.pearsonr(x,y); ax.text(.05,.92,f"r = {r:.2f}",transform=ax.transAxes,fontsize=9)
    ax.set_title("Scatter + regression"); ax.set_xlabel("x"); ax.set_ylabel("y")
    save(fig,"demo_scatter")
d_scatter()

# 5 line trend + CI band
def d_line():
    t=np.arange(0,10);
    rows=[]
    for s,base,col in [("Group 1",0,"#0072B2"),("Group 2",2,"#D55E00")]:
        for r in range(30):
            rows+= [(s,ti, base+0.4*ti+np.random.normal(0,1.2)) for ti in t]
    d=pd.DataFrame(rows,columns=["grp","t","y"])
    fig,ax=plt.subplots(figsize=(3.7,2.8))
    sns.lineplot(data=d,x="t",y="y",hue="grp",errorbar=("ci",95),marker="o",
                 palette={"Group 1":"#0072B2","Group 2":"#D55E00"},ax=ax)
    ax.set_title("Mean ± 95% CI trend"); ax.set_xlabel("Time"); ax.set_ylabel("Value"); ax.legend(title=None,fontsize=8)
    save(fig,"demo_line")
d_line()

# 6 pointrange / coefficient
def d_pointrange():
    terms=["X1","X2","X3","X4","X5"]; est=np.array([.8,-.3,.1,-.6,.4]); se=np.array([.15,.2,.18,.12,.25])
    order=np.argsort(est); est,se=est[order],se[order]; terms=[terms[i] for i in order]
    fig,ax=plt.subplots(figsize=(3.4,2.6)); y=np.arange(len(terms))
    cols=["#B2182B" if e-1.96*s>0 else ("#2166AC" if e+1.96*s<0 else "#999999") for e,s in zip(est,se)]
    for i in range(len(terms)):
        ax.plot([est[i]-1.96*se[i],est[i]+1.96*se[i]],[i,i],c=cols[i],lw=1.4); ax.plot(est[i],i,"o",c=cols[i],ms=5)
    ax.axvline(0,ls="--",c="grey",lw=.8); ax.set_yticks(y); ax.set_yticklabels(terms); ax.grid(False)
    ax.set_xlabel("Coefficient (95% CI)"); ax.set_title("Dot-and-whisker (ref line at 0)")
    save(fig,"demo_pointrange")
d_pointrange()

# 7 forest (OR)
def d_forest():
    terms=["Age","Sex","Smoking","BMI","Hypertension"]; OR=np.array([1.8,0.7,1.5,1.05,2.3])
    lo=np.array([1.4,0.55,1.1,0.95,1.7]); hi=np.array([2.3,0.9,2.0,1.16,3.1])
    fig,ax=plt.subplots(figsize=(4.4,2.7)); y=np.arange(len(terms))[::-1]
    for i in range(len(terms)):
        c="#B2182B" if lo[i]>1 else ("#2166AC" if hi[i]<1 else "#999999")
        ax.plot([lo[i],hi[i]],[y[i],y[i]],c=c,lw=1.4); ax.plot(OR[i],y[i],"s",c=c,ms=6)
    ax.axvline(1,ls="--",c="grey",lw=.8); ax.set_xscale("log"); ax.set_xticks([0.5,1,2,4]); ax.set_xticklabels([0.5,1,2,4])
    ax.set_yticks(y); ax.set_yticklabels(terms); ax.grid(False); ax.set_xlabel("Odds ratio (95% CI)")
    ax.set_title("Forest plot (log axis, ref=1)")
    save(fig,"demo_forest")
d_forest()

# 8 KM
def d_km():
    from lifelines import KaplanMeierFitter
    fig,ax=plt.subplots(figsize=(3.6,3.0))
    for label,c,hz in [("Treatment","#0072B2",.0008),("Control","#D55E00",.0016)]:
        T=np.random.exponential(1/hz,150); E=(np.random.rand(150)<.7).astype(int)
        KaplanMeierFitter(label=label).fit(T,E).plot_survival_function(ax=ax,ci_show=True,color=c)
    ax.set_title("Kaplan–Meier curves"); ax.set_xlabel("Time"); ax.set_ylabel("Survival probability")
    ax.grid(False); ax.legend(fontsize=8)
    save(fig,"demo_km")
d_km()

# 9 ROC
def d_roc():
    from sklearn.metrics import roc_curve,roc_auc_score
    n=500; y=np.random.binomial(1,.4,n); s=np.clip(.5*y+np.random.normal(0,.4,n),0,1)
    fpr,tpr,_=roc_curve(y,s); auc=roc_auc_score(y,s)
    fig,ax=plt.subplots(figsize=(3.2,3.2)); ax.plot(fpr,tpr,color="#0072B2",lw=1.8)
    ax.plot([0,1],[0,1],ls="--",c="grey",lw=.8); ax.text(.45,.12,f"AUC = {auc:.2f}",fontsize=9)
    ax.set_aspect("equal"); ax.grid(False); ax.set_xlabel("1 − Specificity"); ax.set_ylabel("Sensitivity")
    ax.set_title("ROC curve")
    save(fig,"demo_roc")
d_roc()

# 10 calibration
def d_calib():
    from sklearn.calibration import calibration_curve
    n=2000; p=np.random.beta(2,3,n); y=np.random.binomial(1,p)
    pt,pp=calibration_curve(y,p,n_bins=10,strategy="quantile")
    fig,ax=plt.subplots(figsize=(3.2,3.2)); ax.plot([0,1],[0,1],ls="--",c="grey",lw=.8)
    ax.plot(pp,pt,"o-",color="#0072B2"); ax.plot(p,np.full(n,-.02),"|",color="k",alpha=.03)
    ax.set_xlim(-.03,1); ax.set_ylim(-.05,1); ax.set_aspect("equal"); ax.grid(False)
    ax.set_xlabel("Predicted probability"); ax.set_ylabel("Observed frequency"); ax.set_title("Calibration curve")
    save(fig,"demo_calibration")
d_calib()

# 11 heatmap (correlation)
def d_heat():
    d=pd.DataFrame(np.random.randn(200,6),columns=list("ABCDEF"))
    d["B"]+=.8*d["A"]; d["E"]-=.6*d["D"]
    fig,ax=plt.subplots(figsize=(3.2,2.9))
    sns.heatmap(d.corr(),cmap="RdBu_r",center=0,vmin=-1,vmax=1,annot=True,fmt=".2f",square=True,
                cbar_kws=dict(shrink=.8),ax=ax)
    ax.set_title("Correlation heatmap")
    save(fig,"demo_heatmap")
d_heat()

# 12 multipanel
def d_multi():
    fig,axd=plt.subplots(2,2,figsize=(6.4,4.8)); axd=axd.ravel()
    sns.boxplot(data=g3,x="grp",y="val",hue="grp",palette=OK[:3],legend=False,showfliers=False,ax=axd[0]); axd[0].set_title("A  Distribution",loc="left",fontweight="bold")
    x=np.random.randn(200); axd[1].scatter(x,1.2*x+np.random.randn(200),s=8,alpha=.4,color="#0072B2"); axd[1].set_title("B  Relationship",loc="left",fontweight="bold")
    terms=["X1","X2","X3"]; OR=[1.8,.7,1.3]; lo=[1.4,.55,.9]; hi=[2.3,.9,1.9]
    for i in range(3):
        c="#B2182B" if lo[i]>1 else ("#2166AC" if hi[i]<1 else "#999999")
        axd[2].plot([lo[i],hi[i]],[i,i],c=c); axd[2].plot(OR[i],i,"s",c=c,ms=5)
    axd[2].axvline(1,ls="--",c="grey"); axd[2].set_xscale("log"); axd[2].set_yticks(range(3)); axd[2].set_yticklabels(terms); axd[2].set_title("C  Model",loc="left",fontweight="bold")
    from sklearn.metrics import roc_curve
    yy=np.random.binomial(1,.4,400); ss=np.clip(.5*yy+np.random.normal(0,.4,400),0,1); f,t,_=roc_curve(yy,ss)
    axd[3].plot(f,t,color="#0072B2"); axd[3].plot([0,1],[0,1],ls="--",c="grey"); axd[3].set_title("D  Evaluation",loc="left",fontweight="bold")
    for a in axd: a.grid(False)
    fig.suptitle("Multi-panel figure (A/B/C/D)",fontweight="bold"); fig.tight_layout()
    save(fig,"demo_multipanel")
d_multi()

print("\nGALLERY DEMOS DONE ->",OUT)
