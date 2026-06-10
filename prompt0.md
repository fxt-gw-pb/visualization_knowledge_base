# 任务：在 Obsidian 中搭建“科研数据可视化 AI 共创知识仓库”

你是我的科研数据可视化知识库搭建 Agent。请你帮助我在我的 Obsidian 文件夹中建立一个长期可迭代的“科研数据可视化知识仓库”，后续这个知识仓库将进一步发展成一个 R/Python 双后端的作图 Skill。

请注意：当前阶段的重点不是立刻构建完整自动作图软件，而是先搭建结构清晰、可持续迭代、可被 AI 调用和人类阅读的知识仓库。这个知识仓库要服务于未来的科研绘图工作流，让每一种图表都可以逐步细化到接近论文发表/顶刊风格的高质量水平。

---

## 一、项目背景

我认为 R 和 Python 在数据可视化方面各有所长：

- R，尤其是 ggplot2 生态，更适合科研统计图、论文图、模板化图形语法。
    
- Python 更适合与机器学习、数据分析流水线、notebook、自动化报告结合。
    
- 我不想在 R 和 Python 之间二选一，而是希望建立一个统一的科研作图知识体系，未来让 Agent 根据数据类型、研究问题和目标图表自动选择 R 或 Python 后端。
    

最终目标是形成：

```text
知识仓库 → 图表规范 → 配色系统 → 图表模板 → 代码参数 → 示例图像 → Framingham 数据集测试 → 可调用的作图 Skill
```

当前阶段的目标是：

```text
先在 Obsidian 中搭建高质量知识仓库
```

---

## 二、核心目标

请在我的 Obsidian 文件夹下创建一个专门的知识仓库，例如：

```text
科研数据可视化知识库/
```

这个知识库要能够支持以下目标：

1. 系统整理所有常见科研图表类型。
    
2. 每一种图表都建立独立知识卡片。
    
3. 每张图都细化：
    
    - 适用场景
        
    - 不适用场景
        
    - 数据结构要求
        
    - 图表架构选择
        
    - 配色选择
        
    - R 实现方式
        
    - Python 实现方式
        
    - 关键参数
        
    - 高质量示例图
        
    - 常见问题
        
    - 自动返修规则
        
4. 收集网络上的优秀科研图表资源，并记录来源。
    
5. 使用我之后提供的 Framingham 数据集进行全流程跑通测试。
    
6. 让这个 Obsidian 知识库以后能被 Agent 读取，并进一步生成作图代码、图表模板和最终 Skill。
    

---

## 三、Obsidian 知识库总体结构

请在 Obsidian 中建立如下结构：

