## 漏斗图 Funnel plot（发表偏倚）—— 卡片 14_证据合成图/漏斗图_Funnel.md
## 效应量 vs SE（y 反向）+ 合并线 + 伪 95% 漏斗。 Rscript templates/r/funnel.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_funnel"; TITLE <- "Funnel plot"
XLAB <- "log Odds ratio"; YLAB <- "Standard error"
PT_C <- unname(pal("med_case_control")["low"])
k <- 25; mu_true <- 0.3
sei <- runif(k, .05, .45); yi <- rnorm(k, mu_true, sei)
# <<< PARAM ------------------------------------------------------

wi <- 1 / sei^2; mu <- sum(wi * yi) / sum(wi)
seg <- seq(1e-3, max(sei) * 1.05, length.out = 100)
band <- data.frame(se = seg, lo = mu - 1.96 * seg, hi = mu + 1.96 * seg)
p <- ggplot() +
  geom_line(data = band, aes(lo, se), linetype = 2, color = "grey50", linewidth = .4) +
  geom_line(data = band, aes(hi, se), linetype = 2, color = "grey50", linewidth = .4) +
  geom_vline(xintercept = mu, color = "grey50", linewidth = .4) +
  geom_point(data = data.frame(yi = yi, sei = sei), aes(yi, sei),
             color = PT_C, alpha = .75, size = 1.8) +
  scale_y_reverse() +
  labs(x = XLAB, y = YLAB, title = TITLE)
save_gg(p, NAME, w = 100, h = 86)
