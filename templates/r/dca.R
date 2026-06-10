## 决策曲线分析 DCA（净获益）—— 卡片 06_预测模型评价图/决策曲线_DCA.md
## 比较 模型 vs treat-all vs treat-none。纯计算。合成预测，可独立运行： Rscript templates/r/dca.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_dca"; TITLE <- "Decision curve analysis"
XLAB <- "Threshold probability"; YLAB <- "Net benefit"
MODEL_COLOR <- unname(pal("med_case_control")["low"])
TMIN <- 0.01; TMAX <- 0.6
# 换真实数据： y <- df$y; prob <- predict(model, type = "response")
n <- 2000; prob <- rbeta(n, 2, 4); y <- rbinom(n, 1, prob)
# <<< PARAM ------------------------------------------------------

nb <- function(t){ tp <- sum(prob >= t & y == 1); fp <- sum(prob >= t & y == 0)
  tp / n - fp / n * (t / (1 - t)) }
thr <- seq(TMIN, TMAX, length.out = 100); prev <- mean(y)
d <- rbind(
  data.frame(thr = thr, nb = sapply(thr, nb),                      strat = "Model"),
  data.frame(thr = thr, nb = prev - (1 - prev) * (thr / (1 - thr)), strat = "Treat all"),
  data.frame(thr = thr, nb = 0,                                     strat = "Treat none"))
d$strat <- factor(d$strat, levels = c("Model", "Treat all", "Treat none"))
p <- ggplot(d, aes(thr, nb, color = strat, linetype = strat)) +
  geom_line(linewidth = .9) +
  scale_color_manual(values = c(Model = MODEL_COLOR, `Treat all` = "#999999", `Treat none` = "black")) +
  scale_linetype_manual(values = c(Model = 1, `Treat all` = 1, `Treat none` = 2)) +
  coord_cartesian(ylim = c(min(-0.02, min(sapply(thr, nb))), max(sapply(thr, nb)) * 1.15 + 1e-3)) +
  labs(x = XLAB, y = YLAB, color = NULL, linetype = NULL, title = TITLE)
save_gg(p, NAME, w = 100, h = 82)