```text
科研数据可视化知识库/
├── 00_总览/
│   ├── 数据可视化知识库总览.md
│   ├── 图表类型索引.md
│   ├── R与Python后端选择规则.md
│   ├── 科研图表质量检查清单.md
│   ├── 图表返修规则总表.md
│   └── 术语表.md
│
├── 01_资源库/
│   ├── R绘图资源索引.md
│   ├── Python绘图资源索引.md
│   ├── 科研配色资源索引.md
│   ├── 顶刊图表风格参考.md
│   ├── 图表示例图库索引.md
│   └── 资源评价标准.md
│
├── 02_图表类型知识卡片/
│   ├── 01_分布图/
│   ├── 02_组间比较图/
│   ├── 03_相关性图/
│   ├── 04_时间趋势图/
│   ├── 05_模型结果图/
│   ├── 06_预测模型评价图/
│   ├── 07_生存分析图/
│   ├── 08_高维数据图/
│   ├── 09_组学图/
│   ├── 10_多面板组合图/
│   └── 11_医学流行病学常用图/
│
├── 03_配色系统/
│   ├── 配色系统总览.md
│   ├── 分类变量配色.md
│   ├── 连续变量配色.md
│   ├── 发散变量配色.md
│   ├── 医学二分类配色.md
│   ├── 模型效应方向配色.md
│   └── 色盲友好与打印友好原则.md
│
├── 04_图表架构系统/
│   ├── 图表架构总览.md
│   ├── 坐标轴设计.md
│   ├── 图例设计.md
│   ├── 标签与注释设计.md
│   ├── 分面与多面板设计.md
│   ├── 论文单栏双栏尺寸.md
│   └── 汇报型图表尺寸.md
│
├── 05_R代码模板/
│   ├── ggplot2通用主题.md
│   ├── ggplot2参数系统.md
│   ├── patchwork与cowplot组合图.md
│   ├── ComplexHeatmap模板.md
│   ├── survminer生存曲线模板.md
│   ├── forestplot森林图模板.md
│   └── R导出规范.md
│
├── 06_Python代码模板/
│   ├── matplotlib通用主题.md
│   ├── seaborn统计图模板.md
│   ├── plotnine模板.md
│   ├── SciencePlots模板.md
│   ├── sklearn模型评价图模板.md
│   ├── lifelines生存曲线模板.md
│   └── Python导出规范.md
│
├── 07_示例图像库/
│   ├── 网络优秀图表示例/
│   ├── Framingham测试图/
│   └── 示例图像来源记录.md
│
├── 08_Framingham测试/
│   ├── Framingham数据集说明.md
│   ├── 变量字典.md
│   ├── 可测试图表任务清单.md
│   ├── R测试记录.md
│   ├── Python测试记录.md
│   └── 测试结论与返修记录.md
│
└── 09_未来Skill设计/
    ├── 作图Skill总体设计.md
    ├── Agent调用流程.md
    ├── 输入输出规范.md
    ├── 图表决策流程.md
    └── MVP路线图.md
```

---

## 四、每个图表知识卡片的标准模板

每一种图表都要建立独立 Markdown 文件。请使用统一模板，便于 Obsidian 管理，也便于未来 Agent 读取。

例如：

```text
02_图表类型知识卡片/02_组间比较图/箱线图_Boxplot.md
```

每张图表卡片使用如下结构：

```markdown
---
chart_name: 箱线图
chart_name_en: Boxplot
chart_family: 组间比较图
data_type:
  - continuous
  - categorical_group
recommended_backend:
  r: ggplot2
  python: seaborn/matplotlib
difficulty: basic
priority: high
status: draft
tags:
  - dataviz
  - chart
  - boxplot
  - r
  - python
---

# 箱线图 Boxplot

## 1. 图表定位

说明这张图主要解决什么科研问题。

## 2. 适用场景

- 适合比较不同组之间连续变量的分布。
- 适合展示中位数、四分位数、异常值。
- 适合样本量中等或较大时使用。

## 3. 不适用场景

- 样本量极小且不展示原始点时不推荐。
- 如果希望展示完整分布形态，可能小提琴图或雨云图更好。
- 如果只展示均值差异，不应该只用箱线图表达全部信息。

## 4. 数据结构要求

| 字段 | 类型 | 含义 | 是否必需 |
|---|---|---|---|
| group | categorical | 分组变量 | 必需 |
| value | continuous | 连续型结局变量 | 必需 |
| subgroup | categorical | 可选分层变量 | 可选 |

## 5. 图表架构选择

### 5.1 基础架构

- x 轴：分组变量
- y 轴：连续变量
- 图层：boxplot + jitter points
- 可选：均值点、置信区间、p 值标注

### 5.2 高质量架构

- 样本量较小时：boxplot + raw points
- 分布形态重要时：violin + boxplot + points
- 需要美观展示时：raincloud plot
- 分组很多时：横向 boxplot

## 6. 配色选择

### 6.1 默认配色

说明适合该图的默认分类变量配色。

### 6.2 色盲友好配色

记录 Okabe-Ito、ColorBrewer、viridis、ggsci 等可选方案。

### 6.3 医学研究推荐配色

例如 case/control、treatment/control、risk group 等。

## 7. R 实现方案

### 7.1 推荐包

- ggplot2
- ggpubr
- ggsci
- ggbeeswarm
- ggdist

### 7.2 关键参数

解释 geom_boxplot、geom_jitter、theme、scale_fill 等参数。

### 7.3 基础代码模板

提供可直接复用的 R 代码。

### 7.4 发表级代码模板

提供更高质量版本。

## 8. Python 实现方案

### 8.1 推荐包

- matplotlib
- seaborn
- plotnine

### 8.2 关键参数

解释 seaborn.boxplot、stripplot、palette、linewidth、dpi 等参数。

### 8.3 基础代码模板

提供可直接复用的 Python 代码。

### 8.4 发表级代码模板

提供更高质量版本。

## 9. 示例图像

### 9.1 网络优秀示例

记录网络优秀图像链接、来源、许可情况、可学习点。

### 9.2 Framingham 数据测试示例

使用 Framingham 数据集跑通一个真实示例，并保存输出图。

## 10. 常见错误

- 只画箱线图但样本量很小，导致分布信息不足。
- 分组颜色过多。
- 坐标轴标签缺少单位。
- p 值标注过多，造成图形混乱。

## 11. 自动返修规则

- 如果 x 轴标签重叠，旋转 30-45 度或改横向。
- 如果样本量小于 30，自动叠加原始点。
- 如果组别超过 8 个，建议改横向或分面。
- 如果分布强偏态，考虑 log scale 或 violin/raincloud。

## 12. 与其他图表的关系

- 与小提琴图的区别
- 与雨云图的区别
- 与柱状图的区别
- 与点估计图的区别

## 13. 质量检查清单

- [ ] 是否展示了原始数据或分布信息？
- [ ] 颜色是否合理？
- [ ] 轴标签是否清楚？
- [ ] 是否有单位？
- [ ] 图例是否必要？
- [ ] 是否适合论文导出？
```

