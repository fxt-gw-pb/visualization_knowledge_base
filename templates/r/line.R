## 折线趋势 + 95%CI 带（mean_ci）—— 卡片 04_时间趋势图/折线趋势图_Line.md
## 合成数据，可独立运行： Rscript templates/r/line.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_line"; TITLE <- "Mean BMI trend across exams"; XLAB <- NULL; YLAB <- "Mean value"
PALETTE <- pal("cat_main")
BREAKS <- 1:3; BREAK_LABS <- c("Exam 1", "Exam 2", "Exam 3")
# 换真实数据： df <- readr::read_csv("data.csv"); 列 period(数值) / y / grp
df <- do.call(rbind, lapply(c("Male", "Female"), function(g)
  data.frame(grp = g, period = rep(1:3, each = 100),
             y = rnorm(300, mean = ifelse(g == "Male", 26, 25) + rep(c(0, .3, .6), each = 100), sd = 3))))
df$grp <- factor(df$grp)
# <<< PARAM ------------------------------------------------------

cols <- setNames(PALETTE[seq_len(nlevels(df$grp))], levels(df$grp))
p <- ggplot(df, aes(period, y, color = grp, fill = grp)) +
  stat_summary(fun.data = mean_ci, geom = "ribbon", alpha = .2, color = NA) +
  stat_summary(fun = mean, geom = "line", linewidth = 1) +
  stat_summary(fun = mean, geom = "point", size = 1.6) +
  scale_x_continuous(breaks = BREAKS, labels = BREAK_LABS) +
  scale_color_manual(values = cols) + scale_fill_manual(values = cols) +
  labs(x = XLAB, y = YLAB, color = NULL, fill = NULL, title = TITLE)
save_gg(p, NAME, w = 100, h = 75)
