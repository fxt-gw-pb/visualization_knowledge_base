## Swimmer plot 患者时间线 —— 卡片 11_医学流行病学常用图/Swimmer图_Swimmer.md
## 每名患者一条横条=随访时长 + 事件标记（应答/进展/死亡）+ 进行中箭头。
## 合成患者数据，可独立运行： Rscript templates/r/swimmer.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_swimmer"; TITLE <- "Swimmer plot: patient timelines"; XLAB <- "Months since enrollment"
BAR <- pal("cat_main")[2]; C <- pal("cat_main")
# 换真实数据： 每行一患者：pid/duration/response/progression/death(逻辑)/ongoing(逻辑)
m <- 16
df <- data.frame(
  pid = sprintf("P%02d", 1:m), duration = round(runif(m, 3, 30), 1),
  response = round(runif(m, 1, 8), 1),
  progression = ifelse(runif(m) < .6, round(runif(m, 8, 20), 1), NA),
  death = runif(m) < .35, ongoing = runif(m) < .4)
# <<< PARAM ------------------------------------------------------

df <- df[order(df$duration), ]; df$y <- seq_len(nrow(df))
df$pid <- factor(df$pid, levels = df$pid)
prog <- df[!is.na(df$progression) & df$progression <= df$duration, ]
dead <- df[df$death, ]; ong <- df[!df$death & df$ongoing, ]
p <- ggplot(df) +
  geom_segment(aes(x = 0, xend = duration, y = y, yend = y), color = BAR, alpha = .55, linewidth = 3) +
  geom_point(aes(response, y), shape = 17, size = 2, color = C[3]) +                    # 应答
  { if (nrow(prog)) geom_point(data = prog, aes(progression, y), shape = 4, size = 2, stroke = 1.1, color = C[6]) } +
  { if (nrow(dead)) geom_point(data = dead, aes(duration, y), shape = 15, size = 2, color = "#333333") } +
  { if (nrow(ong))  geom_segment(data = ong, aes(x = duration, xend = duration + 1.5, y = y, yend = y),
                                 arrow = arrow(length = unit(1.6, "mm")), color = "grey40") } +
  scale_y_continuous(breaks = df$y, labels = df$pid) +
  labs(x = XLAB, y = NULL, title = TITLE) +
  theme(panel.grid.major.y = element_blank())
save_gg(p, NAME, w = 120, h = 100)
