## 柱状图（默认百分比堆叠/构成比）—— 卡片 02_组间比较图/柱状图_Bar.md
## MODE 可切 count / stack / fill。合成数据，可独立运行： Rscript templates/r/bar.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_bar"; TITLE <- "Composition by group (100% stacked)"; XLAB <- NULL; YLAB <- "Proportion"
MODE <- "fill"                # count(并排) | stack(堆叠计数) | fill(百分比堆叠)
PALETTE <- pal("cat_main")
# 换真实数据： df <- readr::read_csv("data.csv"); 列 grp(x) / sub(填充)
df <- data.frame(
  grp = factor(sample(c("Group 1", "Group 2", "Group 3"), 600, TRUE)),
  sub = factor(sample(c("Mild", "Moderate", "Severe"), 600, TRUE, prob = c(.5, .3, .2)),
               levels = c("Mild", "Moderate", "Severe")))
# <<< PARAM ------------------------------------------------------

pos <- switch(MODE, count = position_dodge(.7), stack = "stack", fill = "fill")
p <- ggplot(df, aes(grp, fill = sub)) +
  geom_bar(position = pos, width = .65, color = "white", linewidth = .2) +
  scale_fill_manual(values = PALETTE) +
  labs(x = XLAB, y = if (MODE == "fill") YLAB else "Count", fill = NULL, title = TITLE)
save_gg(p, NAME, w = 95, h = 78)
