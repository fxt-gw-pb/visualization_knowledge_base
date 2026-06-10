---
title: R 测试记录
type: test-log
status: active
backend: r
updated: 2026-06-10
tags: [dataviz, framingham, r, test]
---

# R 测试记录

> 每个 R 跑图测试一节，套用统一模板。代码可直接复制运行。⏳ = 待跑。
> 数据：`可视化/data_example/Framingham_data(1)_副本.csv`。

## 0. 环境与数据载入（所有测试共用）

```r
# 包
library(tidyverse); library(ggpubr); library(ggbeeswarm)
library(survival); library(survminer); library(forestploter); library(pROC)
source("theme_pub.R")   # 见 [[ggplot2通用主题]]
set.seed(2026)

# 载入（忽略首列行号）
df <- readr::read_csv("data_example/Framingham_data(1)_副本.csv")[ ,-1]
# 派生 + 基线截面（见 [[变量字典]]）
df <- df %>% mutate(
  smoke_f = factor(CURSMOKE, labels = c("Non-smoker","Smoker")),
  hyp_f   = factor(PREVHYP,  labels = c("No HTN","HTN")),
  sex_f   = factor(SEX, labels=c("Male","Female")),  # 编码已确认：0=男 1=女
  age_f   = factor(AGE_group, levels = 1:3, ordered = TRUE))
base <- filter(df, PERIOD == 1)
```

> ✅ **已执行（2026-06-10）**。完整生产脚本是 `可视化/scripts/framingham_figs.R`（8 图）；本文件保留作分节说明与可复制片段。
> 环境：系统 R 4.5.2（已装 ggpubr/survminer/forestploter/pROC/pheatmap/ggdist 等）。运行：`Rscript scripts/framingham_figs.R`。
> 注意：本机无 X11，PDF 用默认 `pdf()` 设备而非 `cairo_pdf`；`mean_cl_normal` 用自定义 `mean_ci()` 替代（免装 Hmisc）。
> 输出图存 `07_示例图像库/Framingham测试图/`，已内嵌各卡片第 9.2 节。

---

## 测试模板（复制用）

```markdown
## 测试 N：<图名>
### 数据字段
### 图表目标
### R 实现
（代码块）
### 输出图像
（fig_xxx_v1.pdf 链接）
### 质量检查
- [ ] 图表类型合适
- [ ] 配色合理
- [ ] 坐标轴清楚
- [ ] 图例清楚
- [ ] 导出质量合格
- [ ] 可用于论文/汇报
### 发现的问题
### 返修记录
- 第一版问题：
- 第二版修改：
- 最终结论：
```

---

## 测试 1：PREVHYP × BMI 箱线图 ⭐ ⏳

### 数据字段
`base$hyp_f`（分组）、`base$BMI`（连续）

### 图表目标
比较有无既往高血压者的 BMI 分布，标组间检验 p。关联 [[箱线图_Boxplot]]。

### R 实现
```r
p1 <- ggplot(base, aes(hyp_f, BMI, fill = hyp_f)) +
  geom_boxplot(outlier.shape = NA, width = .55, alpha = .85) +
  geom_quasirandom(size = .5, alpha = .25, color = "grey25") +
  stat_compare_means(method = "wilcox.test", label = "p.format") +
  scale_fill_manual(values = c("No HTN" = "#0072B2","HTN" = "#D55E00")) +
  labs(x = NULL, y = "BMI (kg/m²)") +
  theme_pub() + theme(legend.position = "none")
ggsave("07_示例图像库/Framingham测试图/fig_box_prevhyp_bmi_v1.pdf",
       p1, width = 89, height = 70, units = "mm", device = cairo_pdf)
```
### 输出图像
⏳ `fig_box_prevhyp_bmi_v1.pdf`
### 质量检查 / 发现的问题 / 返修记录
⏳ 待跑后填写

---

## 测试 2：相关矩阵热图 ⭐ ⏳
### R 实现
```r
M <- base %>% select(TOTCHOL, BMI, GLUCOSE, TIMEDTH) %>%
  cor(use = "pairwise.complete.obs")
pheatmap::pheatmap(M, display_numbers = TRUE,
  color = colorRampPalette(c("#2166AC","white","#B2182B"))(100),
  breaks = seq(-1,1,length.out=101),
  filename = "07_示例图像库/Framingham测试图/fig_heatmap_corr_v1.pdf",
  width = 4, height = 3.5)
```
⏳ 待跑。关联 [[热图_Heatmap]]。

---

## 测试 3：BMI ~ PERIOD 趋势 ⭐ ⏳
### R 实现
```r
p3 <- ggplot(df, aes(PERIOD, BMI, color = sex_f, fill = sex_f)) +
  stat_summary(fun.data = mean_cl_normal, geom = "ribbon", alpha = .2, color = NA) +
  stat_summary(fun = mean, geom = "line", linewidth = 1) +
  stat_summary(fun = mean, geom = "point") +
  scale_x_continuous(breaks = 1:3, labels = c("Exam 1","Exam 2","Exam 3")) +
  scale_color_manual(values = c("#0072B2","#D55E00")) +
  scale_fill_manual(values = c("#0072B2","#D55E00")) +
  labs(x = NULL, y = "Mean BMI (kg/m²)", color = "Sex", fill = "Sex") +
  theme_pub()
ggsave("07_示例图像库/Framingham测试图/fig_line_bmi_period_v1.pdf",
       p3, width = 100, height = 75, units = "mm", device = cairo_pdf)
```
⏳ 待跑。关联 [[折线趋势图_Line]]。

---

## 测试 4：DEATH OR 森林图 ⭐ ⏳
### R 实现
```r
m <- glm(DEATH ~ sex_f + BMI + smoke_f + hyp_f + age_f + TOTCHOL,
         data = base, family = binomial)
res <- broom::tidy(m, conf.int = TRUE, exponentiate = TRUE) %>%
  filter(term != "(Intercept)")
# → forestploter，见 [[forestplot森林图模板]]
```
⏳ 待跑。关联 [[森林图_ForestPlot]]。

---

## 测试 5：PREVHYP KM ⭐ ⏳
### R 实现
```r
fit <- survfit(Surv(TIMEDTH, DEATH) ~ hyp_f, data = base)  # 基线每人一条
p5 <- ggsurvplot(fit, data = base, pval = TRUE, conf.int = TRUE,
  risk.table = TRUE, censor = TRUE, break.time.by = 1000,
  palette = c("#0072B2","#D55E00"),
  xlab = "Time (days)", ylab = "Survival probability",
  legend.labs = c("No HTN","HTN"), legend.title = "Hypertension")
```
⏳ 待跑。关联 [[KM生存曲线_KaplanMeier]]。

---

## 测试 6：DEATH ROC ⭐ ⏳
### R 实现
```r
base$pred <- predict(m, type = "response")     # m 来自测试4
r <- roc(base$DEATH, base$pred, quiet = TRUE)
ci.auc(r)                                       # AUC 95%CI
```
⏳ 待跑。**注意**：此处用同一数据训练+评价，仅为流程演示；正式评价需 hold-out/CV（[[ROC曲线_ROC]]）。

---

相关：[[可测试图表任务清单]] · [[Python测试记录]] · [[测试结论与返修记录]] · [[变量字典]]
