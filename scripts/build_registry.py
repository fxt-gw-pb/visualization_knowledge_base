#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从图表卡片的 YAML frontmatter 生成机器可读注册表，并把派生信息回写到人看的索引。

唯一事实源 = 每张卡片 frontmatter。本脚本是纯派生工具，不手写状态。

产物：
  registry/charts.json        —— agent 路由用（免读 87 个文件）
  registry/charts.md          —— 人看的自动生成状态总表（按族分组）
  00_总览/图表类型索引.md      —— 仅就地刷新带 ✅ 行的「状态」列，其余不动

同时做轻量校验：必填字段缺失、recommended_backend 缺 r/python、卡片内 [[wikilink]] 断链。
零三方依赖（viz 环境无 PyYAML），自带极简 frontmatter 解析器。

用法： /opt/anaconda3/envs/viz/bin/python scripts/build_registry.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # 可视化/
KB = ROOT / "科研数据可视化知识库"
CARDS_DIR = KB / "02_图表类型知识卡片"
INDEX_FILE = KB / "00_总览" / "图表类型索引.md"
REGISTRY_DIR = ROOT / "registry"

REQUIRED = ["chart_name", "chart_name_en", "chart_family", "status"]
VALID_STATUS = {"draft", "reviewed", "tested", "publication_ready"}

# 卡片 id → 可执行模板文件名（templates/{python,r}/<base>.{py,R}）
TEMPLATE_MAP = {
    "散点图_Scatter": "scatter", "箱线图_Boxplot": "boxplot",
    "小提琴图_Violin": "violin", "雨云图_Raincloud": "raincloud",
    "折线趋势图_Line": "line", "点估计置信区间图_PointRange": "pointrange",
    "森林图_ForestPlot": "forest", "KM生存曲线_KaplanMeier": "km",
    "ROC曲线_ROC": "roc", "校准曲线_Calibration": "calibration",
    "热图_Heatmap": "heatmap", "多面板组合图_MultiPanel": "multipanel",
}


def parse_frontmatter(text: str) -> dict:
    """极简 YAML frontmatter 解析：顶层标量、顶层列表(- x)、一层嵌套字典(key: v)。

    够用于本库卡片结构（data_type/tags 是列表，recommended_backend 是字典）。
    """
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    body = text[3:end].strip("\n").splitlines()

    data: dict = {}
    cur_key = None          # 正在累积的嵌套块的父键
    cur_kind = None         # "list" | "dict"
    for raw in body:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        if indent == 0:
            if line.endswith(":"):                       # 进入嵌套块
                cur_key = line[:-1].strip()
                cur_kind = None
                data[cur_key] = None
            elif ":" in line:                            # 顶层标量
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip()
                cur_key = cur_kind = None
        else:                                            # 嵌套行
            if cur_key is None:
                continue
            if line.startswith("- "):
                if cur_kind != "list":
                    data[cur_key] = []
                    cur_kind = "list"
                data[cur_key].append(line[2:].strip())
            elif ":" in line:
                if cur_kind != "dict":
                    data[cur_key] = {}
                    cur_kind = "dict"
                k, v = line.split(":", 1)
                data[cur_key][k.strip()] = v.strip()
    return data


def collect_cards():
    cards, warnings = [], []
    for md in sorted(CARDS_DIR.rglob("*.md")):
        if md.stem.startswith("_"):                       # 族索引，非图表卡片
            continue
        fm = parse_frontmatter(md.read_text(encoding="utf-8"))
        if "chart_name_en" not in fm:                     # 不是图表卡片
            continue
        rel = md.relative_to(ROOT).as_posix()
        for field in REQUIRED:
            if not fm.get(field):
                warnings.append(f"[缺字段] {rel} 缺 `{field}`")
        st = fm.get("status")
        if st and st not in VALID_STATUS:
            warnings.append(f"[状态非法] {rel} status=`{st}`，应为 {sorted(VALID_STATUS)}")
        backend = fm.get("recommended_backend") or {}
        if not isinstance(backend, dict) or "r" not in backend or "python" not in backend:
            warnings.append(f"[后端] {rel} recommended_backend 缺 r/python")
        base = TEMPLATE_MAP.get(md.stem)
        tpl_py = f"templates/python/{base}.py" if base else None
        tpl_r = f"templates/r/{base}.R" if base else None
        if tpl_py and not (ROOT / tpl_py).exists():
            tpl_py = None
        if tpl_r and not (ROOT / tpl_r).exists():
            tpl_r = None
        if st in ("tested", "publication_ready") and (not tpl_py or not tpl_r):
            warnings.append(f"[缺模板] {rel} status={st} 但缺可执行模板（py={bool(tpl_py)} r={bool(tpl_r)}）")
        cards.append({
            "id": md.stem,
            "file": rel,
            "chart_name": fm.get("chart_name"),
            "chart_name_en": fm.get("chart_name_en"),
            "chart_family": fm.get("chart_family"),
            "backend_r": backend.get("r") if isinstance(backend, dict) else None,
            "backend_python": backend.get("python") if isinstance(backend, dict) else None,
            "template_python": tpl_py,
            "template_r": tpl_r,
            "status": st,
            "priority": fm.get("priority"),
            "difficulty": fm.get("difficulty"),
            "data_type": fm.get("data_type") or [],
            "tags": fm.get("tags") or [],
        })
    return cards, warnings