---

## 五、优先建设的图表类型

请不要一开始追求大而全，而是先搭建 MVP。优先建立以下图表卡片：

### 1. 分布图

- Histogram 直方图
    
- Density plot 密度图
    
- Boxplot 箱线图
    
- Violin plot 小提琴图
    
- Raincloud plot 雨云图
    
- Ridgeline plot 山峦图
    

### 2. 组间比较图

- Bar plot 柱状图
    
- Dot plot 点图
    
- Point-range plot 点估计 + CI
    
- Boxplot + jitter
    
- Violin + boxplot
    
- Stacked bar plot 堆叠柱状图
    
- 100% stacked bar plot 百分比堆叠图
    

### 3. 相关性图

- Scatter plot 散点图
    
- Scatter + regression line
    
- Bubble plot 气泡图
    
- Correlation heatmap 相关矩阵热图
    
- Pair plot 成对关系图
    

### 4. 时间趋势图

- Line plot 折线图
    
- Mean ± CI trend plot
    
- Spaghetti plot 个体轨迹图
    
- Area plot 面积图
    
- Slope chart 斜率图
    

### 5. 模型结果图

- Forest plot 森林图
    
- Coefficient plot 回归系数图
    
- Odds ratio plot
    
- Hazard ratio plot
    
- Marginal effect plot
    
- Nomogram-like visualization
    

### 6. 预测模型评价图

- ROC curve
    
- PR curve
    
- Calibration curve
    
- Decision curve analysis
    
- Lift curve
    
- Confusion matrix heatmap
    

### 7. 生存分析图

- Kaplan-Meier curve
    
- KM curve + risk table
    
- Cumulative incidence curve
    
- Cox model forest plot
    

### 8. 高维数据图

- Heatmap
    
- Annotated heatmap
    
- PCA plot
    
- UMAP plot
    
- t-SNE plot
    
- Cluster dendrogram
    

### 9. 组学图

- Volcano plot
    
- MA plot
    
- Pathway enrichment dotplot
    
- GO/KEGG barplot
    
- Lollipop plot
    

### 10. 多面板组合图

