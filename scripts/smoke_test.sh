#!/usr/bin/env bash
# 冒烟测试：用默认参数跑全部 templates/，校验每个模板都产出非空 PNG+PDF。
# 改完任何模板或 _common 后必跑。用法： bash scripts/smoke_test.sh
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PY="${SCIPLOT_PY:-/opt/anaconda3/envs/viz/bin/python}"
OUT="$(mktemp -d)"
export SCIPLOT_OUT="$OUT"
pass=0; fail=0; fails=""

check() {  # check <name> —— 校验 <name>.png 与 <name>.pdf 存在且非空
  local n="$1" ok=1
  for ext in png pdf; do
    [ -s "$OUT/$n.$ext" ] || ok=0
  done
  return $((1 - ok))
}

run() {  # run <label> <cmd...>
  local label="$1"; shift
  printf "%-22s " "$label"
  local log; log="$("$@" 2>&1)"
  # 模板里 NAME 决定输出名；从输出 "-> NAME" 抓取
  local name; name="$(printf '%s\n' "$log" | sed -n 's/.*-> \([A-Za-z0-9_]*\) .*/\1/p' | tail -1)"
  if [ -n "$name" ] && check "$name"; then
    echo "OK   ($name)"; pass=$((pass+1))
  else
    echo "FAIL"; fail=$((fail+1)); fails="$fails $label"
    printf '%s\n' "$log" | tail -3 | sed 's/^/    /'
  fi
}

echo "== Python 模板 (=$PY) =="
for f in "$REPO"/templates/python/*.py; do
  [ "$(basename "$f")" = "_common.py" ] && continue
  run "py/$(basename "$f")" "$PY" "$f"
done

echo "== R 模板 (Rscript) =="
if command -v Rscript >/dev/null 2>&1; then
  for f in "$REPO"/templates/r/*.R; do
    [ "$(basename "$f")" = "_common.R" ] && continue
    run "r/$(basename "$f")" Rscript "$f"
  done
else
  echo "  (跳过：未找到 Rscript)"
fi

echo "----------------------------------------"
echo "通过 ${pass}，失败 ${fail}"
[ -n "$fails" ] && echo "失败项:${fails}"
rm -rf "$OUT"
[ "$fail" -eq 0 ]
