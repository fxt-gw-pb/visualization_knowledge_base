## 缺失数据模式图（上：缺失% 条；下：缺失矩阵）—— 卡片 12_数据质量图/缺失数据图_Missingness.md
## base + patchwork（不依赖 naniar/VIM）。合成数据，可独立运行： Rscript templates/r/missingness.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
suppressPackageStartupMessages(library(patchwork))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_missingness"; TITLE <- "Missing data pattern"
BAR_COLOR <- pal("cat_main")[5]; MISS_COLOR <- unname(pal("med_case_control")["high"])
MATRIX_ROWS <- 200
# 换真实数据： df <- readr::read_csv("ehr.csv")
cols <- c("Age","Sex","BMI","SBP","Glucose","HbA1c","LDL","eGFR","Smoker","Outcome")
rates <- c(0,0,.01,.08,.12,.35,.22,.18,.05,0); n <- 1000
df <- as.data.frame(setNames(lapply(seq_along(cols), function(j){
  x <- rnorm(n); x[runif(n) < rates[j]] <- NA; x }), cols))
# <<< PARAM ------------------------------------------------------

mf <- colMeans(is.na(df)); ord <- names(sort(mf, decreasing = TRUE))
bar_df <- data.frame(var = factor(ord, levels = ord), pct = as.numeric(mf[ord]) * 100)
pbar <- ggplot(bar_df, aes(var, pct)) +
  geom_col(fill = BAR_COLOR, width = .7) +
  geom_text(aes(label = ifelse(pct > 0, sprintf("%.0f", pct), "")), vjust = -.3, size = 2.3) +
  labs(x = NULL, y = "Missing %") +
  theme(axis.text.x = element_blank(), axis.ticks.x = element_blank())

samp <- df[seq_len(min(MATRIX_ROWS, nrow(df))), ord, drop = FALSE]
nr <- nrow(samp)
ml <- data.frame(row = rep(seq_len(nr), times = length(ord)),
                 var = factor(rep(ord, each = nr), levels = ord),
                 missing = as.vector(is.na(as.matrix(samp))))
ptile <- ggplot(ml, aes(var, row, fill = missing)) +
  geom_tile() +
  scale_fill_manual(values = c(`FALSE` = "#F2F2F2", `TRUE` = MISS_COLOR), guide = "none") +
  labs(x = NULL, y = sprintf("Records (n=%d)", nr)) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1), axis.text.y = element_blank(),
        axis.ticks.y = element_blank(), panel.grid = element_blank())

p <- pbar / ptile + plot_layout(heights = c(1, 3)) +
  plot_annotation(title = TITLE, theme = theme(plot.title = element_text(face = "bold", hjust = .5)))
save_gg(p, NAME, w = 120, h = 105)
