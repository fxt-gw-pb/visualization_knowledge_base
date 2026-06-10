## 多面板组合图（patchwork，A/B/C/D）—— 卡片 10_多面板组合图/多面板组合图_MultiPanel.md
## 合成数据，可独立运行： Rscript templates/r/multipanel.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
suppressPackageStartupMessages(library(patchwork))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_multipanel"; SUPTITLE <- "Figure 1. Composite (R)"
PALETTE <- pal("cat_main"); MED <- pal("med_case_control"); DIV <- pal("div_rdbu")
# <<< PARAM ------------------------------------------------------

g3 <- data.frame(grp = factor(rep(c("A", "B", "C"), each = 200)),
                 val = c(rnorm(200, 0, 1), rnorm(200, .8, 1.2), rnorm(200, .3, .8)))
pa <- ggplot(g3, aes(grp, fill = grp)) + geom_bar(width = .7) +
  scale_fill_manual(values = PALETTE) + labs(x = NULL, y = "Count", title = "Groups") +
  theme(legend.position = "none")
pb <- ggplot(g3, aes(grp, val, fill = grp)) + geom_boxplot(outlier.shape = NA, width = .5) +
  scale_fill_manual(values = PALETTE) + labs(x = NULL, y = "Value", title = "By group") +
  theme(legend.position = "none")
xx <- rnorm(200); pc <- ggplot(data.frame(x = xx, y = 1.2 * xx + rnorm(200)), aes(x, y)) +
  geom_point(alpha = .3, size = .8, color = unname(MED["low"])) +
  labs(x = "x", y = "y", title = "Relationship")
M <- cor(matrix(rnorm(200 * 4), 200, 4)); dimnames(M) <- list(LETTERS[1:4], LETTERS[1:4])
Ml <- data.frame(Var1 = rep(rownames(M), 4), Var2 = rep(colnames(M), each = 4), value = as.vector(M))
pd <- ggplot(Ml, aes(Var1, Var2, fill = value)) + geom_tile() +
  scale_fill_gradient2(low = DIV[1], mid = DIV[2], high = DIV[3], midpoint = 0, limits = c(-1, 1)) +
  labs(x = NULL, y = NULL, title = "Correlations") + theme(legend.position = "none")
fig <- (pa | pb) / (pc | pd) +
  plot_annotation(title = SUPTITLE, tag_levels = "A") & theme(plot.tag = element_text(face = "bold"))
save_gg(fig, NAME, w = 180, h = 150)