- Figure 1 style baseline figure
    
- Figure 2 style model result figure
    
- Multi-panel layout
    
- Patchwork/cowplot layout
    
- Matplotlib gridspec layout
    

### 11. 医学流行病学常用图

- Incidence trend plot
    
- Age-stratified prevalence plot
    
- Risk factor distribution plot
    
- Standardized rate plot
    
- Epidemiological flowchart
    
- Cohort selection flow diagram
    

---

## 六、必须检索和整理的绘图资源

请从网络检索、阅读并整理以下资源。不要只复制介绍，要提炼“对本知识库有什么用”。

### R 端资源

重点整理：

1. ggplot2
    
    - 用途：R 科研绘图核心框架。
        
    - 重点：Grammar of Graphics、theme、scale、facet、geom 系统。
        
2. R Graph Gallery
    
    - 用途：大量 R 图表示例。
        
    - 重点：按图表类型整理，可作为知识库图表分类参考。
        
3. ggsci
    
    - 用途：科学期刊风格配色。
        
    - 重点：NPG、Lancet、JAMA、NEJM、AAAS 等风格色板。
        
4. ggpubr
    
    - 用途：publication-ready plots。
        
    - 重点：科研常用图、p 值标注、组间比较。
        
5. ggthemes
    
    - 用途：常见媒体和出版风格主题。
        
    - 重点：Economist、Tufte、FiveThirtyEight、Wall Street Journal 等。
        
6. patchwork
    
    - 用途：多图组合。
        
    - 重点：论文多面板布局。
        
7. cowplot
    
    - 用途：出版级 ggplot 组合与对齐。
        
    - 重点：多面板排版。
        
8. ComplexHeatmap
    
    - 用途：复杂热图。
        
    - 重点：组学、临床注释、多层 annotation。
        
9. pheatmap
    
    - 用途：简单热图。
        
    - 重点：快速生成聚类热图。
        
10. survminer
    
    - 用途：生存分析可视化。
        
    - 重点：KM 曲线、risk table、p 值、Cox 模型结果。
        
11. forestplot / forestploter
    
    - 用途：森林图。
        
    - 重点：OR、HR、RR、回归模型、meta 分析。
        
12. EnhancedVolcano
    
    - 用途：火山图。
        
    - 重点：差异表达分析。
        
13. factoextra
    
    - 用途：PCA/聚类结果可视化。
        
14. ggdist / ggridges / ggbeeswarm
    
    - 用途：分布图、雨云图、蜂群图、山峦图。
        

### Python 端资源

重点整理：

1. matplotlib
    
    - 用途：Python 绘图底层核心。
        
    - 重点：figure、axes、style、export、精细控制。
        
2. seaborn
    
    - 用途：统计图快速生成。
        
    - 重点：boxplot、violinplot、regplot、heatmap、pairplot。
        
3. plotnine
    
    - 用途：Python 中类似 ggplot2 的 Grammar of Graphics。
        
    - 重点：跨 R/Python 图形语法统一。
        
4. SciencePlots
    
    - 用途：科学论文 Matplotlib 样式。
        
    - 重点：paper、science、ieee、nature 风格。
        
5. altair
    
    - 用途：声明式可视化。
        
    - 重点：快速探索、交互图。
        
6. plotly
    
    - 用途：交互式图表。
        
    - 重点：网页展示和探索分析。
        
7. scikit-learn metrics display
    
    - 用途：ROC、PR、confusion matrix 等模型评价图。
        
8. lifelines
    
    - 用途：Python 生存分析。
        
    - 重点：KM 曲线、Cox 模型。
        
9. statsmodels graphics
    
    - 用途：统计模型诊断图。
        
10. missingno
    
    - 用途：缺失值可视化。
        
11. joypy
    
    - 用途：ridgeline plot。
        
12. statannotations
    
    - 用途：seaborn/matplotlib 图中添加统计检验标注。
        

### 配色与设计资源

重点整理：

