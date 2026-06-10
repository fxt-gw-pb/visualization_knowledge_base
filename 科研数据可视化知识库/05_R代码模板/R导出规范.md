---
title: R 导出规范
type: code-template
status: active
backend: r
updated: 2026-06-10
tags:
  - dataviz
  - r
  - export
  - ggsave
  - template
---

# R 导出规范

> 出图最后一步：**矢量优先、尺寸即终稿、字体嵌入、命名规范、留可复现脚本**。配合 [[论文单栏双栏尺寸]]。

## 1. 格式选择

| 用途 | 格式 | 设备 |
|---|---|---|
| 论文线图/统计图 | **PDF / SVG**（矢量）| `cairo_pdf` / `svglite` |
| 含照片/密集像素（热图）| PNG/TIFF 高 dpi | `ragg::agg_png` / `agg_tiff` |
| 汇报 | PNG(≥300dpi) + PDF | 同时导 |
| 期刊 EPS 需求 | EPS | `cairo_ps` |

## 2. 标准 ggsave 调用

```r
library(ggplot2)
# 论文单栏（89mm）矢量，字体嵌入
ggsave("fig1_box_chd_bmi_v1.pdf", plot = p,
       width = 89, height = 70, units = "mm",
       device = cairo_pdf)                    # cairo 保证字体/透明正确

# 高 dpi PNG（汇报/预览）
ggsave("fig1_box_chd_bmi_v1.png", plot = p,
       width = 89, height = 70, units = "mm",
       dpi = 600, bg = "white",
       device = ragg::agg_png)                # ragg 字体渲染更好
```

## 3. 关键参数

| 参数 | 建议 |
|---|---|
| `width/height/units` | 按终稿尺寸（mm），见 [[论文单栏双栏尺寸]] |
| `device` | `cairo_pdf`/`svglite`（矢量）、`ragg::agg_png`（栅格）|
| `dpi` | 线图 PNG 600；含照片 300 |
| `bg` | "white" 或 "transparent"（深色 slide）|

## 4. 字体嵌入（避免投稿字体丢失）

- 用 `cairo_pdf`/`ragg` 设备，字体会被正确处理。
- 固定特定字体：`systemfonts::register_font()` 或 `showtext`（中文/特殊字体）。
- 检查 PDF 是否嵌字体：`pdffonts fig1.pdf`（终端）应显示 “emb=yes”。

## 5. 文件命名规范

```text
<figNo>_<chartType>_<topic>_<version>.<ext>
例：
fig1_box_chd_bmi_v2.pdf
fig2_km_prevhyp_v1.pdf
figS1_heatmap_clinmarkers_v1.png   （补充材料 S 前缀）
```
- 全小写、下划线分隔、版本号 `v1/v2`、补充材料 `figS#`。
- 与卡片第 14 节“迭代记录”的版本号对应。

## 6. 可复现（必做）

```r
# 脚本头部记录环境
sessionInfo()                         # 或 sessioninfo::session_info()
# 关键：数据版本 + 包版本 + 随机种子
set.seed(2026)
# 推荐 renv 锁定依赖：renv::snapshot()
```
- 每张图配一个可运行 `.R` 脚本，存到对应测试目录（[[R测试记录]]）。
- 不要只存图片不存代码（[[科研图表质量检查清单]] D 区）。

## 7. 常见错误（→ 返修）

- ❌ 只导 PNG 无矢量 → 论文补 PDF/SVG。
- ❌ 大图缩小导出 → 按终稿尺寸出。
- ❌ 字体没嵌入，换机器变字体 → cairo/ragg。
- ❌ 文件名随意（`Rplot01.pdf`）。
- ❌ 边界裁切错误留大白边 → 调 width/height 或 `+ theme(plot.margin=...)`。

相关：[[论文单栏双栏尺寸]] · [[汇报型图表尺寸]] · [[Python导出规范]] · [[ggplot2通用主题]]
