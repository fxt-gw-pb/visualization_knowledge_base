#!/usr/bin/env Rscript
## Framingham MVP 图（R 后端）。重点产出 R 擅长的图。
## 输出到 科研数据可视化知识库/07_示例图像库/Framingham测试图/ ，每图 PNG(300dpi)+PDF。
suppressPackageStartupMessages({
  library(readr); library(dplyr); library(forcats); library(ggplot2)
  library(ggpubr); library(ggbeeswarm); library(ggdist)
  library(survival); library(survminer); library(forestploter); library(grid)
  library(pROC); library(pheatmap); library(patchwork); library(broom)
})
set.seed(2026)

ROOT <- "/Users/fpb/Obsidian_Vault/可视化"
OUT  <- file.path(ROOT, "科研数据可视化知识库", "07_示例图像库", "Framingham测试图")
dir.create(OUT, showWarnings = FALSE, recursive = TRUE)

okabe <- c("#E69F00","#56B4E9","#009E73","#0072B2","#D55E00","#CC79A7","#F0E442","#999999")
med   <- c("No HTN"="#0072B2","HTN"="#D55E00")

## 发表级主题
theme_pub <- function(base=9) theme_minimal(base_size=base) +
  theme(panel.grid.minor=element_blank(),
        panel.grid.major=element_line(color="grey92", linewidth=.3),
        axis.line=element_line(color="black", linewidth=.4),
        axis.ticks=element_line(color="black", linewidth=.3),
        plot.title=element_text(face="bold", size=base+1),
        strip.text=element_text(face="bold"), strip.background=element_blank())
theme_set(theme_pub())

save_gg <- function(p, name, w=89, h=72){
  ggsave(file.path(OUT, paste0(name,".pdf")), p, width=w, height=h, units="mm")  # 默认 pdf 设备，无需 X11
  ggsave(file.path(OUT, paste0(name,".png")), p, width=w, height=h, units="mm", dpi=300, bg="white")
  cat("  ->", name, "\n")
}
## 均值±95%CI（替代 Hmisc::mean_cl_normal，避免额外依赖）
mean_ci <- function(x){ x<-x[!is.na(x)]; m<-mean(x); s<-sd(x)/sqrt(length(x))
  data.frame(y=m, ymin=m-1.96*s, ymax=m+1.96*s) }
save_dev <- function(expr, name, w=110, h=120){  # 给 survminer/forestploter/pheatmap
  pdf(file.path(OUT, paste0(name,".pdf")), width=w/25.4, height=h/25.4); print(expr); dev.off()
  png(file.path(OUT, paste0(name,".png")), width=w, height=h, units="mm", res=300, bg="white"); print(expr); dev.off()
  cat("  ->", name, "\n")
}

## 数据
df <- read_csv(file.path(ROOT,"data_example","Framingham_data(1)_副本.csv"), show_col_types=FALSE)[,-1]
df <- df %>% mutate(
  hyp_f   = factor(PREVHYP, labels=c("No HTN","HTN")),
  smoke_f = factor(CURSMOKE, labels=c("Non-smoker","Smoker")),
  sex_f   = factor(SEX, labels=c("Male","Female")),        # 编码已确认：0=男 1=女
  age_f   = factor(AGE_group, labels=c("Age grp 1","Age grp 2","Age grp 3")))
sexpal <- c("Male"="#0072B2","Female"="#D55E00")           # 对等中性两色（色盲安全）
base <- filter(df, PERIOD==1)
cat(sprintf("loaded: %d rows, baseline %d\n", nrow(df), nrow(base)))

## 1. 箱线 BMI by PREVHYP + p（ggpubr）
p1 <- ggplot(filter(base,!is.na(BMI)), aes(hyp_f, BMI, fill=hyp_f)) +
  geom_boxplot(outlier.shape=NA, width=.55, alpha=.85) +
  geom_quasirandom(size=.4, alpha=.12, color="grey25") +
  stat_compare_means(method="wilcox.test", label="p.format", label.x=1.3) +
  scale_fill_manual(values=med) +
  labs(x=NULL, y="BMI (kg/m²)", title="BMI by hypertension status") +
  theme(legend.position="none")
save_gg(p1, "fig_box_prevhyp_bmi_r")

