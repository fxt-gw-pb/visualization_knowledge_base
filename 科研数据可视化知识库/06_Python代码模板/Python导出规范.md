---
title: Python 导出规范
type: code-template
status: active
backend: python
updated: 2026-06-10
tags:
  - dataviz
  - python
  - export
  - savefig
  - template
---

# Python 导出规范

> 出图最后一步：矢量优先、尺寸即终稿、字体可嵌入、命名规范、留可复现脚本。对应 R 的 [[R导出规范]]。

## 1. 格式选择

| 用途 | 格式 | 说明 |
|---|---|---|
| 论文线图/统计图 | **PDF / SVG**（矢量）| `savefig("f.pdf")` / `.svg` |
| 含照片/密集像素（热图）| PNG/TIFF 高 dpi | `dpi=300~600` |
| 汇报 | PNG(≥300dpi) + PDF | 同时导 |
| 期刊 EPS | EPS | `savefig("f.eps")` |

## 2. 标准 savefig 调用

```python
mm = 1/25.4
fig, ax = plt.subplots(figsize=(89*mm, 70*mm))   # 单栏，见 论文单栏双栏尺寸
# ... 画图 ...
fig.savefig("fig1_box_chd_bmi_v1.pdf",
            bbox_inches="tight", pad_inches=0.02) # 矢量，裁白边
fig.savefig("fig1_box_chd_bmi_v1.png",
            dpi=600, bbox_inches="tight", facecolor="white")  # 高 dpi PNG
```

## 3. 关键参数

| 参数 | 建议 |
|---|---|
| `figsize` | 终稿尺寸（英寸；mm→`*mm`），不要事后缩放 |
| `dpi` | 线图 PNG 600；含照片 300（PDF/SVG 无需 dpi）|
| `bbox_inches="tight"` | 裁多余白边 |
| `facecolor` | "white" 或 `transparent=True`（深色 slide）|
| `pad_inches` | 控制留白 |

## 4. 字体嵌入（避免投稿字体丢失）

```python
import matplotlib as mpl
mpl.rcParams["pdf.fonttype"] = 42   # TrueType，嵌入而非曲线化，期刊可编辑
mpl.rcParams["ps.fonttype"]  = 42
```
- 检查嵌入：`pdffonts fig.pdf` 应显示字体 emb=yes。
- 用系统有的字体（Arial/Helvetica/DejaVu Sans），缺字会回退。

## 5. 文件命名规范（与 R 一致）

```text
<figNo>_<chartType>_<topic>_<version>.<ext>
fig1_box_chd_bmi_v2.pdf
fig2_roc_models_v1.pdf
figS1_heatmap_clinmarkers_v1.png   （补充材料 S 前缀）
```
全小写、下划线、版本号、补充材料 `figS#`，与卡片第 14 节迭代记录对应。

## 6. 可复现（必做）

```python
import sys, sklearn, seaborn, matplotlib, pandas, numpy as np
print(sys.version, "sklearn", sklearn.__version__, "seaborn", seaborn.__version__)
np.random.seed(2026)              # 固定种子
# 推荐：导出 requirements.txt / 用 conda env / pip freeze
```
- 每张图配可运行 `.py`/notebook，存到测试目录（[[Python测试记录]]）。
- 不要只存图片不存代码（[[科研图表质量检查清单]] D 区）。

## 7. 常见错误（→ 返修）

- ❌ 只导 PNG 无矢量 → 论文补 PDF/SVG。
- ❌ `pdf.fonttype` 默认 3 把字体转曲线，期刊不可编辑 → 设 42。
- ❌ 大图缩小贴入 → 按终稿 figsize 出图。
- ❌ 没 `bbox_inches="tight"` 留大白边。
- ❌ 文件名 `Figure_1.png` 难追溯版本。

相关：[[R导出规范]] · [[论文单栏双栏尺寸]] · [[汇报型图表尺寸]] · [[matplotlib通用主题]]
