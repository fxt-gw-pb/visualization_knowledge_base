## 箱线图 + 抖动点 + 组间 p —— 卡片 02_组间比较图/箱线图_Boxplot.md
## 合成数据，可独立运行： Rscript templates/r/boxplot.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
suppressPackageStartupMessages({ library(ggpubr); library(ggbeeswarm) })
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_boxplot"; TITLE <- "Boxplot + jitter + p"; XLAB <- NULL; YLAB <- "Value"
PALETTE <- pal("med_case_control")            # 二分类（高=暖 低=冷）
# 换真实数据： df <- readr::read_csv("data.csv"); 列 grp / val
df <- data.frame(grp = factor(rep(c("Group 1", "Group 2"), each = 150)),
                 val = c(rnorm(150, 0, 1), rnorm(150, .6, 1.1)))
# <<< PARAM ------------------------------------------------------

cols <- c("Group 1" = unname(PALETTE["low"]), "Group 2" = unname(PALETTE["high"]))
p <- ggplot(df, aes(grp, val, fill = grp)) +
  geom_boxplot(outlier.shape = NA, width = .55, alpha = .85) +
  geom_quasirandom(size = .4, alpha = .15, color = "grey25") +
  stat_compare_means(method = "wilcox.test", label = "p.format", label.x = 1.3) +
  scale_fill_manual(values = cols) +
  labs(x = XLAB, y = YLAB, title = TITLE) + theme(legend.position = "none")
save_gg(p, NAME)
