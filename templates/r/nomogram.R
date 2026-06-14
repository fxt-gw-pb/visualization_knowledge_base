## 列线图 Nomogram（logistic 预测模型）—— 卡片 05_模型结果图/列线图_Nomogram.md
## 手绘（免 rms）：每个预测因子一条带刻度点数标尺 + 总点数 + 风险标尺。 Rscript templates/r/nomogram.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_nomogram"; TITLE <- "Nomogram (logistic model)"
AXIS_C <- unname(pal("med_case_control")["low"])
RISKS <- c(0.1, 0.2, 0.3, 0.5, 0.7, 0.9); INTERCEPT <- -6.5
# 每个预测因子： name / beta / xmin / xmax / 显示刻度（ticks，分号分隔）
preds <- list(
  list(name = "Age (years)",     beta = 0.06, xmin = 40, xmax = 80, ticks = c(40, 50, 60, 70, 80)),
  list(name = "BMI (kg/m2)",     beta = 0.10, xmin = 18, xmax = 40, ticks = c(18, 24, 30, 36)),
  list(name = "Smoking (1=yes)", beta = 0.80, xmin = 0,  xmax = 1,  ticks = c(0, 1)),
  list(name = "Hypertension",    beta = 0.70, xmin = 0,  xmax = 1,  ticks = c(0, 1)))
# <<< PARAM ------------------------------------------------------

ranges <- sapply(preds, function(p) abs(p$beta) * (p$xmax - p$xmin))
scale <- 100 / max(ranges)
los <- sapply(preds, function(p) min(p$beta * p$xmin, p$beta * p$xmax))
max_total <- scale * sum(ranges); sum_lo <- sum(los)
rows <- c("Points", sapply(preds, `[[`, "name"), "Total Points", "Predicted risk")
ny <- length(rows); ys <- rev(seq_len(ny)) - 1     # 顶部 Points

seg <- data.frame(); tick <- data.frame(); txt <- data.frame()
add_ruler <- function(y, xn, labels, color, above = TRUE) {
  seg  <<- rbind(seg,  data.frame(x = min(xn), xend = max(xn), y = y, color = color))
  tick <<- rbind(tick, data.frame(x = xn, y = y, color = color))
  txt  <<- rbind(txt,  data.frame(x = xn, y = if (above) y + 0.18 else y - 0.30,
                                  label = labels, vj = if (above) 0 else 1))
}
# Points 标尺
pp <- seq(0, 100, 10); add_ruler(ys[1], pp / 100, as.character(pp), "black")
# 各预测因子标尺
for (j in seq_along(preds)) {
  p <- preds[[j]]; pts <- scale * (p$beta * p$ticks - los[j])
  add_ruler(ys[1 + j], pts / 100, formatC(p$ticks, format = "g"), AXIS_C)
}
# Total Points 标尺
tp <- seq(0, max_total, length.out = 6)
add_ruler(ys[ny - 1], tp / max_total, sprintf("%.0f", tp), "black")
# 风险标尺
rr <- RISKS; tpr <- scale * (qlogis(rr) - INTERCEPT - sum_lo)
ok <- tpr >= 0 & tpr <= max_total
add_ruler(ys[ny], (tpr[ok]) / max_total, formatC(rr[ok], format = "g"), "black", above = FALSE)

rownames_df <- data.frame(x = -0.02, y = ys, label = rows)
p <- ggplot() +
  geom_segment(data = seg, aes(x = x, xend = xend, y = y, yend = y, color = color), linewidth = .5) +
  geom_segment(data = tick, aes(x = x, xend = x, y = y - 0.12, yend = y + 0.12, color = color), linewidth = .4) +
  geom_text(data = txt, aes(x = x, y = y, label = label, vjust = vj), size = 2.1) +
  geom_text(data = rownames_df, aes(x = x, y = y, label = label), hjust = 1, fontface = "bold", size = 2.6) +
  scale_color_identity() +
  coord_cartesian(xlim = c(-0.34, 1.06), ylim = c(-0.7, ny - 0.3), clip = "off") +
  labs(title = TITLE) +
  theme_void(base_size = 9) + theme(plot.title = element_text(face = "bold", hjust = .5))
save_gg(p, NAME, w = 160, h = 92)
