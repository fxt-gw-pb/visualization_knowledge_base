## 亚组分析森林图（含交互 p）—— 卡片 05_模型结果图/亚组森林图_Subgroup.md
## 合成亚组层 OR/CI + 交互 p，ggplot 手绘（log 轴）。 Rscript templates/r/subgroup.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_subgroup"; TITLE <- "Subgroup analysis"; XLAB <- "Odds ratio (95% CI)"
DIR <- pal("effect_dir")
# label/OR/lo/hi/header/p_int（表头行 OR=NA）
d <- data.frame(
  label  = c("Sex","  Male","  Female","Age group","  < 50 y","  >= 50 y","Smoking","  Never","  Current"),
  OR     = c(NA, 1.45, 1.30, NA, 1.10, 1.85, NA, 1.38, 1.55),
  lo     = c(NA, 1.10, 0.98, NA, 0.82, 1.40, NA, 1.02, 1.12),
  hi     = c(NA, 1.92, 1.72, NA, 1.48, 2.45, NA, 1.86, 2.15),
  header = c(TRUE, FALSE, FALSE, TRUE, FALSE, FALSE, TRUE, FALSE, FALSE),
  p_int  = c("0.62", NA, NA, "0.03", NA, NA, "0.48", NA, NA),
  stringsAsFactors = FALSE)
# <<< PARAM ------------------------------------------------------

d$y <- rev(seq_len(nrow(d)))
d$dir <- with(d, ifelse(is.na(OR), "ns", ifelse(lo > 1, "harm", ifelse(hi < 1, "protect", "ns"))))
pt <- d[!d$header, ]; hd <- d[d$header, ]
XL <- 0.11; XR <- 8                    # 标签 / 数值文本的 x 位置（log 轴）
p <- ggplot() +
  geom_vline(xintercept = 1, linetype = 2, color = "grey50") +
  geom_errorbarh(data = pt, aes(y = y, xmin = lo, xmax = hi, color = dir), height = .22, linewidth = .6) +
  geom_point(data = pt, aes(y = y, x = OR, color = dir), shape = 15, size = 2.6) +
  geom_text(data = d, aes(y = y, x = XL, label = label, fontface = ifelse(header, "bold", "plain")),
            hjust = 0, size = 2.8) +
  geom_text(data = pt, aes(y = y, x = XR, label = sprintf("%.2f (%.2f-%.2f)", OR, lo, hi)),
            hjust = 1, size = 2.5) +
  geom_text(data = hd, aes(y = y, x = XR, label = paste0("P-int ", p_int)),
            hjust = 1, size = 2.5, color = "grey40") +
  scale_color_manual(values = c(harm = unname(DIR["harm"]), protect = unname(DIR["protect"]),
                                ns = unname(DIR["ns"])), guide = "none") +
  scale_x_log10(limits = c(0.1, 9), breaks = c(0.5, 1, 2), labels = c("0.5", "1", "2")) +
  labs(x = XLAB, y = NULL, title = TITLE) +
  theme(axis.text.y = element_blank(), axis.ticks.y = element_blank(),
        panel.grid.major.y = element_blank())
save_gg(p, NAME, w = 135, h = 88)
