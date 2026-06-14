## 状态转移 Alluvial 图（患者状态随时间流动）—— 卡片 11_医学流行病学常用图/状态转移图_Alluvial.md
## 手绘（免 ggalluvial）：各时点堆叠 + 转移流量彩带。 Rscript templates/r/alluvial.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_alluvial"; TITLE <- "Disease state transitions"
STAGES <- c("Baseline", "Year 1", "Year 2")
STATES <- c("Healthy", "Mild", "Severe", "Dead")
COLORS <- pal("cat_main")[seq_along(STATES)]; names(COLORS) <- STATES
P <- rbind(c(.70, .20, .08, .02), c(.15, .55, .25, .05),
           c(.03, .20, .57, .20), c(0, 0, 0, 1))         # 转移矩阵（行=from）
n <- 500
# <<< PARAM ------------------------------------------------------

ns <- length(STATES); nst <- length(STAGES)
seqm <- matrix(0L, n, nst)
seqm[, 1] <- sample(ns, n, replace = TRUE, prob = c(.6, .25, .13, .02))
for (s in 2:nst) for (i in 1:n) seqm[i, s] <- sample(ns, 1, prob = P[seqm[i, s - 1], ])

GAP <- 0.03 * n; BW <- 0.16
blocks <- function(col) { cnt <- sapply(1:ns, function(c) sum(seqm[, col] == c))
  top <- 0; m <- matrix(0, ns, 2)
  for (c in 1:ns) { m[c, ] <- c(top, top + cnt[c]); top <- top + cnt[c] + GAP }; m }
sm <- function(t) 3 * t^2 - 2 * t^3
xpos <- (1:nst) - 1; BL <- lapply(1:nst, blocks)

ribbons <- data.frame(); rects <- data.frame(); pid <- 0
for (s in 1:(nst - 1)) {
  oc <- BL[[s]][, 1]; ic <- BL[[s + 1]][, 1]
  for (src in 1:ns) for (dst in 1:ns) {
    h <- sum(seqm[, s] == src & seqm[, s + 1] == dst); if (h <= 0) next
    a0 <- oc[src]; a1 <- oc[src] + h; oc[src] <- a1
    b0 <- ic[dst]; b1 <- ic[dst] + h; ic[dst] <- b1
    t <- seq(0, 1, length.out = 30)
    xs <- (xpos[s] + BW / 2) + ((xpos[s + 1] - BW / 2) - (xpos[s] + BW / 2)) * t
    pid <- pid + 1
    ribbons <- rbind(ribbons, data.frame(x = c(xs, rev(xs)),
      y = c(a0 + (b0 - a0) * sm(t), rev(a1 + (b1 - a1) * sm(t))),
      id = pid, fill = unname(COLORS[src])))
  }
}
for (s in 1:nst) for (c in 1:ns)
  rects <- rbind(rects, data.frame(xmin = xpos[s] - BW / 2, xmax = xpos[s] + BW / 2,
    ymin = BL[[s]][c, 1], ymax = BL[[s]][c, 2], fill = unname(COLORS[c])))

p <- ggplot() +
  geom_polygon(data = ribbons, aes(x, y, group = id, fill = fill), alpha = .45, color = NA) +
  geom_rect(data = rects, aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax, fill = fill),
            color = "white", linewidth = .3) +
  scale_fill_identity(guide = "legend", breaks = unname(COLORS), labels = names(COLORS), name = NULL) +
  scale_x_continuous(breaks = xpos, labels = STAGES) + scale_y_reverse() +
  labs(x = NULL, y = NULL, title = TITLE) +
  theme(axis.text.y = element_blank(), axis.ticks.y = element_blank(),
        panel.grid = element_blank(), legend.position = "bottom")
save_gg(p, NAME, w = 115, h = 90)
