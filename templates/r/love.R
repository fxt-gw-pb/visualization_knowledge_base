## 协变量平衡 Love plot（PSM/IPTW 前后 |SMD|）—— 卡片 13_因果推断图/协变量平衡图_LovePlot.md
## 合成 SMD，手算对照（免 cobalt/MatchIt）。 Rscript templates/r/love.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
suppressPackageStartupMessages({ library(tidyr) })
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_love"; TITLE <- "Covariate balance (Love plot)"
XLAB <- "Absolute standardized mean difference"; THRESH <- 0.1
C_BEFORE <- unname(pal("effect_dir")["ns"]); C_AFTER <- unname(pal("med_case_control")["low"])
# 换真实数据： 每个协变量匹配前/后 |SMD|（cobalt::bal.tab 或手算）
d <- data.frame(
  covar  = c("Age","BMI","Total cholesterol","Glucose","Smoking","Hypertension","Sex"),
  before = c(0.42, 0.31, 0.28, 0.51, 0.22, 0.37, 0.05),
  after  = c(0.06, 0.04, 0.08, 0.05, 0.07, 0.03, 0.02))
# <<< PARAM ------------------------------------------------------

d <- d[order(d$before), ]; d$covar <- factor(d$covar, levels = d$covar)
dl <- pivot_longer(d, c(before, after), names_to = "stage", values_to = "smd")
dl$stage <- factor(dl$stage, levels = c("before", "after"),
                   labels = c("Before matching", "After matching"))
p <- ggplot(dl, aes(smd, covar)) +
  geom_line(aes(group = covar), color = "grey80", linewidth = .5) +
  geom_point(aes(color = stage), size = 2.4) +
  geom_vline(xintercept = THRESH, linetype = 2, color = "grey50") +
  scale_color_manual(values = c("Before matching" = C_BEFORE, "After matching" = C_AFTER)) +
  expand_limits(x = 0) +
  labs(x = XLAB, y = NULL, color = NULL, title = TITLE) +
  theme(legend.position = c(.82, .16), legend.background = element_rect(fill = "white", color = NA))
save_gg(p, NAME, w = 110, h = 82)