1. ColorBrewer
    
    - 分类变量、连续变量、发散变量配色。
        
    - 注意 colorblind safe、print friendly。
        
2. viridis
    
    - 连续变量色盲友好配色。
        
3. Okabe-Ito palette
    
    - 色盲友好分类变量配色。
        
4. Crameri scientific colour maps
    
    - 科学可视化连续/发散色图。
        
5. Nature / Science / Cell / Lancet / NEJM / JAMA 图表风格
    
    - 不要机械复制图，而是总结其设计原则：
        
        - 简洁
            
        - 高信息密度
            
        - 明确轴标签
            
        - 控制颜色数量
            
        - 多面板结构清晰
            
        - 注释服务于结论
            
        - 不使用无意义装饰
            

---

## 七、资源整理格式

在 `01_资源库/` 下建立资源索引时，每个资源请按如下格式记录：

```markdown
# 资源名称

## 基本信息

- 名称：
- 语言：
- 官网/仓库：
- 文档：
- GitHub：
- 维护状态：
- license：
- 适合程度：高/中/低

## 主要用途

这个资源主要适合解决什么绘图问题。

## 适合的图表类型

- 
- 
- 

## 不适合的场景

- 
- 

## 可迁移到本知识库的内容

- 图表类型分类
- 代码模板
- 配色
- 主题
- 参数设置
- 示例图架构

## 代表性代码/思路

记录关键用法，但不要大段复制文档。

## 参考链接

- 
```

---

## 八、样例图像收集规范

我希望每种图都有高质量样例图像。样例图像可以来自网络资源，但必须规范记录来源。

请建立：

```text
07_示例图像库/网络优秀图表示例/
```

每种图建立一个文件，例如：

```text
Boxplot_优秀示例.md
ForestPlot_优秀示例.md
ROC_优秀示例.md
Heatmap_优秀示例.md
```

每个示例图像记录：

```markdown
# 示例图：图表类型 + 来源名称

## 图像来源

- 原始链接：
- 来源网站/论文/仓库：
- 作者/机构：
- license/使用限制：
- 是否可下载保存到本地：
- 是否仅作为参考链接：

## 图像特点

- 图表架构：
- 配色：
- 字体：
- 坐标轴：
- 图例：
- 注释：
- 多面板结构：
- 值得学习的地方：

## 可迁移规则

- 
- 
- 

## 不建议照搬的地方

- 
- 
```

注意：

1. 不要无脑下载和复制网络图片。
    
2. 如果 license 不清楚，只记录链接和截图说明，不要作为可复用素材。
    
3. 重点不是收集图片本身，而是提炼高质量图表设计规则。
    
4. 样例图像要和图表知识卡片互相链接。
    
5. 每个图表卡片至少链接 2-3 个优秀示例。
    

---

## 九、Framingham 数据集测试设计

我会提供 Framingham 数据集。请为它建立专门的测试区：

```text
08_Framingham测试/
```

你需要完成以下内容：

### 1. 数据集说明

建立：

```text
Framingham数据集说明.md
变量字典.md
```

内容包括：

- 数据来源
    
- 每个变量的含义
    
- 变量类型
    
- 连续变量
    
- 分类变量
    
- 二分类变量
    
- 时间/结局变量
    
- 是否适合做预测模型
    
- 是否适合做生存分析
    
- 缺失值情况
    

### 2. 可测试图表任务清单

建立：

```text
可测试图表任务清单.md
```

例如：

```markdown
# Framingham 数据集可测试图表任务

## 分布图

- age 年龄分布直方图
- sysBP 收缩压密度图
- BMI 分布图

## 组间比较图

- 按 TenYearCHD 比较 age
- 按 TenYearCHD 比较 sysBP
- 按 sex 比较 BMI
- 按 currentSmoker 比较 heartRate

## 相关性图

- age, BMI, sysBP, diaBP, glucose 相关矩阵
- sysBP 与 diaBP 散点图
- age 与 TenYearCHD 风险关系图

## 模型结果图

- Logistic 回归预测 TenYearCHD 的 OR 森林图
- 模型系数图

## 预测模型评价图

- ROC curve
- PR curve
- Calibration curve
- Confusion matrix heatmap

## 多面板图

- Figure 1: baseline characteristics visualization
- Figure 2: model performance visualization
```