## 2. 雨云 BMI by AGE_group（ggdist）
p2 <- ggplot(filter(base,!is.na(BMI)), aes(age_f, BMI, fill=age_f)) +
  stat_halfeye(adjust=.6, width=.6, justification=-.18, .width=0, point_colour=NA, alpha=.7) +
  geom_boxplot(width=.13, outlier.shape=NA, alpha=.6) +
  geom_quasirandom(width=.08, size=.3, alpha=.12, color="grey25") +
  scale_fill_manual(values=okabe) + coord_flip() +
  labs(x=NULL, y="BMI (kg/m²)", title="Raincloud: BMI by age group") +
  theme(legend.position="none")
save_gg(p2, "fig_raincloud_age_bmi_r", w=100, h=80)

## 3. 折线 BMI~PERIOD by SEX (mean±CI)
p3 <- ggplot(df, aes(PERIOD, BMI, color=sex_f, fill=sex_f)) +
  stat_summary(fun.data=mean_ci, geom="ribbon", alpha=.2, color=NA) +
  stat_summary(fun=mean, geom="line", linewidth=1) +
  stat_summary(fun=mean, geom="point", size=1.6) +
  scale_x_continuous(breaks=1:3, labels=c("Exam 1","Exam 2","Exam 3")) +
  scale_color_manual(values=sexpal) +
  scale_fill_manual(values=sexpal) +
  labs(x=NULL, y="Mean BMI (kg/m²)", color="Sex", fill="Sex", title="BMI trend across exams")
save_gg(p3, "fig_line_bmi_period_r", w=100, h=75)

## 3b. 分布 TOTCHOL 直方+密度
pdist <- ggplot(filter(base,!is.na(TOTCHOL)), aes(TOTCHOL)) +
  geom_histogram(aes(y=after_stat(density)), bins=40, fill="#56B4E9", color="white", alpha=.85) +
  geom_density(color="#0072B2", linewidth=1) +
  labs(x="Total cholesterol (mg/dL)", y="Density", title="Distribution of total cholesterol")
save_gg(pdist, "fig_dist_totchol_r", w=92, h=72)

## 3c. 小提琴 TOTCHOL by SEX（split by smoke 用 dodge 近似）
pviol <- ggplot(filter(base,!is.na(TOTCHOL)), aes(sex_f, TOTCHOL, fill=smoke_f)) +
  geom_violin(scale="width", trim=FALSE, alpha=.7, position=position_dodge(.8)) +
  geom_boxplot(width=.12, outlier.shape=NA, position=position_dodge(.8), alpha=.6, show.legend=FALSE) +
  scale_fill_manual(values=c("Non-smoker"="#0072B2","Smoker"="#D55E00")) +
  labs(x=NULL, y="Total cholesterol (mg/dL)", fill=NULL, title="Cholesterol by sex and smoking") +
  theme(legend.position="bottom")
save_gg(pviol, "fig_violin_sex_totchol_r", w=100, h=82)

## 3d. 点估计+CI BMI by AGE_group（横向 + n 标注）
summ <- filter(base,!is.na(BMI)) %>% group_by(age_f) %>%
  summarise(est=mean(BMI), se=sd(BMI)/sqrt(n()), n=n()) %>%
  mutate(lo=est-1.96*se, hi=est+1.96*se)
ppr <- ggplot(summ, aes(est, age_f)) +
  geom_pointrange(aes(xmin=lo, xmax=hi), color="#0072B2", linewidth=.6, size=.5) +
  geom_text(aes(x=hi, label=paste0("  n=",n)), hjust=0, size=2.6, color="grey40") +
  labs(x="Mean BMI (95% CI), kg/m²", y=NULL, title="Mean BMI by age group")
save_gg(ppr, "fig_pointrange_age_bmi_r", w=92, h=62)

## 4. 散点 BMI vs TOTCHOL + 回归 + r（ggpubr）
p4 <- ggscatter(filter(base,!is.na(BMI)&!is.na(TOTCHOL)), "BMI","TOTCHOL",
                alpha=.12, size=.8, color="#0072B2",
                add="reg.line", add.params=list(color="#D55E00")) +
  stat_cor(method="pearson", label.x.npc="left", label.y.npc="top") +
  labs(x="BMI (kg/m²)", y="Total cholesterol (mg/dL)", title="BMI vs cholesterol") + theme_pub()
save_gg(p4, "fig_scatter_bmi_totchol_r")

