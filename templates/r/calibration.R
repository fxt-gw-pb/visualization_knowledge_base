## 校准曲线（loess + 分箱点 + Brier）—— 卡片 06_预测模型评价图/校准曲线_Calibration.md
## 合成预测，可独立运行： Rscript templates/r/calibration.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_calibration"; TITLE <- "Calibration curve"
XLAB <- "Predicted probability"; YLAB <- "Observed frequency"
CURVE <- unname(pal("med_case_control")["low"]); PTS <- unname(pal("med_case_control")["high"])
# 换真实数据： y(0/1) 与 pred(预测概率)
n <- 2000; pred <- rbeta(n, 2, 3); y <- rbinom(n, 1, pred)
# <<< PARAM ------------------------------------------------------

dat <- data.frame(pred = pred, y = y)
brier <- mean((dat$pred - dat$y)^2)
qbin <- cut(dat$pred, breaks = quantile(dat$pred, 0:10 / 10), include.lowest = TRUE)
binpts <- data.frame(pred = tapply(dat$pred, qbin, mean), obs = tapply(dat$y, qbin, mean))
p <- ggplot(dat, aes(pred, y)) +
  geom_abline(slope = 1, intercept = 0, linetype = 2, color = "grey60") +
  geom_smooth(method = "loess", se = TRUE, color = CURVE, linewidth = .8) +
  geom_point(data = binpts, aes(pred, obs), color = PTS, size = 1.8, inherit.aes = FALSE) +
  geom_rug(sides = "b", alpha = .05) +
  annotate("text", x = .05, y = .92, hjust = 0, size = 2.8, label = sprintf("Brier = %.3f", brier)) +
  coord_equal(xlim = c(0, 1), ylim = c(0, 1)) +
  labs(x = XLAB, y = YLAB, title = TITLE)
save_gg(p, NAME, w = 88, h = 88)