### 3. 测试记录

每个图表测试都要记录：

```markdown
# 测试记录：图表名称

## 数据字段

使用了哪些变量。

## 图表目标

这张图想表达什么。

## R 实现

代码路径或代码块。

## Python 实现

代码路径或代码块。

## 输出图像

链接到输出图。

## 质量检查

- [ ] 图表类型合适
- [ ] 配色合理
- [ ] 坐标轴清楚
- [ ] 图例清楚
- [ ] 导出质量合格
- [ ] 可用于论文/汇报

## 发现的问题

- 

## 返修记录

- 第一版问题：
- 第二版修改：
- 最终结论：
```

---

## 十、R/Python 后端选择规则

请在 `00_总览/R与Python后端选择规则.md` 中写清楚：

```text
普通科研统计图 → 优先 R/ggplot2
复杂多面板论文图 → 优先 R/ggplot2 + patchwork/cowplot
复杂热图/组学注释热图 → 优先 R/ComplexHeatmap
机器学习流水线中的快速图 → 优先 Python/Seaborn/Matplotlib
Python 分析结果需要直接出图 → Python/Matplotlib/Plotnine
交互探索 → Plotly/Altair
最终论文图 → 优先输出 PDF/SVG
组会汇报图 → 同时输出 PNG/PDF
```

注意：不要把 R 和 Python 写成竞争关系，而是写成“根据任务自动选择最佳后端”。

---

## 十一、配色系统设计

请在 `03_配色系统/` 中建立系统化配色规则。

核心思想：

```text
不要简单追求“顶刊同款颜色”，而要建立 publication-style palette registry。
配色要根据数据语义选择。
```

至少包括：

### 1. 分类变量配色

适合：

- 性别
    
- 病例/对照
    
- 治疗/对照
    
- 风险分组
    
- 多类别分组
    

要求：

- 色盲友好
    
- 打印友好
    
- 不超过 8-10 个主要颜色
    
- 超过颜色上限时建议分面或合并类别
    

### 2. 连续变量配色

适合：

- 风险评分
    
- 表达量
    
- 预测概率
    
- 年龄
    
- 血压
    
- BMI
    

要求：

- 亮度单调变化
    
- 避免 rainbow/jet
    
- 优先 viridis、ColorBrewer sequential、Crameri scientific colormaps
    

### 3. 发散变量配色

适合：

- 正负效应
    
- fold change
    
- 回归系数
    
- z-score
    
- 标准化残差
    

要求：

- 有明确中心值，例如 0
    
- 正负方向颜色语义一致
    
- 不要随意反转颜色含义
    

### 4. 医学二分类配色

建立统一语义：

```text
case/control
disease/no disease
treatment/control
exposed/unexposed
high risk/low risk
```

每组都要给出推荐颜色和注意事项。

---

## 十二、图表架构系统

请在 `04_图表架构系统/` 中建立以下规范：

1. 坐标轴设计
    
    - 什么时候必须从 0 开始
        
    - 什么时候可以截断
        
    - log scale 如何标注
        
    - 单位如何标注
        
2. 图例设计
    
    - 什么时候需要图例
        
    - 什么时候可以直接标注
        
    - 图例放右侧、底部、图内的规则
        
3. 标签与注释
    
    - 统计显著性如何标注
        
    - p 值如何格式化
        
    - CI/SD/SE 如何说明
        
    - 重点结论如何标注
        
4. 分面与多面板
    
    - 什么时候分面
        
    - 什么时候拆图
        
    - 多面板 A/B/C/D 标签规范
        
    - patchwork/cowplot/matplotlib gridspec 使用场景
        
