## 小提琴图（+内嵌箱线）—— 卡片 01_分布图/小提琴图_Violin.md
## 合成数据，可独立运行： Rscript templates/r/violin.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_violin"; TITLE <- "Violin (inner box)"; XLAB <- NULL; YLAB <- "Value"
PALETTE <- pal("cat_main")
# 换真实数据： df <- readr::read_csv("data.csv"); 列 grp / val
df <- data.frame(grp = factor(rep(c("A", "B", "C"), each = 200)),
                 val = c(rnorm(200, 0, 1), rnorm(200, .8, 1.2), rnorm(200, .3, .8)))
# <<< PARAM ------------------------------------------------------

p <- ggplot(df, aes(grp, val, fill = grp)) +
  geom_violin(scale = "width", trim = FALSE, alpha = .7) +
  geom_boxplot(width = .12, outlier.shape = NA, alpha = .6, show.legend = FALSE) +
  scale_fill_manual(values = PALETTE) +
  labs(x = XLAB, y = YLAB, title = TITLE) + theme(legend.position = "none")
save_gg(p, NAME)
