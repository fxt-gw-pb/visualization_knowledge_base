## 相关矩阵热图（ggplot geom_tile，发散配色中心0）—— 卡片 08_高维数据图/热图_Heatmap.md
## 合成数据，可独立运行： Rscript templates/r/heatmap.R
## 注：注释/聚类热图可改用 pheatmap 或 ComplexHeatmap（见 05_R代码模板/ComplexHeatmap模板.md），
##     那两者自带 filename 导出，用 save_dev 包裹即可。
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))
set.seed(2026)

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_heatmap"; TITLE <- "Correlation matrix"
DIV <- pal("div_rdbu")        # 低-中-高
# 换真实数据： M <- cor(dplyr::select(df, c1, c2, ...), use="pairwise.complete.obs")
X <- matrix(rnorm(200 * 5), 200, 5); colnames(X) <- c("TOTCHOL", "BMI", "GLUCOSE", "AGE", "SBP")
X[, 2] <- X[, 2] + .8 * X[, 1]; X[, 4] <- X[, 4] - .6 * X[, 3]
M <- cor(X)
# <<< PARAM ------------------------------------------------------

Mlong <- data.frame(Var1 = rep(rownames(M), times = ncol(M)),
                    Var2 = rep(colnames(M), each = nrow(M)),
                    value = as.vector(M))
p <- ggplot(Mlong, aes(Var1, Var2, fill = value)) +
  geom_tile() + geom_text(aes(label = sprintf("%.2f", value)), size = 2.6) +
  scale_fill_gradient2(low = DIV[1], mid = DIV[2], high = DIV[3], midpoint = 0, limits = c(-1, 1)) +
  labs(x = NULL, y = NULL, fill = NULL, title = TITLE) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1), panel.grid = element_blank())
save_gg(p, NAME, w = 95, h = 85)