5. 论文尺寸
    
    - 单栏图
        
    - 双栏图
        
    - Supplementary figure
        
    - PPT 图
        
6. 导出规范
    
    - PDF
        
    - SVG
        
    - PNG 300/600 dpi
        
    - 白底/透明背景
        
    - 文件命名规则
        

---

## 十三、质量检查与返修机制

请建立两个核心文件：

```text
00_总览/科研图表质量检查清单.md
00_总览/图表返修规则总表.md
```

### 质量检查清单

每张图都要检查：

```text
图表语义：
- 图形类型是否匹配数据类型？
- 是否误用柱状图展示连续变量分布？
- 是否误用饼图展示过多类别？
- 是否清楚展示研究问题？

统计表达：
- CI/SE/SD 是否标注清楚？
- p 值是否格式统一？
- log scale 是否明确标注？
- reference line 是否存在？
- 样本量 n 是否需要展示？

视觉质量：
- 字体是否统一？
- 字号是否适合论文/汇报？
- 坐标轴标签是否遮挡？
- 图例是否过长？
- 颜色是否色盲友好？
- 多面板间距是否一致？
- 是否存在无意义装饰？

导出质量：
- 是否输出 PDF/SVG？
- PNG 是否至少 300 dpi？
- 文件名是否规范？
- 图像边界是否裁切正确？
- 是否保留可复现代码？
```

### 返修规则

必须包含：

```text
如果坐标轴标签重叠 → 旋转标签、缩写标签或改为横向图
如果图例过长 → 移到底部、拆成多列或直接标注到图中
如果颜色类别过多 → 分面、合并低频类别或使用形状辅助
如果散点重叠严重 → alpha、jitter、hexbin、density contour
如果箱线图样本量太小 → 加原始点
如果柱状图表达连续变量均值 → 建议改为 box/violin/point-range
如果热图标签过密 → 聚类、筛选 top features 或隐藏部分标签
如果 p 值过多 → 改为全局检验或只展示预设比较
如果图片太拥挤 → 自动增加尺寸或拆成多面板
如果图像用于论文 → 优先导出 PDF/SVG
如果图像用于汇报 → 同时导出 PNG/PDF
```

---

## 十四、AI 共创迭代机制

这个知识库不是一次性完成，而是持续共创迭代。请建立以下机制：

### 1. 每个图表卡片设置状态

使用 frontmatter：

```yaml
status: draft / reviewed / tested / publication_ready
```

含义：

- draft：初稿，只完成基础整理
    
- reviewed：已经人工或 AI 检查过
    
- tested：已经用 Framingham 数据集跑通过
    
- publication_ready：已经有高质量代码、示例图、返修规则和质量检查
    

### 2. 每张图建立迭代记录

在每个图表卡片底部加入：

```markdown
## 14. 迭代记录

| 日期 | 版本 | 修改内容 | 问题 | 下一步 |
|---|---|---|---|---|
| 2026-xx-xx | v0.1 | 建立初稿 | 示例不足 | 增加 Framingham 测试 |
```

### 3. 每次新增图表都走固定流程

```text
建立图表卡片
↓
补充适用场景和不适用场景
↓
检索网络优秀示例
↓
整理 R/Python 实现
↓
写入配色和架构规则
↓
用 Framingham 数据集测试
↓
输出示例图
↓
执行质量检查
↓
记录返修规则
↓
更新状态
```

---

## 十五、执行顺序

请按以下顺序执行，不要一上来就写大量代码。

### Step 1：确认 Obsidian 根目录

先找到我的 Obsidian 文件夹。如果不确定，请让我提供路径。

### Step 2：创建知识库目录结构

在 Obsidian 中创建：

```text
科研数据可视化知识库/
```

以及上文列出的全部子目录。

### Step 3：创建总览文件

优先创建：

```text
00_总览/数据可视化知识库总览.md
00_总览/图表类型索引.md
00_总览/R与Python后端选择规则.md
00_总览/科研图表质量检查清单.md
00_总览/图表返修规则总表.md
```

