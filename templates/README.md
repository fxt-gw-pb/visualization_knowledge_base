# templates/ —— 可执行作图模板

把 `05_R代码模板/`、`06_Python代码模板/` 卡片里的代码块，沉淀为**可独立运行、可参数化、可冒烟测试**的脚本。
`sci-plot` Skill 出图时**读这里的文件**注参运行，而不是从 md 代码块拷贝 —— 从而与知识库不漂移。

```
templates/
├── python/_common.py     # 主题 + 配色 registry + 导出助手（共享）
├── python/<chart>.py      # 12 张 MVP 图，每张一个文件
├── r/_common.R            # 同上（R 端）
├── r/<chart>.R
└── _preview/              # 冒烟测试输出（gitignore）
```

12 张：`scatter / boxplot / violin / raincloud / line / pointrange / forest / km / roc / calibration / heatmap / multipanel`，与 `registry/charts.json` 的 12 张卡片一一对应。

## 运行

```bash
# Python（conda viz）
/opt/anaconda3/envs/viz/bin/python templates/python/boxplot.py            # 出到 templates/_preview/
SCIPLOT_OUT=/tmp/figs /opt/anaconda3/envs/viz/bin/python templates/python/boxplot.py

# R
Rscript templates/r/boxplot.R
SCIPLOT_OUT=/tmp/figs Rscript templates/r/boxplot.R

# 全部冒烟测试（改完模板必跑）
bash scripts/smoke_test.sh
```

每个模板**默认用合成数据**，因此随处可跑、license 干净；要换成真实数据见各文件 `# >>> PARAM` 区注释。

## PARAM 契约（sci-plot 注入点）

每个模板顶部有一段 `# >>> PARAM ... # <<< PARAM`，是**唯一**该改的地方。约定字段：

| 字段 | 含义 |
|---|---|
| `DATA` | 数据来源：合成（默认）或 `pd.read_csv(...)` / `read_csv(...)` |
| `X`,`Y`,`GROUP` | 列名/角色 |
| `PALETTE` | **配色 registry 名**（`cat_main`/`med_case_control`/`effect_dir`/`div_rdbu`/`seq_viridis`…），经 `pal()` 取值，**不写死 hex** |
| `TITLE`,`XLAB`,`YLAB` | 文案 |
| `FIGSIZE` | 尺寸（论文单栏≈3.4in / 双栏≈7in，详见 `04_图表架构系统/论文单栏双栏尺寸.md`）|
| `NAME` | 输出文件名（不含扩展名）|

输出：`<NAME>.png`(300dpi) + `<NAME>.pdf`(矢量) 到 `SCIPLOT_OUT`（默认 `templates/_preview/`）。

## 配色 registry（代码侧镜像）

`_common` 里的 `REGISTRY` 是 `03_配色系统/配色系统总览.md` 第 2 节的代码镜像。改色改两处需同步；
模板只用 `pal("名字")` 取值，绝不内联 hex。