ASSET_EXT = {".png", ".jpg", ".jpeg", ".pdf", ".svg", ".gif", ".webp"}


def check_links(warnings):
    """全库扫描 [[wikilink]]/![[embed]]，对真正断链报警。

    - 跳过 ``` 围栏代码块（避免把 df[["A","B"]] 当成链接）。
    - 别名 |alias 与 #anchor 忽略。
    - 形如 xxx.png 的资源嵌入按真实文件名解析（图片不是 .md，不能查 stems）。
    """
    note_stems = {p.stem for p in KB.rglob("*.md")}
    asset_names = {p.name for p in KB.rglob("*") if p.suffix.lower() in ASSET_EXT}
    link_re = re.compile(r"\[\[([^\]]+)\]\]")
    for md in sorted(KB.rglob("*.md")):
        in_fence = False
        for line in md.read_text(encoding="utf-8").splitlines():
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for m in link_re.finditer(line):
                target = m.group(1).split("|")[0].split("#")[0].strip()
                if not target:
                    continue
                if Path(target).suffix.lower() in ASSET_EXT:   # 资源嵌入
                    if target not in asset_names:
                        warnings.append(f"[缺图] {md.relative_to(ROOT).as_posix()} -> ![[{target}]]")
                elif target not in note_stems:                 # 笔记链接
                    warnings.append(f"[断链] {md.relative_to(ROOT).as_posix()} -> [[{target}]]")


def write_json(cards):
    REGISTRY_DIR.mkdir(exist_ok=True)
    payload = {
        "_generated_by": "scripts/build_registry.py",
        "_note": "派生产物，请勿手改；改卡片 frontmatter 后重跑脚本",
        "count": len(cards),
        "charts": cards,
    }
    (REGISTRY_DIR / "charts.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(cards):
    fams = {}
    for c in cards:
        fams.setdefault(c["chart_family"], []).append(c)
    lines = [
        "---", "title: 图表卡片状态总表（自动生成）", "type: index",
        "tags: [dataviz, index, generated]", "---", "",
        "# 图表卡片状态总表（自动生成）", "",
        "> ⚠️ 本文件由 `scripts/build_registry.py` 从各卡片 frontmatter 生成，**请勿手改**。",
        "> 改了卡片后重跑脚本即可刷新。机器可读版见 `registry/charts.json`。", "",
        f"共 {len(cards)} 张卡片。", "",
    ]
    for fam in sorted(fams):
        lines += [f"## {fam}", "",
                  "| 卡片 | EN | 状态 | 优先级 | R 后端 | Python 后端 |",
                  "|---|---|---|---|---|---|"]
        for c in sorted(fams[fam], key=lambda x: x["id"]):
            lines.append(
                f"| [[{c['id']}]] | {c['chart_name_en']} | {c['status']} | "
                f"{c['priority'] or '—'} | {c['backend_r'] or '—'} | {c['backend_python'] or '—'} |")
        lines.append("")
    (REGISTRY_DIR / "charts.md").write_text("\n".join(lines), encoding="utf-8")


def refresh_index(cards):
    """就地刷新 图表类型索引.md：仅含 ✅ 的表行，把最后一列(状态)改为卡片真实 status。"""
    if not INDEX_FILE.exists():
        return 0
    status_by_id = {c["id"]: c["status"] for c in cards}
    link_re = re.compile(r"\[\[([^\]]+)\]\]")
    out, changed = [], 0
    for line in INDEX_FILE.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("|") and "✅" in line:
            m = link_re.search(line)
            if m:
                card_id = m.group(1).split("|")[0].split("#")[0].strip()
                st = status_by_id.get(card_id)
                if st:
                    cells = line.split("|")
                    # 末尾 split 产生空串，倒数第二个才是最后一列内容
                    idx = len(cells) - 2 if cells[-1].strip() == "" else len(cells) - 1
                    if cells[idx].strip() != st:
                        cells[idx] = f" {st} "
                        line = "|".join(cells)
                        changed += 1
        out.append(line)
    INDEX_FILE.write_text("\n".join(out) + "\n", encoding="utf-8")
    return changed


def main():
    cards, warnings = collect_cards()
    check_links(warnings)
    write_json(cards)
    write_md(cards)
    changed = refresh_index(cards)

    print(f"✅ 扫描卡片 {len(cards)} 张 → registry/charts.json + registry/charts.md")
    print(f"✅ 图表类型索引.md 刷新状态单元格 {changed} 处")
    by_status = {}
    for c in cards:
        by_status[c["status"]] = by_status.get(c["status"], 0) + 1
    print("   状态分布:", ", ".join(f"{k}={v}" for k, v in sorted(by_status.items())))
    if warnings:
        print(f"\n⚠️  {len(warnings)} 条校验警告：")
        for w in warnings:
            print("  -", w)
    else:
        print("✅ 校验通过：无缺字段 / 无断链")
    return 1 if any(w.startswith(("[缺字段]", "[状态非法]")) for w in warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
