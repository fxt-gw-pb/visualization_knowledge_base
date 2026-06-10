## 雨云图（ggdist：云=halfeye + 箱 + 雨）—— 卡片 01_分布图/雨云图_Raincloud.md
## 合成数据，可独立运行： Rscript templates/r/raincloud.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
suppressPackageStartupMessages({ library(ggdist); library(ggbeeswarm) })
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_raincloud"; TITLE <- "Raincloud: value by group"; XLAB <- NULL; YLAB <- "Value"
PALETTE <- pal("cat_main")
# 换真实数据： df <- readr::read_csv("data.csv"); 列 grp / val
df <- data.frame(grp = factor(rep(c("Grp 1", "Grp 2", "Grp 3"), each = 200)),
                 val = c(rnorm(200, 0, 1), rnorm(200, .8, 1.1), rnorm(200, 1.5, .9)))
# <<< PARAM ------------------------------------------------------

p <- ggplot(df, aes(grp, val, fill = grp)) +
  stat_halfeye(adjust = .6, width = .6, justification = -.18, .width = 0,
               point_colour = NA, alpha = .7) +
  geom_boxplot(width = .13, outlier.shape = NA, alpha = .6) +
  geom_quasirandom(width = .08, size = .3, alpha = .15, color = "grey25") +
  scale_fill_manual(values = PALETTE) + coord_flip() +
  labs(x = XLAB, y = YLAB, title = TITLE) + theme(legend.position = "none")
save_gg(p, NAME, w = 100, h = 80)
