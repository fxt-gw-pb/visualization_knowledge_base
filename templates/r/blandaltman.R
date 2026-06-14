## Bland-Altman 一致性图（两测量方法）—— 卡片 03_相关性图/BlandAltman一致性图_BlandAltman.md
## 合成两方法测量，均值 vs 差值 + 偏倚 + 95% 一致性界限。 Rscript templates/r/blandaltman.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_blandaltman"; TITLE <- "Bland-Altman agreement"
XLAB <- "Mean of two methods"; YLAB <- "Difference (M1 - M2)"
PT_C <- unname(pal("med_case_control")["low"])
# 换真实数据： m1 <- df$method1; m2 <- df$method2
n <- 150; truth <- rnorm(n, 100, 15)
m1 <- truth + rnorm(n, 0, 4); m2 <- truth + 2 + rnorm(n, 0, 4)
# <<< PARAM ------------------------------------------------------

d <- data.frame(mean = (m1 + m2) / 2, diff = m1 - m2)
bias <- mean(d$diff); s <- sd(d$diff); lo <- bias - 1.96 * s; hi <- bias + 1.96 * s
xr <- max(d$mean); span <- diff(range(d$mean))
labs_df <- data.frame(y = c(bias, hi, lo),
                      lab = c(sprintf("Bias %.1f", bias),
                              sprintf("+1.96SD %.1f", hi), sprintf("-1.96SD %.1f", lo)))
p <- ggplot(d, aes(mean, diff)) +
  geom_hline(yintercept = 0, color = "black", linewidth = .3, alpha = .4) +
  geom_point(color = PT_C, alpha = .6, size = 1.6) +
  geom_hline(yintercept = bias, color = "grey40", linewidth = .5) +
  geom_hline(yintercept = c(lo, hi), color = "grey40", linetype = 2, linewidth = .5) +
  geom_text(data = labs_df, aes(x = xr + span * .01, y = y, label = lab),
            hjust = 0, size = 2.4, color = "grey30", inherit.aes = FALSE) +
  coord_cartesian(xlim = c(min(d$mean), xr + span * .22), clip = "off") +
  labs(x = XLAB, y = YLAB, title = TITLE)
save_gg(p, NAME, w = 100, h = 82)
