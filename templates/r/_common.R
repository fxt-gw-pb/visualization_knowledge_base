## sci-plot R 模板共享层：发表级主题 + 配色 registry + 导出助手。
## 所有 templates/r/*.R 都 source() 本文件。本机无 X11 → PDF 用默认 pdf() 不要 cairo_pdf()。
## REGISTRY 是 03_配色系统/配色系统总览.md 第 2 节的代码镜像 —— 模板只用 pal() 取值，不内联 hex。

suppressPackageStartupMessages(library(ggplot2))

## REPO：由调用模板设置的 .sd（脚本所在目录 templates/r）推导；缺省退回 cwd
.sd_guess <- if (exists(".sd")) .sd else getwd()
REPO <- normalizePath(file.path(.sd_guess, "..", ".."), mustWork = FALSE)

## 配色 registry（名 → 值），与 配色系统总览.md 同步
registry <- list(
  cat_main          = c("#E69F00","#56B4E9","#009E73","#F0E442",
                        "#0072B2","#D55E00","#CC79A7","#999999"),
  med_case_control  = c(high = "#D55E00", low = "#0072B2"),
  med_treat_control = c(treat = "#009E73", control = "#999999"),
  effect_dir        = c(harm = "#B2182B", protect = "#2166AC", ns = "#999999"),
  div_rdbu          = c("#2166AC","#FFFFFF","#B2182B"),   # 低-中-高
  seq_blues         = c("#F7FBFF","#6BAED6","#08306B")
)

pal <- function(name){
  if (!name %in% names(registry)) stop(sprintf("未知配色 registry 名 '%s'", name))
  registry[[name]]
}

## 发表级主题（与 framingham_figs.R 一致）
theme_pub <- function(base = 9) theme_minimal(base_size = base) +
  theme(panel.grid.minor = element_blank(),
        panel.grid.major = element_line(color = "grey92", linewidth = .3),
        axis.line   = element_line(color = "black", linewidth = .4),
        axis.ticks  = element_line(color = "black", linewidth = .3),
        plot.title  = element_text(face = "bold", size = base + 1),
        strip.text  = element_text(face = "bold"), strip.background = element_blank())
theme_set(theme_pub())

## 均值±95%CI（替代 Hmisc，避免额外依赖）
mean_ci <- function(x){ x <- x[!is.na(x)]; m <- mean(x); s <- sd(x)/sqrt(length(x))
  data.frame(y = m, ymin = m - 1.96*s, ymax = m + 1.96*s) }

default_outdir <- function()
  Sys.getenv("SCIPLOT_OUT", unset = file.path(REPO, "templates", "_preview"))

## 导出 PNG(300dpi)+PDF(矢量)；遵循 R导出规范.md
save_gg <- function(p, name, outdir = default_outdir(), w = 89, h = 72){
  dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
  ggsave(file.path(outdir, paste0(name, ".pdf")), p, width = w, height = h, units = "mm")
  ggsave(file.path(outdir, paste0(name, ".png")), p, width = w, height = h, units = "mm",
         dpi = 300, bg = "white")
  cat("  ->", name, "(png, pdf) @", outdir, "\n")
}

## 给 survminer/forestploter/pheatmap 等 base/grid 设备
save_dev <- function(expr, name, outdir = default_outdir(), w = 110, h = 120){
  dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
  pdf(file.path(outdir, paste0(name, ".pdf")), width = w/25.4, height = h/25.4); print(expr); dev.off()
  png(file.path(outdir, paste0(name, ".png")), width = w, height = h, units = "mm",
      res = 300, bg = "white"); print(expr); dev.off()
  cat("  ->", name, "(png, pdf) @", outdir, "\n")
}
