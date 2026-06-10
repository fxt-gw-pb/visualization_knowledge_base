## 密度图（分组 KDE 叠加）—— 卡片 01_分布图/密度图_Density.md
## 合成数据，可独立运行： Rscript templates/r/density.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_density"; TITLE <- "Density by group"; XLAB <- "Value"; YLAB <- "Density"
PALETTE <- pal("cat_main")
# 换真实数据： df <- readr::read_csv("data.csv"); 列 val / grp
df <- data.frame(grp = factor(rep(c("A", "B", "C"), each = 400)),
                 val = c(rnorm(400, 0, 1), rnorm(400, 1.5, 1), rnorm(400, 3, 1.3)))
# <<< PARAM ------------------------------------------------------

p <- ggplot(df, aes(val, fill = grp, color = grp)) +
  geom_density(alpha = .35, linewidth = .7) +
  scale_fill_manual(values = PALETTE) + scale_color_manual(values = PALETTE) +
  labs(x = XLAB, y = YLAB, fill = NULL, color = NULL, title = TITLE)
save_gg(p, NAME, w = 100, h = 75)
