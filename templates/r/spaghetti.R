## 个体轨迹 Spaghetti 图（纵向）+ 组均值 95%CI —— 卡片 04_时间趋势图/个体轨迹图_Spaghetti.md
## 合成纵向数据，细线=个体，粗线=组均值。 Rscript templates/r/spaghetti.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
suppressPackageStartupMessages(library(dplyr))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_spaghetti"; TITLE <- "Individual trajectories"
XLAB <- "Visit"; YLAB <- "Biomarker"; PALETTE <- "cat_main"
# 换真实数据： 长格式 df(id, visit, y, grp)
mk <- function(g, slope, base, n = 25) do.call(rbind, lapply(1:n, function(i) {
  r0 <- base + rnorm(1, 0, 1.2); s <- slope + rnorm(1, 0, .25)
  data.frame(id = paste0(g, "_", i), visit = 0:4, y = r0 + s * (0:4) + rnorm(5, 0, .4), grp = g)
}))
df <- rbind(mk("Treatment", -0.6, 10), mk("Control", -0.1, 10))
# <<< PARAM ------------------------------------------------------

cols <- pal(PALETTE)[seq_along(unique(df$grp))]; names(cols) <- unique(df$grp)
agg <- df %>% group_by(grp, visit) %>%
  summarise(m = mean(y), se = sd(y) / sqrt(n()), .groups = "drop")
p <- ggplot() +
  geom_line(data = df, aes(visit, y, group = id, color = grp), linewidth = .25, alpha = .22) +
  geom_ribbon(data = agg, aes(visit, ymin = m - 1.96 * se, ymax = m + 1.96 * se, fill = grp), alpha = .2) +
  geom_line(data = agg, aes(visit, m, color = grp), linewidth = 1.1) +
  scale_color_manual(values = cols) + scale_fill_manual(values = cols) +
  labs(x = XLAB, y = YLAB, color = NULL, fill = NULL, title = TITLE)
save_gg(p, NAME, w = 100, h = 82)
