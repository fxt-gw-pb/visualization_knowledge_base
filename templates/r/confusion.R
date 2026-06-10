## 混淆矩阵热图（注：计数 + 行归一%）—— 卡片 06_预测模型评价图/混淆矩阵_ConfusionMatrix.md
## 合成预测，可独立运行： Rscript templates/r/confusion.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_confusion"; TITLE <- "Confusion matrix"; XLAB <- "Predicted"; YLAB <- "Actual"
LABELS <- c("No event", "Event")
SEQ <- pal("seq_blues")
# 换真实数据： actual <- df$y; pred <- as.integer(prob >= 0.5)
n <- 600; actual <- rbinom(n, 1, .35)
pred <- as.integer(runif(n) < ifelse(actual == 1, .78, .12))
# <<< PARAM ------------------------------------------------------

cm <- table(factor(actual, 0:1, LABELS), factor(pred, 0:1, LABELS))
d <- as.data.frame(cm); names(d) <- c("Actual", "Predicted", "n")
d$rowsum <- ave(d$n, d$Actual, FUN = sum); d$pct <- d$n / d$rowsum
d$lab <- sprintf("%d\n%.0f%%", d$n, d$pct * 100)
p <- ggplot(d, aes(Predicted, Actual, fill = pct)) +
  geom_tile(color = "white", linewidth = .8) +
  geom_text(aes(label = lab), size = 3) +
  scale_fill_gradient(low = SEQ[1], high = SEQ[3], limits = c(0, 1), guide = "none") +
  scale_y_discrete(limits = rev(LABELS)) +
  coord_equal() + labs(x = XLAB, y = YLAB, title = TITLE) +
  theme(panel.grid = element_blank())
save_gg(p, NAME, w = 82, h = 78)