## 5. 森林图 DEATH OR（forestploter）—— 完整案例，与 Python 一致
dmod <- filter(base, !is.na(BMI), !is.na(TOTCHOL), !is.na(GLUCOSE))
m <- glm(DEATH ~ sex_f + BMI + smoke_f + hyp_f + age_f + TOTCHOL + GLUCOSE,
         data=dmod, family=binomial)
dmod$pred <- predict(m, type="response")
res <- tidy(m, conf.int=TRUE, exponentiate=TRUE) %>% filter(term!="(Intercept)")
res$term <- recode(res$term, sex_fFemale="Female (vs male)", BMI="BMI (per unit)",
                   smoke_fSmoker="Current smoker", hyp_fHTN="Hypertension",
                   `age_fAge grp 2`="Age grp 2", `age_fAge grp 3`="Age grp 3",
                   TOTCHOL="Total chol (per unit)", GLUCOSE="Glucose (per unit)")
res$`OR (95% CI)` <- sprintf("%.2f (%.2f, %.2f)", res$estimate, res$conf.low, res$conf.high)
res$p <- ifelse(res$p.value<.001,"<0.001", sprintf("%.3f", res$p.value))
res$` ` <- paste(rep(" ",20), collapse=" ")
tm <- forest_theme(base_size=9, ci_pch=15, ci_col="#B2182B", refline_col="grey50")
fp <- forest(res[,c("term","OR (95% CI)","p"," ")],
             est=res$estimate, lower=res$conf.low, upper=res$conf.high,
             ci_column=4, ref_line=1, xlim=c(0.4,4), ticks_at=c(0.5,1,2,4),
             x_trans="log", theme=tm)
save_dev(fp, "fig_forest_death_or_r", w=180, h=90)

## 5b. ROC（pROC）+ AUC 95%CI
roc_obj <- roc(dmod$DEATH, dmod$pred, quiet=TRUE)
ci_auc <- ci.auc(roc_obj)
roc_df <- data.frame(spec=rev(roc_obj$specificities), sens=rev(roc_obj$sensitivities))
proc <- ggplot(roc_df, aes(1-spec, sens)) +
  geom_abline(slope=1, intercept=0, linetype=2, color="grey60") +
  geom_path(color="#0072B2", linewidth=1) +
  annotate("text", x=.62, y=.12,
           label=sprintf("AUC = %.3f\n(95%% CI %.3f-%.3f)", ci_auc[2], ci_auc[1], ci_auc[3]), size=2.8) +
  coord_equal() + labs(x="1 - Specificity", y="Sensitivity", title="ROC: predicting death")
save_gg(proc, "fig_roc_death_r", w=88, h=88)

## 5c. 校准曲线（loess + 分箱点 + Brier）
brier <- mean((dmod$pred - dmod$DEATH)^2)
qbin <- cut(dmod$pred, breaks=quantile(dmod$pred, 0:10/10), include.lowest=TRUE)
binpts <- data.frame(pred=tapply(dmod$pred, qbin, mean),
                     obs =tapply(dmod$DEATH, qbin, mean))
pcal <- ggplot(dmod, aes(pred, DEATH)) +
  geom_abline(slope=1, intercept=0, linetype=2, color="grey60") +
  geom_smooth(method="loess", se=TRUE, color="#0072B2", linewidth=.8) +
  geom_point(data=binpts, aes(pred, obs), color="#D55E00", size=1.8, inherit.aes=FALSE) +
  geom_rug(sides="b", alpha=.05) +
  annotate("text", x=.05, y=.92, hjust=0, label=sprintf("Brier = %.3f", brier), size=2.8) +
  coord_equal(xlim=c(0,1), ylim=c(0,1)) +
  labs(x="Predicted probability", y="Observed frequency", title="Calibration: death model")
save_gg(pcal, "fig_calibration_death_r", w=88, h=88)

## 6. KM by PREVHYP + risk table（survminer，R 招牌）
fit <- survfit(Surv(TIMEDTH, DEATH) ~ hyp_f, data=base)
km <- ggsurvplot(fit, data=base, pval=TRUE, conf.int=TRUE, risk.table=TRUE,
                 risk.table.height=.26, censor=FALSE, break.time.by=2000,
                 palette=unname(med), legend.labs=c("No HTN","HTN"),
                 legend.title="Hypertension", xlab="Time (days)",
                 ylab="Survival probability", ggtheme=theme_pub())
