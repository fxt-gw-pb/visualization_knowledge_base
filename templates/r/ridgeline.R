## 山峦图 / ridgeline（多组密度纵向堆叠，用 ggdist::stat_slab，无需 ggridges）
## —— 卡片 01_分布图/山峦图_Ridgeline.md。合成数据，可独立运行： Rscript templates/r/ridgeline.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
suppressPackageStartupMessages(library(ggdist))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_ridgeline"; TITLE <- "Ridgeline: value across groups"; XLAB <- "Value"
PALETTE <- pal("cat_main"); HEIGHT <- 1.6     # >1 让相邻山峦重叠
# 换真实数据： df <- readr::read_csv("data.csv"); 列 val / grp
df <- do.call(rbind, lapply(1:6, function(i)
  data.frame(grp = factor(paste("Grp", i), levels = paste("Grp", 1:6)),
             val = rnorm(300, i * .8, 1))))
# <<< PARAM ------------------------------------------------------

p <- ggplot(df, aes(x = val, y = grp, fill = grp)) +
  stat_slab(height = HEIGHT, color = "white", linewidth = .3, alpha = .85, normalize = "groups") +
  scale_fill_manual(values = PALETTE) +
  labs(x = XLAB, y = NULL, title = TITLE) + theme(legend.position = "none")
save_gg(p, NAME, w = 100, h = 90)
