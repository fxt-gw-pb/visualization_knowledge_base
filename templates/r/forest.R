## 森林图（forestploter，表格式，log 轴，ref=1）—— 卡片 05_模型结果图/森林图_ForestPlot.md
## 合成 OR 表，可独立运行： Rscript templates/r/forest.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
suppressPackageStartupMessages({ library(forestploter); library(grid) })
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_forest"
CI_COL <- unname(pal("effect_dir")["harm"])   # 点色
# 换真实数据： 由 broom::tidy(glm/coxph, exponentiate=TRUE, conf.int=TRUE) 得 term/estimate/conf.low/conf.high/p.value
res <- data.frame(
  term      = c("Age", "Sex (female)", "Current smoker", "BMI", "Hypertension"),
  estimate  = c(1.8, 0.7, 1.5, 1.05, 2.3),
  conf.low  = c(1.4, 0.55, 1.1, 0.95, 1.7),
  conf.high = c(2.3, 0.9, 2.0, 1.16, 3.1),
  p.value   = c(1e-4, .02, .03, .3, 1e-5))
# <<< PARAM ------------------------------------------------------

res$`OR (95% CI)` <- sprintf("%.2f (%.2f, %.2f)", res$estimate, res$conf.low, res$conf.high)
res$p <- ifelse(res$p.value < .001, "<0.001", sprintf("%.3f", res$p.value))
res$` ` <- paste(rep(" ", 20), collapse = " ")
tm <- forest_theme(base_size = 9, ci_pch = 15, ci_col = CI_COL, refline_col = "grey50")
fp <- forest(res[, c("term", "OR (95% CI)", "p", " ")],
             est = res$estimate, lower = res$conf.low, upper = res$conf.high,
             ci_column = 4, ref_line = 1, xlim = c(0.4, 4), ticks_at = c(0.5, 1, 2, 4),
             x_trans = "log", theme = tm)
save_dev(fp, NAME, w = 180, h = 90)
