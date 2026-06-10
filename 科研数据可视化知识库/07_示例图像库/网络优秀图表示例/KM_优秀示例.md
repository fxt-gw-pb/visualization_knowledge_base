---
title: KM 优秀示例
type: example
status: active
updated: 2026-06-10
tags: [dataviz, example, survival, kaplan-meier]
---

# 示例图：KM 生存曲线

> 关联：[[KM生存曲线_KaplanMeier]]。

## 示例 1：survminer — ggsurvplot with risk table

### 图像来源
- 原始链接：https://rpkgs.datanovia.com/survminer/ （Drawing Survival Curves）
- 来源：survminer 文档（Kassambara）
- license：GPL-2（代码）
- 是否可下载保存：示例图开源；默认参考链接
- 是否仅作参考：可参考/学习

### 图像特点
- 架构：KM 阶梯曲线 + 置信带 + 删失标记 + **底部 risk table** + log-rank p
- 配色：分组明确，可接医学二分类
- 坐标轴：时间轴带单位，y 生存概率 0–1
- 值得学习：**risk table 是顶刊标配**；删失标记与 p 值齐全

### 可迁移规则
- KM 必带 risk table + log-rank + 删失标记（[[survminer生存曲线模板]]）。

### 不建议照搬
- 配色换成 [[医学二分类配色]] 固定映射。

## 示例 2：NEJM 风格 KM（医学论文范式）

### 图像来源
- 原始链接：示例可见 https://www.nejm.org （具体文章 KM 图，受版权）
- 来源：NEJM 等医学期刊
- license：受版权，仅记链接
- 是否仅作参考：是

### 图像特点
- 架构：克制、黑白/双色、risk table、随访末端截断
- 值得学习：**末端样本少时截断随访时间**，避免抖动误导

### 可迁移规则
- 末端 at-risk 少 → `xlim` 截断（[[KM生存曲线_KaplanMeier]] 返修）。

### 不建议照搬
- 期刊图受版权，不下载。

相关：[[KM生存曲线_KaplanMeier]] · [[森林图_ForestPlot]] · [[图表示例图库索引]]
