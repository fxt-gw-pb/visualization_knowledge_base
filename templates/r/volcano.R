## 火山图 Volcano（差异表达）—— 卡片 09_组学图/火山图_Volcano.md
## 合成基因数据，可独立运行： Rscript templates/r/volcano.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_volcano"; TITLE <- "Volcano plot"
XLAB <- "log2 fold change"; YLAB <- "-log10 (adj. p)"
FC_THR <- 1.0; P_THR <- 0.05
DIR <- pal("effect_dir")      # up=harm(红) down=protect(蓝) ns=灰
# 换真实数据： df 含 log2fc / padj（每行一个基因）
n <- 4000; log2fc <- rnorm(n)
padj <- 10^(-abs(rnorm(n, 0, 1.5)) - 0.2 * abs(log2fc))
df <- data.frame(log2fc = log2fc, padj = padj)
# <<< PARAM ------------------------------------------------------

df$sig <- with(df, ifelse(padj < P_THR & log2fc > FC_THR, "up",
                   ifelse(padj < P_THR & log2fc < -FC_THR, "down", "ns")))
df$sig <- factor(df$sig, levels = c("down", "ns", "up"))
cols <- c(down = unname(DIR["protect"]), ns = unname(DIR["ns"]), up = unname(DIR["harm"]))
p <- ggplot(df, aes(log2fc, -log10(padj), color = sig)) +
  geom_point(size = .7, alpha = .5) +
  geom_hline(yintercept = -log10(P_THR), linetype = 2, color = "grey60", linewidth = .4) +
  geom_vline(xintercept = c(-FC_THR, FC_THR), linetype = 2, color = "grey60", linewidth = .4) +
  scale_color_manual(values = cols) +
  labs(x = XLAB, y = YLAB, color = NULL, title = TITLE) +
  guides(color = guide_legend(override.aes = list(size = 2)))
save_gg(p, NAME, w = 95, h = 88)
