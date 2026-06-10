# CLAUDE.md — 科研数据可视化知识库 · Agent 操作手册

任何 agent 进入本仓库，**先读这一篇**，再读 `科研数据可视化知识库/00_总览/数据可视化知识库总览.md`（全库地图 MOC）。
本库目标：长期沉淀科研作图知识，支撑一个 **R / Python 双后端**自动作图流程。任务来了 → 据知识库快速产出**发表级**图。

## 快速路由（要画图时）

1. 读机器可读注册表 `registry/charts.json`（12 张卡片的族/后端/状态，**免读 87 个 md**）。
2. 按「科研问题」定位图表 → 打开对应卡片 `科研数据可视化知识库/02_图表类型知识卡片/<族>/<卡片>.md`。
3. 卡片含：适用/不适用、数据结构、配色、R/Python 实现、返修规则、实测图。
4. 收尾**必走** `00_总览/科研图表质量检查清单.md` + `00_总览/图表返修规则总表.md`。
5. 新增/迭代一张图：走总览**第 4 节标准流程**。

## 三条铁律（违反会引入腐化）

1. **配色不写死 hex** —— 一律引用 `03_配色系统/配色系统总览.md` 的命名色板（registry）。
2. **frontmatter 是唯一事实源** —— 改了卡片 `status`/后端等字段后，**必须重跑** `python scripts/build_registry.py` 刷新 `registry/charts.json`、`registry/charts.md` 和 `00_总览/图表类型索引.md` 的状态列。**不要手改派生文件**。
3. **代码模板的 `# >>> PARAM` 行是参数注入点** —— 复用模板时只动这些行。

## 环境事实（不知道会踩坑）

- **Python**：conda 环境 `viz`，解释器 `/opt/anaconda3/envs/viz/bin/python`。含 matplotlib / seaborn / scikit-learn / statsmodels / lifelines / scipy / pandas / numpy。**注意没有 PyYAML**（`build_registry.py` 因此自带零依赖解析器）。
- **R**：系统 R 4.5.2，含 ggplot2 / ggpubr / survminer / forestploter / pROC / pheatmap / ggdist / ggbeeswarm / ggsci。
- **本机无 X11** → R 出 PDF 用默认 `pdf()`，**不要用 `cairo_pdf()`**；用脚本里自定义的 `mean_ci()` 替代 `Hmisc`。
- 重建环境：`conda env create -f environment.yml`（R 包见 `scripts/install_r_pkgs.R`）。

## 数据坑（图注准确性的阻塞项）

测试数据 `data_example/Framingham_data(1)_副本.csv`：

- **纵向长格式**：11168 行 / 4215 人 / `PERIOD` 1–3（每人多行）。建模/作图前先决定用基线 `PERIOD==1` 还是全随访。
- 变量：`RANDID / SEX / TOTCHOL / CURSMOKE / BMI / GLUCOSE / PREVHYP / PERIOD / DEATH / TIMEDTH / AGE_group`。**不是**经典教学版（无 sysBP/diaBP/TenYearCHD）。
- **`SEX`：0=Male，1=Female**（已 4 项证据交叉验证确认）。
- ⏳ **未确认**：`AGE_group` 1/2/3 的年龄分界、单位（mg/dL、天）—— 作图用中性标签回避，**不要编造具体数值/单位**。
- 详见 `08_Framingham测试/变量字典.md` 与 `测试结论与返修记录.md`。

## 出图脚本（可复跑）

- `scripts/framingham_figs.py` / `.R` —— 真实数据各 14 张图（PNG 300dpi + PDF 矢量）→ `07_示例图像库/Framingham测试图/`。
- `scripts/gallery_demo.py` —— 12 张范式 demo（合成数据）→ `07_示例图像库/示例图库demo/`。
- `scripts/build_registry.py` —— 从 frontmatter 生成注册表 + 校验断链/缺字段（见铁律 2）。

## GitHub

远程：`git@github.com:fxt-gw-pb/visualization_knowledge_base.git`（**用 SSH，不用 HTTPS**）。提交/推送前先确认用户意图。
