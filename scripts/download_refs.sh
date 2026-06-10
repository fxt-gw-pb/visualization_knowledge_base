#!/usr/bin/env bash
# 下载开源许可（BSD/Matplotlib License）的参考图例到示例图库。
# 仅下载许可明确开放的官方 gallery 图；版权受限图（期刊/license不明gallery）不下载。
# 复现：bash scripts/download_refs.sh
set -e
DIR="$(cd "$(dirname "$0")/.." && pwd)/科研数据可视化知识库/07_示例图像库/网络优秀图表示例/参考图例_开源"
mkdir -p "$DIR"
UA="Mozilla/5.0 (research; knowledge-base archival)"
dl(){ curl -sL -A "$UA" --max-time 30 "$1" -o "$DIR/$2" && file -b "$DIR/$2" | grep -q PNG && echo "ok  $2" || echo "FAIL $2"; }

# scikit-learn — BSD-3-Clause
dl "https://scikit-learn.org/stable/_images/sphx_glr_plot_roc_002.png"               "ref_sklearn_roc.png"
dl "https://scikit-learn.org/stable/_images/sphx_glr_plot_calibration_curve_001.png" "ref_sklearn_calibration.png"
dl "https://scikit-learn.org/stable/_images/sphx_glr_plot_confusion_matrix_001.png"  "ref_sklearn_confusion.png"
# seaborn — BSD-3-Clause
dl "https://seaborn.pydata.org/_images/grouped_violinplots.png"        "ref_seaborn_violin.png"
dl "https://seaborn.pydata.org/_images/horizontal_boxplot.png"         "ref_seaborn_boxplot.png"
dl "https://seaborn.pydata.org/_images/errorband_lineplots.png"        "ref_seaborn_line.png"
dl "https://seaborn.pydata.org/_images/many_pairwise_correlations.png" "ref_seaborn_corr_heatmap.png"
dl "https://seaborn.pydata.org/_images/scatterplot_matrix.png"         "ref_seaborn_scatter_matrix.png"
dl "https://seaborn.pydata.org/_images/regression_marginals.png"       "ref_seaborn_scatter_marginals.png"
dl "https://seaborn.pydata.org/_images/kde_ridgeplot.png"              "ref_seaborn_ridgeline.png"
# matplotlib — Matplotlib License (BSD-style)
dl "https://matplotlib.org/stable/_images/sphx_glr_boxplot_demo_001.png" "ref_mpl_boxplot.png"
echo "done -> $DIR"
