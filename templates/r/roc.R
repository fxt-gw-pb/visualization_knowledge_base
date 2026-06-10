## ROC 曲线 + AUC 95%CI（pROC + ggplot）—— 卡片 06_预测模型评价图/ROC曲线_ROC.md
## 合成预测，可独立运行： Rscript templates/r/roc.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
suppressPackageStartupMessages(library(pROC))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_roc"; TITLE <- "ROC curve"; XLAB <- "1 - Specificity"; YLAB <- "Sensitivity"
CURVE <- unname(pal("med_case_control")["low"])
# 换真实数据： y(0/1) 与 pred(预测概率)
n <- 500; y <- rbinom(n, 1, .4); pred <- pmin(pmax(.5 * y + rnorm(n, 0, .4), 0), 1)
# <<< PARAM ------------------------------------------------------

roc_obj <- roc(y, pred, quiet = TRUE); ci_auc <- ci.auc(roc_obj)
roc_df <- data.frame(spec = rev(roc_obj$specificities), sens = rev(roc_obj$sensitivities))
p <- ggplot(roc_df, aes(1 - spec, sens)) +
  geom_abline(slope = 1, intercept = 0, linetype = 2, color = "grey60") +
  geom_path(color = CURVE, linewidth = 1) +
  annotate("text", x = .62, y = .12, size = 2.8,
           label = sprintf("AUC = %.3f\n(95%% CI %.3f-%.3f)", ci_auc[2], ci_auc[1], ci_auc[3])) +
  coord_equal() + labs(x = XLAB, y = YLAB, title = TITLE)
save_gg(p, NAME, w = 88, h = 88)
