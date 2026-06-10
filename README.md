# 科研数据可视化知识库

一个**长期可迭代**的科研数据可视化 / 科研作图个人知识仓库。既方便浏览、复习、随时把新的好图和想法沉淀进来，也方便与 AI agent 协作 —— 让任何 agent 据此快速产出**发表级**图表。

核心理念：不在 R 与 Python 之间二选一，而是**按任务自动选最佳后端**；每种图沉淀为结构统一、机器可读的知识卡片；不堆砌网络内容，而是提炼成**可执行规则**（适用/不适用、配色、架构、参数、返修）。

## 怎么用

- 🧭 **全库地图**：`科研数据可视化知识库/00_总览/数据可视化知识库总览.md`
- 📇 **找图表**：`00_总览/图表类型索引.md`（按科研问题分族）
- 🤖 **机器可读注册表**：`registry/charts.json` + `registry/charts.md`（由脚本从卡片 frontmatter 生成）
- 🎨 **配色系统**：`03_配色系统/配色系统总览.md`
- 🏗 **图表架构**：`04_图表架构系统/图表架构总览.md`
- ✅ **质检与返修**：`00_总览/科研图表质量检查清单.md`、`图表返修规则总表.md`

## 目录结构

```
可视化/
├── CLAUDE.md / AGENTS.md       # agent 操作手册（环境、数据坑、铁律）
├── README.md                   # 本文件（人的入口）
├── environment.yml             # conda 环境 viz 锁定
├── registry/                   # 由 frontmatter 派生：charts.json / charts.md
├── scripts/                    # 出图脚本 + build_registry.py
├── data_example/               # Framingham 测试数据
└── 科研数据可视化知识库/         # 00_总览 … 09_未来Skill设计（核心知识）
```

## 环境

```bash
conda env create -f environment.yml          # Python：matplotlib/seaborn/sklearn/statsmodels/lifelines…
Rscript scripts/install_r_pkgs.R             # R：ggplot2/ggpubr/survminer/forestploter/pROC…
```

改了任何卡片 frontmatter 后，重跑：

```bash
/opt/anaconda3/envs/viz/bin/python scripts/build_registry.py   # 刷新注册表 + 校验断链/缺字段
```

## 维护约定

- frontmatter 是唯一事实源，`registry/` 与索引状态列全是派生产物，勿手改。
- 配色引用 registry 名，不写死 hex。
- 新增一张图走总览第 4 节标准流程，跑通后状态升级（`draft → reviewed → tested → publication_ready`）。
