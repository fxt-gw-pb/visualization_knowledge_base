## PCA 散点图（PC1 vs PC2，按组着色）—— 卡片 08_高维数据图/PCA图_PCA.md
## 合成高维数据 + prcomp，可独立运行： Rscript templates/r/pca.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_pca"; TITLE <- "PCA of samples"
PALETTE <- pal("cat_main")
# 换真实数据： X <- as.matrix(df[, feature_cols]); labels <- df$group
groups <- c("Type A", "Type B", "Type C"); per <- 80; p <- 20
centers <- matrix(rnorm(length(groups) * p, 0, 3), length(groups), p)
X <- do.call(rbind, lapply(seq_along(groups), function(i)
  matrix(rep(centers[i, ], per), per, p, byrow = TRUE) + matrix(rnorm(per * p), per, p)))
labels <- factor(rep(groups, each = per))
# <<< PARAM ------------------------------------------------------

pc <- prcomp(X, center = TRUE, scale. = TRUE)
ev <- (pc$sdev^2 / sum(pc$sdev^2)) * 100
d <- data.frame(PC1 = pc$x[, 1], PC2 = pc$x[, 2], grp = labels)
p_plot <- ggplot(d, aes(PC1, PC2, color = grp)) +
  geom_hline(yintercept = 0, linetype = 3, color = "grey70", linewidth = .3) +
  geom_vline(xintercept = 0, linetype = 3, color = "grey70", linewidth = .3) +
  geom_point(size = 1.6, alpha = .75) +
  scale_color_manual(values = PALETTE) +
  labs(x = sprintf("PC1 (%.1f%%)", ev[1]), y = sprintf("PC2 (%.1f%%)", ev[2]),
       color = NULL, title = TITLE)
save_gg(p_plot, NAME, w = 95, h = 85)
