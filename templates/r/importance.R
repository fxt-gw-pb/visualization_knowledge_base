## 特征重要性（置换重要性，glm + AUC 下降）—— 卡片 05_模型结果图/特征重要性图_FeatureImportance.md
## R 端用 base glm + pROC 置换重要性（无 RF 包依赖）；Python 端旗舰是 SHAP beeswarm。
## 合成 EHR 数据，可独立运行： Rscript templates/r/importance.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
suppressPackageStartupMessages(library(pROC))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_importance"; TITLE <- "Permutation importance (AUC drop)"
XLAB <- "Mean AUC decrease"; BAR <- unname(pal("med_case_control")["low"])
N_REP <- 10
# 换真实数据： df 含结局 y(0/1) + 数值特征列
n <- 800
df <- data.frame(Age = rnorm(n, 60, 12), BMI = rnorm(n, 27, 4), SBP = rnorm(n, 135, 18),
                 Glucose = rnorm(n, 105, 25), HbA1c = rnorm(n, 6, 1), LDL = rnorm(n, 120, 30),
                 eGFR = rnorm(n, 80, 20), Smoker = rbinom(n, 1, .3))
lp <- 0.04*(df$Age-60) + 0.06*(df$Glucose-105) + 1.2*df$Smoker - 0.02*(df$eGFR-80)
df$y <- rbinom(n, 1, plogis(lp))
# <<< PARAM ------------------------------------------------------

fit <- glm(y ~ ., data = df, family = binomial)
base_auc <- as.numeric(auc(df$y, predict(fit, type = "response"), quiet = TRUE))
feats <- setdiff(names(df), "y")
imp <- sapply(feats, function(f){
  drops <- replicate(N_REP, { d2 <- df; d2[[f]] <- sample(d2[[f]])
    base_auc - as.numeric(auc(df$y, predict(fit, newdata = d2, type = "response"), quiet = TRUE)) })
  mean(drops) })
bar_df <- data.frame(feat = factor(feats, levels = feats[order(imp)]), imp = as.numeric(imp))
p <- ggplot(bar_df, aes(imp, feat)) +
  geom_col(fill = BAR, width = .7) +
  labs(x = XLAB, y = NULL, title = TITLE)
save_gg(p, NAME, w = 95, h = 80)
