## 限制性立方样条 RCS 剂量反应（非线性 OR + 95%CI 带）—— 卡片 13_因果推断图/限制性立方样条_RCS.md
## base splines::ns + glm（免 rms），相对参考点求 OR。 Rscript templates/r/rcs.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
suppressPackageStartupMessages(library(splines))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_rcs"; TITLE <- "RCS dose-response"
XLAB <- "Exposure"; YLAB <- "Odds ratio (95% CI)"
KNOT_Q <- c(.05, .35, .65, .95)       # 4 节点位置（Harrell 推荐分位）
LINE_C <- unname(pal("med_case_control")["low"]); BAND_C <- LINE_C
# 换真实数据： x <- df$exposure; y <- df$outcome（0/1）
n <- 1500; x <- rnorm(n)
y <- rbinom(n, 1, plogis(0.4 * x^2 - 0.3 * x - 0.5))   # J 形真实关系
REF <- median(x)                      # 参考点（OR=1）
# <<< PARAM ------------------------------------------------------

knots <- quantile(x, KNOT_Q); bk <- knots[c(1, length(knots))]; ik <- knots[-c(1, length(knots))]
fit <- glm(y ~ ns(x, knots = ik, Boundary.knots = bk), family = binomial)
grid <- seq(quantile(x, .01), quantile(x, .99), length.out = 200)
mm  <- model.matrix(~ ns(grid, knots = ik, Boundary.knots = bk))
mmr <- model.matrix(~ ns(REF,  knots = ik, Boundary.knots = bk))
ct <- sweep(mm, 2, mmr, "-")          # 相对参考点的对比（截距相消）
lp <- as.vector(ct %*% coef(fit))
se <- sqrt(rowSums((ct %*% vcov(fit)) * ct))
d <- data.frame(x = grid, OR = exp(lp), lo = exp(lp - 1.96 * se), hi = exp(lp + 1.96 * se))
p <- ggplot(d, aes(x, OR)) +
  geom_ribbon(aes(ymin = lo, ymax = hi), fill = BAND_C, alpha = .18) +
  geom_line(color = LINE_C, linewidth = .9) +
  geom_hline(yintercept = 1, linetype = 2, color = "grey50") +
  geom_vline(xintercept = REF, linetype = 3, color = "grey50") +
  labs(x = XLAB, y = YLAB, title = TITLE)
save_gg(p, NAME, w = 100, h = 82)
