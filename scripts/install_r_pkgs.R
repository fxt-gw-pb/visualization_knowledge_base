#!/usr/bin/env Rscript
# R 后端依赖安装 —— 科研数据可视化知识库
# 用法： Rscript scripts/install_r_pkgs.R
# 目标：系统 R 4.5.2。本机无 X11 → 出 PDF 用默认 pdf()，勿用 cairo_pdf()。

cran_pkgs <- c(
  "ggplot2", "ggpubr", "survminer", "survival", "forestploter",
  "pROC", "pheatmap", "ggdist", "ggbeeswarm", "ggsci",
  "patchwork", "cowplot", "dplyr", "tidyr", "readr", "scales"
)

# Bioconductor（注释热图，可选）
bioc_pkgs <- c("ComplexHeatmap")

repos <- "https://cloud.r-project.org"

to_install <- cran_pkgs[!cran_pkgs %in% rownames(installed.packages())]
if (length(to_install)) {
  message("安装 CRAN 包: ", paste(to_install, collapse = ", "))
  install.packages(to_install, repos = repos)
} else {
  message("CRAN 包均已安装。")
}

if (length(bioc_pkgs)) {
  if (!requireNamespace("BiocManager", quietly = TRUE)) {
    install.packages("BiocManager", repos = repos)
  }
  bioc_missing <- bioc_pkgs[!bioc_pkgs %in% rownames(installed.packages())]
  if (length(bioc_missing)) {
    message("安装 Bioconductor 包: ", paste(bioc_missing, collapse = ", "))
    BiocManager::install(bioc_missing, update = FALSE, ask = FALSE)
  }
}

message("完成。")
