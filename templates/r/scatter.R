## 散点 + 回归线 + r（ggpubr）—— 卡片 03_相关性图/散点图_Scatter.md
## 合成数据，可独立运行： Rscript templates/r/scatter.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
suppressPackageStartupMessages(library(ggpubr))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_scatter"; TITLE <- "x vs y"; XLAB <- "x"; YLAB <- "y"
PT <- unname(pal("med_case_control")["low"]); LINE <- unname(pal("med_case_control")["high"])
# 换真实数据： df <- readr::read_csv("data.csv"); 列 x / y
x <- rnorm(400); df <- data.frame(x = x, y = 1.2 * x + rnorm(400))
# <<< PARAM ------------------------------------------------------

p <- ggscatter(df, "x", "y", alpha = .15, size = .8, color = PT,
               add = "reg.line", add.params = list(color = LINE)) +
  stat_cor(method = "pearson", label.x.npc = "left", label.y.npc = "top") +
  labs(x = XLAB, y = YLAB, title = TITLE) + theme_pub()
save_gg(p, NAME)
