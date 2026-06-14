## Meta 分析森林图（逆方差合并 + 权重方块 + 合并菱形 + I²）—— 卡片 14_证据合成图/Meta森林图_MetaForest.md
## 手算 DerSimonian-Laird（免 meta/metafor），ggplot 手绘。 Rscript templates/r/metaforest.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_metaforest"; TITLE <- "Random-effects meta-analysis"; XLAB <- "Odds ratio (95% CI)"
BOX_C <- unname(pal("med_case_control")["low"]); DIA_C <- unname(pal("effect_dir")["harm"])
d <- data.frame(
  study = c("Cohort A 2018", "RCT B 2019", "Registry C 2020", "Cohort D 2021", "RCT E 2023"),
  OR = c(1.62, 1.21, 1.95, 1.10, 1.48),
  lo = c(1.10, 0.88, 1.30, 0.80, 1.05),
  hi = c(2.38, 1.66, 2.92, 1.51, 2.09), stringsAsFactors = FALSE)
# <<< PARAM ------------------------------------------------------

yi <- log(d$OR); sei <- (log(d$hi) - log(d$lo)) / (2 * 1.96); wi <- 1 / sei^2
Q <- sum(wi * (yi - sum(wi * yi) / sum(wi))^2); dfree <- nrow(d) - 1
C <- sum(wi) - sum(wi^2) / sum(wi); tau2 <- max(0, (Q - dfree) / C); I2 <- max(0, (Q - dfree) / Q) * 100
wr <- 1 / (sei^2 + tau2); mu <- sum(wr * yi) / sum(wr); semu <- sqrt(1 / sum(wr))
pool <- c(OR = exp(mu), lo = exp(mu - 1.96 * semu), hi = exp(mu + 1.96 * semu)); d$w <- wr / sum(wr) * 100

d$y <- rev(seq_len(nrow(d))) + 1
XL <- 0.16; XR <- 6.5; hh <- 0.34
diamond <- data.frame(x = c(pool["lo"], pool["OR"], pool["hi"], pool["OR"]), y = c(0, hh, 0, -hh))
labs_l <- rbind(data.frame(y = d$y, lab = d$study, b = FALSE),
                data.frame(y = 0, lab = "Pooled (RE)", b = TRUE))
labs_r <- rbind(data.frame(y = d$y, lab = sprintf("%.2f (%.2f-%.2f)  %.0f%%", d$OR, d$lo, d$hi, d$w), b = FALSE),
                data.frame(y = 0, lab = sprintf("%.2f (%.2f-%.2f)", pool["OR"], pool["lo"], pool["hi"]), b = TRUE))
p <- ggplot() +
  geom_vline(xintercept = 1, linetype = 2, color = "grey50") +
  geom_errorbarh(data = d, aes(y = y, xmin = lo, xmax = hi), height = 0, color = BOX_C, linewidth = .5) +
  geom_point(data = d, aes(y = y, x = OR, size = w), color = BOX_C, shape = 15) +
  geom_polygon(data = diamond, aes(x, y), fill = DIA_C) +
  geom_text(data = labs_l, aes(y = y, x = XL, label = lab, fontface = ifelse(b, "bold", "plain")), hjust = 0, size = 2.6) +
  geom_text(data = labs_r, aes(y = y, x = XR, label = lab, fontface = ifelse(b, "bold", "plain")), hjust = 1, size = 2.4) +
  scale_size(range = c(2, 5), guide = "none") +
  scale_x_log10(limits = c(0.13, 7), breaks = c(0.5, 1, 2), labels = c("0.5", "1", "2")) +
  labs(x = XLAB, y = NULL, title = sprintf("%s  (I² = %.0f%%, tau² = %.3f)", TITLE, I2, tau2)) +
  theme(axis.text.y = element_blank(), axis.ticks.y = element_blank(), panel.grid.major.y = element_blank())
save_gg(p, NAME, w = 145, h = 92)
