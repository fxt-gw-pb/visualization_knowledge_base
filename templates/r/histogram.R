## 直方图（+核密度叠加）—— 卡片 01_分布图/直方图_Histogram.md
## 合成数据，可独立运行： Rscript templates/r/histogram.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_histogram"; TITLE <- "Distribution of a continuous variable"
XLAB <- "Value"; YLAB <- "Density"
FILL <- pal("cat_main")[2]; LINE <- pal("cat_main")[5]   # 浅蓝填充 + 深蓝密度线
BINS <- 40
# 换真实数据： df <- readr::read_csv("data.csv"); 列 x
df <- data.frame(x = rnorm(2000, 230, 45))
# <<< PARAM ------------------------------------------------------

p <- ggplot(df, aes(x)) +
  geom_histogram(aes(y = after_stat(density)), bins = BINS, fill = FILL,
                 color = "white", alpha = .85) +
  geom_density(color = LINE, linewidth = 1) +
  labs(x = XLAB, y = YLAB, title = TITLE)
save_gg(p, NAME, w = 92, h = 72)
