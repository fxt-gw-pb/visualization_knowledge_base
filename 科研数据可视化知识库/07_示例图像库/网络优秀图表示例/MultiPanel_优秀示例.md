---
title: MultiPanel 优秀示例
type: example
status: active
updated: 2026-06-10
tags: [dataviz, example, multipanel]
---

# 示例图：多面板组合图 Multi-panel

> 关联：[[多面板组合图_MultiPanel]]。

## 示例 1：patchwork 官方组合示例

### 图像来源
- 原始链接：https://patchwork.data-imaginist.com/
- 来源：patchwork 文档（Thomas Lin Pedersen）
- license：MIT（代码）
- 是否可下载保存：示例图开源；默认参考链接
- 是否仅作参考：可参考/学习

### 图像特点
- 架构：`+ | /` 运算符拼版，`tag_levels="A"` 自动标号，`guides="collect"` 共享图例
- 值得学习：**直观运算符布局 + 自动 A/B/C/D + 合并图例**

### 可迁移规则
- 多面板用 patchwork 拼，统一主题 + 合并图例（[[patchwork与cowplot组合图]]）。

### 不建议照搬
- 严格对齐场景改 cowplot。

## 示例 2：医学论文 Figure 1/2 范式（baseline / model result）

### 图像来源
- 原始链接：示例见各医学期刊（如 https://www.thelancet.com 文章 Figure，受版权）
- 来源：医学期刊
- license：受版权，仅记链接
- 是否仅作参考：是

### 图像特点
- 架构：Figure 1 = 人群特征多面板；Figure 2 = 模型结果（森林 + ROC + 校准 + KM）
- 值得学习：**多面板讲完整证据链**；统一字体/配色/标号

### 可迁移规则
- 用 Figure 1/2 叙事结构组织 Framingham 测试输出（[[可测试图表任务清单]]）。

### 不建议照搬
- 期刊图受版权，不下载。

相关：[[多面板组合图_MultiPanel]] · [[patchwork与cowplot组合图]] · [[图表示例图库索引]]
