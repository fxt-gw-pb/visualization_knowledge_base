## 倾向评分重叠图（mirror density，正性/共同支持域）—— 卡片 13_因果推断图/倾向评分重叠图_PSOverlap.md
## 合成 treated/control 倾向评分，上下镜像密度。 Rscript templates/r/psoverlap.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_psoverlap"; TITLE <- "Propensity score overlap"
XLAB <- "Propensity score"; YLAB <- "Density"
C_T <- unname(pal("med_treat_control")["treat"]); C_C <- unname(pal("med_treat_control")["control"])
# 换真实数据： ps <- predict(ps_model, type="response"); treat <- df$treat（0/1）
ps_t <- pmin(pmax(rbeta(600, 5, 3), 1e-3), 1 - 1e-3)
ps_c <- pmin(pmax(rbeta(900, 3, 5), 1e-3), 1 - 1e-3)
# <<< PARAM ------------------------------------------------------

dt <- density(ps_t, from = 0, to = 1); dc <- density(ps_c, from = 0, to = 1)
d <- rbind(data.frame(x = dt$x, y =  dt$y, grp = "Treated"),
           data.frame(x = dc$x, y = -dc$y, grp = "Control"))
p <- ggplot(d, aes(x, y, fill = grp)) +
  geom_area(alpha = .75) +
  geom_hline(yintercept = 0, linewidth = .3) +
  scale_fill_manual(values = c(Treated = C_T, Control = C_C)) +
  labs(x = XLAB, y = YLAB, fill = NULL, title = TITLE) +
  theme(axis.text.y = element_blank(), axis.ticks.y = element_blank(),
        legend.position = "top")
save_gg(p, NAME, w = 110, h = 82)
