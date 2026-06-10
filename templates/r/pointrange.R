## 点估计 + 95%CI（横向 + n 标注）—— 卡片 02_组间比较图/点估计置信区间图_PointRange.md
## 合成数据，可独立运行： Rscript templates/r/pointrange.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
suppressPackageStartupMessages(library(dplyr))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_pointrange"; TITLE <- "Mean value by group"; XLAB <- "Mean (95% CI)"; YLAB <- NULL
COLOR <- unname(pal("med_case_control")["low"])
# 换真实数据： df <- readr::read_csv("data.csv"); 列 grp / val
df <- data.frame(grp = factor(rep(c("Grp 1", "Grp 2", "Grp 3"), each = 150)),
                 val = c(rnorm(150, 25), rnorm(150, 26.5), rnorm(150, 28)))
# <<< PARAM ------------------------------------------------------

summ <- df %>% group_by(grp) %>%
  summarise(est = mean(val), se = sd(val) / sqrt(n()), n = n(), .groups = "drop") %>%
  mutate(lo = est - 1.96 * se, hi = est + 1.96 * se)
p <- ggplot(summ, aes(est, grp)) +
  geom_pointrange(aes(xmin = lo, xmax = hi), color = COLOR, linewidth = .6, size = .5) +
  geom_text(aes(x = hi, label = paste0("  n=", n)), hjust = 0, size = 2.6, color = "grey40") +
  labs(x = XLAB, y = YLAB, title = TITLE)
save_gg(p, NAME, w = 92, h = 62)
