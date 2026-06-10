## KM 生存曲线 + risk table + log-rank p（survminer，R 招牌）—— 卡片 07_生存分析图/KM生存曲线_KaplanMeier.md
## 合成生存数据，可独立运行： Rscript templates/r/km.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
suppressPackageStartupMessages({ library(survival); library(survminer) })
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_km"; XLAB <- "Time (days)"; YLAB <- "Survival probability"
PALETTE <- pal("med_case_control"); LEGEND_TITLE <- "Group"
LABS <- c("Low risk", "High risk")
# 换真实数据： df 需含 time / event(1=事件) / group；一行一个体
n <- 150
df <- rbind(
  data.frame(time = rexp(n, .0008), event = rbinom(n, 1, .7), grp = LABS[1]),
  data.frame(time = rexp(n, .0016), event = rbinom(n, 1, .7), grp = LABS[2]))
df$grp <- factor(df$grp, levels = LABS)
# <<< PARAM ------------------------------------------------------

fit <- survfit(Surv(time, event) ~ grp, data = df)
km <- ggsurvplot(fit, data = df, pval = TRUE, conf.int = TRUE, risk.table = TRUE,
                 risk.table.height = .26, censor = FALSE, break.time.by = 2000,
                 palette = c(unname(PALETTE["low"]), unname(PALETTE["high"])),
                 legend.labs = LABS, legend.title = LEGEND_TITLE,
                 xlab = XLAB, ylab = YLAB, ggtheme = theme_pub())
save_dev(km, NAME, w = 120, h = 130)
