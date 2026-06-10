---
title: R 与 Python 后端选择规则
type: rule
status: active
updated: 2026-06-10
tags:
  - dataviz
  - backend
  - r
  - python
  - rule
---

# R 与 Python 后端选择规则

> 核心立场：**R 与 Python 不是竞争关系，而是同一作图工作流的两个后端。** Agent 根据“数据类型 + 研究问题 + 目标图表 + 下游环境”自动选择，而不是让用户二选一。

## 1. 一句话决策表

| 任务情境 | 优先后端 | 理由 |
|---|---|---|
| 普通科研统计图（箱线/散点/柱状/小提琴）| **R / ggplot2** | 图形语法成熟、ggpubr 一行加 p 值、ggsci 期刊配色 |
| 复杂多面板论文图（Figure 1/2）| **R / ggplot2 + patchwork/cowplot** | 对齐、A/B/C/D 标注、共享图例最省心 |
| 复杂热图 / 组学注释热图 | **R / ComplexHeatmap** | 多层 annotation、聚类、拆分行列无可替代 |
| 生存曲线 + risk table | **R / survminer** | `ggsurvplot` 一步出 risk table + p 值 |
| 森林图（OR/HR/RR/meta）| **R / forestploter 或 forestplot** | 表格 + 图对齐排版强 |
| 机器学习流水线里的快速图 | **Python / seaborn + matplotlib** | 紧贴 sklearn/pandas，不切换语言 |
| 模型评价图（ROC/PR/混淆矩阵/校准）| **Python / scikit-learn display** | `RocCurveDisplay` 等开箱即用 |
| Python 分析结果直接出图 | **Python / matplotlib / plotnine** | 不离开 notebook，plotnine 给到 ggplot 语法 |
| 交互探索 / 网页展示 | **Plotly / Altair** | 声明式 + 交互 |
| 想要跨语言统一图形语法 | **plotnine（Py）/ ggplot2（R）** | 同一套 Grammar of Graphics 心智模型 |

## 2. 选择的四个维度

```text
1) 数据从哪来？
   - 数据已在 R / data.frame 管道里  → R
   - 数据已在 pandas / sklearn 管道里 → Python

2) 研究问题是什么？
   - 统计推断、生存、meta、组学注释 → R 生态更厚
   - 预测建模、特征工程、深度学习    → Python 生态更厚

3) 目标图表的“天花板”在谁那边？
   - 论文级统计图、注释热图、生存图 → R 上限更高
   - 与训练循环耦合的评价图          → Python 更顺手

4) 下游怎么用？
   - 最终论文图 → 输出 PDF / SVG（矢量）
   - 组会汇报   → 同时输出 PNG(≥300dpi) + PDF
   - 网页/交互  → Plotly / Altair → HTML
```

## 3. 导出格式约定（与 [[图表架构总览]] 的导出规范一致）

```text
最终论文图   → 优先 PDF / SVG（矢量，可无损缩放，嵌字体）
组会汇报图   → 同时输出 PNG(300–600 dpi) + PDF
期刊投稿     → 看 author guideline；多数接受 TIFF/EPS/PDF，线图矢量、含照片栅格
交互/网页    → HTML（Plotly/Altair）
```

## 4. 关键决策原则

1. **同一管道内不要无谓切换语言**：数据在 pandas 就用 Python 出图，除非该图“天花板”明显在 R（如注释热图、生存 risk table）。
2. **统计图优先 R，工程图优先 Python**：统计语义（CI、p 值、生存、meta）R 更地道；与模型训练耦合的评价图 Python 更近。
3. **图形语法心智模型可迁移**：ggplot2 ↔ plotnine 几乎同构；学会一套，两边都能写。
4. **配色与主题统一**：无论哪个后端，都引用 [[配色系统总览]] 的命名色板，保证全 figure 视觉一致。
5. **可复现优先**：每张图保留可运行脚本（[[R导出规范]] / [[Python导出规范]]），而不是只存图片。

## 5. 不要这样做（反模式）

- ❌ 因为“别人都用 Python”就把生存 risk table 硬塞进 matplotlib，排版痛苦还不如 survminer。
- ❌ 因为“R 更顶刊”就把已在 sklearn 里训练好的模型结果导出 csv 再回 R 画 ROC，徒增环节。
- ❌ 在一张多面板 figure 里混用两套后端导致字体/字号/配色不一致。**一张 figure 用一个后端。**

## 6. 与各卡片的衔接

每张图表卡片 frontmatter 里都有：

```yaml
recommended_backend:
  r: <主推 R 包>
  python: <主推 Python 包>
```

Agent 路由时：先按本规则定后端，再读卡片第 7/8 节取对应代码模板，配色查 [[配色系统总览]]，尺寸查 [[论文单栏双栏尺寸]]，收尾走 [[科研图表质量检查清单]]。

相关：[[数据可视化知识库总览]] · [[作图Skill总体设计]] · [[图表决策流程]]
