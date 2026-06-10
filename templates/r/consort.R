## CONSORT 队列入组流程图（ggplot2 手搓盒+箭头）—— 卡片 11_医学流行病学常用图/CONSORT流程图_Consort.md
## 改 # >>> PARAM 的人数即可。可独立运行： Rscript templates/r/consort.R
.args <- commandArgs(trailingOnly = FALSE)
.sd <- dirname(normalizePath(sub("^--file=", "", .args[grep("^--file=", .args)])))
source(file.path(.sd, "_common.R"))

# >>> PARAM ------------------------------------------------------
NAME <- "tpl_consort"; TITLE <- "Study flow (CONSORT-style)"
BOX <- pal("cat_main")[2]     # 盒填充
assessed <- 1200; excluded <- 350; enrolled <- assessed - excluded
arm_a <- 430; arm_b <- 420; ana_a <- 410; ana_b <- 405
excl_txt <- paste0("Excluded (n=", excluded, ")\n• Not meeting criteria (n=210)",
                   "\n• Declined (n=90)\n• Other (n=50)")
# <<< PARAM ------------------------------------------------------

boxes <- data.frame(
  x = c(3.2, 7.3, 3.2, 1.8, 4.6, 1.8, 4.6),
  y = c(11, 9.4, 8.4, 6.0, 6.0, 4.3, 4.3),
  w = c(4.4, 4.2, 4.4, 3.0, 3.0, 3.0, 3.0),
  h = c(1.0, 1.6, 0.9, 0.9, 0.9, 0.9, 0.9),
  fc = c(BOX, "#F0F0F0", BOX, BOX, BOX, BOX, BOX),
  lab = c(sprintf("Assessed for eligibility\n(n=%d)", assessed), excl_txt,
          sprintf("Enrolled / Randomized\n(n=%d)", enrolled),
          sprintf("Arm A\nAllocated (n=%d)", arm_a), sprintf("Arm B\nAllocated (n=%d)", arm_b),
          sprintf("Analyzed (n=%d)", ana_a), sprintf("Analyzed (n=%d)", ana_b)))
seg <- data.frame(x = c(3.2, 3.2, 1.8, 4.6, 1.8, 4.6),
                  xe = c(3.2, 5.2, 1.8, 4.6, 1.8, 4.6),
                  y = c(10.5, 9.7, 7.2, 7.2, 5.55, 5.55),
                  ye = c(8.9, 9.7, 6.45, 6.45, 4.75, 4.75))
p <- ggplot() +
  geom_tile(data = boxes, aes(x, y, width = w, height = h), fill = boxes$fc,
            color = "black", linewidth = .4) +
  geom_text(data = boxes, aes(x, y, label = lab), size = 2.5, lineheight = .9) +
  geom_segment(data = seg, aes(x = x, xend = xe, y = y, yend = ye),
               arrow = arrow(length = unit(1.6, "mm")), linewidth = .4) +
  geom_segment(aes(x = 1.8, xend = 4.6, y = 7.2, yend = 7.2), linewidth = .4) +
  coord_cartesian(xlim = c(0, 10), ylim = c(3.5, 12)) +
  labs(title = TITLE) +
  theme_void() + theme(plot.title = element_text(face = "bold", hjust = .5, size = 10))
save_gg(p, NAME, w = 140, h = 150)
