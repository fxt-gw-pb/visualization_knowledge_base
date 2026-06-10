## 竞争风险累积发病曲线 CIF —— 卡片 07_生存分析图/竞争风险累积发病图_CompetingRisk.md
## 用 survival 多状态 survfit（event 为因子）估计 CIF；broom 整理。无需 cmprsk。
## 合成竞争风险数据，可独立运行： Rscript templates/r/cif.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
suppressPackageStartupMessages({ library(survival); library(broom) })
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_cif"; TITLE <- "Cumulative incidence (event of interest)"
XLAB <- "Time (days)"; YLAB <- "Cumulative incidence"
EVENT_STATE <- "event1"          # 目标事件状态名
TC <- pal("med_case_control")
# 换真实数据： df 含 time / event(0 删失/1 目标/2 竞争) / group
mk <- function(g, hz1, hz2, m = 300){
  t1 <- rexp(m, hz1); t2 <- rexp(m, hz2); tc <- rexp(m, 1/3000)
  t <- pmin(t1, t2, tc)
  ev <- ifelse(t1 <= t2 & t1 <= tc, 1, ifelse(t2 < t1 & t2 <= tc, 2, 0))
  data.frame(time = t, event = ev, group = g)
}
df <- rbind(mk("Exposed", .0009, .0006), mk("Unexposed", .0005, .0006))
# <<< PARAM ------------------------------------------------------

df$event <- factor(df$event, levels = c(0, 1, 2), labels = c("censor", "event1", "event2"))
fit <- survfit(Surv(time, event) ~ group, data = df)
td <- tidy(fit)                                   # 含 time/estimate/state/strata
td <- td[td$state == EVENT_STATE, ]
td$group <- sub("group=", "", td$strata)
p <- ggplot(td, aes(time, estimate, color = group)) +
  geom_step(linewidth = 1) +
  scale_color_manual(values = c(Exposed = unname(TC["high"]), Unexposed = unname(TC["low"]))) +
  labs(x = XLAB, y = YLAB, color = "Group", title = TITLE)
save_gg(p, NAME, w = 100, h = 82)