save_dev(km, "fig_km_prevhyp_r", w=120, h=130)

## 7. 相关矩阵热图（pheatmap）
M <- cor(select(base, TOTCHOL, BMI, GLUCOSE, TIMEDTH), use="pairwise.complete.obs")
pheatmap(M, display_numbers=TRUE, number_format="%.2f",
         color=colorRampPalette(c("#2166AC","white","#B2182B"))(100),
         breaks=seq(-1,1,length.out=101), cluster_rows=FALSE, cluster_cols=FALSE,
         main="Correlation matrix (baseline)",
         filename=file.path(OUT,"fig_heatmap_corr_r.pdf"), width=4, height=3.5)
pheatmap(M, display_numbers=TRUE, number_format="%.2f",
         color=colorRampPalette(c("#2166AC","white","#B2182B"))(100),
         breaks=seq(-1,1,length.out=101), cluster_rows=FALSE, cluster_cols=FALSE,
         main="Correlation matrix (baseline)",
         filename=file.path(OUT,"fig_heatmap_corr_r.png"), width=4, height=3.5)
cat("  -> fig_heatmap_corr_r\n")

## 8. Figure 1 多面板（patchwork）
pa <- ggplot(base, aes(age_f, fill=age_f)) + geom_bar(width=.7) +
  scale_fill_manual(values=okabe) + labs(x=NULL,y="Count",title="Age groups") +
  theme(legend.position="none")
pb <- ggplot(filter(base,!is.na(BMI)), aes(hyp_f, BMI, fill=hyp_f)) +
  geom_boxplot(outlier.shape=NA, width=.5) + scale_fill_manual(values=med) +
  labs(x=NULL,y="BMI (kg/m²)",title="BMI by HTN") + theme(legend.position="none")
pc <- ggplot(base, aes(sex_f, fill=smoke_f)) + geom_bar(position="fill", width=.6) +
  scale_fill_manual(values=c("#0072B2","#D55E00")) +
  labs(x=NULL,y="Proportion",fill=NULL,title="Smoking by sex") +
  theme(legend.position="bottom", legend.text=element_text(size=6))
Mlong <- data.frame(Var1=rep(rownames(M), times=ncol(M)),
                    Var2=rep(colnames(M), each=nrow(M)),
                    value=as.vector(M))
pd <- ggplot(Mlong, aes(Var1,Var2,fill=value)) + geom_tile() +
  geom_text(aes(label=sprintf("%.2f",value)), size=2.4) +
  scale_fill_gradient2(low="#2166AC",mid="white",high="#B2182B",midpoint=0,limits=c(-1,1)) +
  labs(x=NULL,y=NULL,title="Correlations") +
  theme(legend.position="none", axis.text.x=element_text(angle=45,hjust=1,size=6))
fig1 <- (pa | pb) / (pc | pd) +
  plot_annotation(title="Figure 1. Baseline characteristics (Framingham, R)",
                  tag_levels="A") & theme(plot.tag=element_text(face="bold"))
save_gg(fig1, "fig1_baseline_multipanel_r", w=180, h=150)

## 9. Figure 2 多面板（patchwork：森林 + ROC + 校准 + KM）
res_o <- res %>% arrange(estimate) %>%
  mutate(term=factor(term, levels=term),
         dir=ifelse(conf.low>1,"harm",ifelse(conf.high<1,"protect","ns")))
pforest <- ggplot(res_o, aes(estimate, term, color=dir)) +
  geom_vline(xintercept=1, linetype=2, color="grey60") +
  geom_pointrange(aes(xmin=conf.low, xmax=conf.high), size=.4) +
  scale_x_log10() +
  scale_color_manual(values=c(harm="#B2182B", ns="#999999", protect="#2166AC")) +
  labs(x="OR (95% CI)", y=NULL, title="Predictors of death") +
  theme(legend.position="none", axis.text.y=element_text(size=7))
fig2 <- (pforest | proc) / (pcal | km$plot) +
  plot_annotation(title="Figure 2. Model performance (death, R)",
                  tag_levels="A") & theme(plot.tag=element_text(face="bold"))
save_gg(fig2, "fig2_model_multipanel_r", w=185, h=165)

cat("\nALL R FIGURES DONE ->", OUT, "\n")