### Step 4：创建资源索引

创建：

```text
01_资源库/R绘图资源索引.md
01_资源库/Python绘图资源索引.md
01_资源库/科研配色资源索引.md
01_资源库/顶刊图表风格参考.md
```

并开始检索和整理资源。

### Step 5：创建第一批图表知识卡片

优先创建以下 12 个 MVP 图表卡片：

```text
1. 散点图 Scatter plot
2. 箱线图 Boxplot
3. 小提琴图 Violin plot
4. 雨云图 Raincloud plot
5. 折线趋势图 Line plot
6. 点估计+置信区间图 Point-range plot
7. 森林图 Forest plot
8. KM生存曲线 Kaplan-Meier curve
9. ROC曲线 ROC curve
10. 校准曲线 Calibration curve
11. 热图 Heatmap
12. 多面板组合图 Multi-panel figure
```

### Step 6：为每个 MVP 图表补充资源和示例

每张图至少补充：

- 2 个网络优秀示例链接
    
- 1 套 R 实现思路
    
- 1 套 Python 实现思路
    
- 1 套配色建议
    
- 1 套架构建议
    
- 3 条常见错误
    
- 3 条返修规则
    

### Step 7：等待 Framingham 数据集

我之后会提供 Framingham 数据集。你需要在收到数据集后：

1. 建立变量字典。
    
2. 识别变量类型。
    
3. 设计每类图的测试任务。
    
4. 分别用 R 和 Python 跑图。
    
5. 保存输出图像。
    
6. 将测试结果写回对应图表卡片。
    
7. 更新图表状态为 tested 或 publication_ready。
    

---

## 十六、质量要求

请严格遵守：

1. Obsidian 笔记要结构清晰，适合长期维护。
    
2. 每个文件都要有标题、frontmatter、tags、反向链接。
    
3. 图表卡片之间要建立链接，例如箱线图链接到小提琴图、雨云图、点估计图。
    
4. 不要堆砌网络内容，要提炼成可执行规则。
    
5. 不要只收集代码，要解释为什么这样画。
    
6. 不要机械追求“顶刊同款”，要总结顶刊图表背后的设计原则。
    
7. 网络图像必须记录来源和 license。
    
8. 如果 license 不明确，只作为参考链接，不保存为可复用素材。
    
9. 所有代码模板都要可复制、可修改、可参数化。
    
10. 每个图表都要能服务于未来自动化作图 Skill。
    

---

## 十七、最终交付物

当前阶段请交付：

1. Obsidian 知识库完整目录结构。
    
2. 总览文件。
    
3. 资源索引文件。
    
4. 配色系统初稿。
    
5. 图表架构系统初稿。
    
6. 至少 12 个 MVP 图表知识卡片。
    
7. 每个 MVP 图表的 R/Python 实现思路。
    
8. 每个 MVP 图表的网络优秀示例链接。
    
9. 每个 MVP 图表的配色、架构、参数、返修规则。
    
10. Framingham 测试区的空白结构，等待我提供数据集后继续填充。
    
11. 一个 `09_未来Skill设计/作图Skill总体设计.md`，说明未来如何从这个知识库发展为自动作图 Skill。
    

---

## 十八、工作方式

请边做边记录，不要只在最后总结。

每完成一个阶段，请更新：

```text
00_总览/数据可视化知识库总览.md
```

记录：

- 已完成内容
    
- 新增文件
    
- 待补充内容
    
- 发现的问题
    
- 下一步建议
    

如果需要联网检索，请优先检索官方文档、GitHub 仓库、CRAN/PyPI 页面、权威教程和高质量图表 gallery。

如果发现某些资源过时、维护差、license 不清楚，请明确记录，不要盲目纳入核心资源。

当前最重要的任务是：  
**先把 Obsidian 知识仓库搭建起来，并让每种图表都有可持续细化迭代的知识卡片。**