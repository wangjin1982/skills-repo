#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-.}"
OUTPUT_DIR="${2:-$TARGET_DIR/_organizer_output}"

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Target directory not found: $TARGET_DIR" >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR" 2>/dev/null || {
  OUTPUT_DIR="/tmp/folder-organizer-output-$(date +%Y%m%d_%H%M%S)"
  mkdir -p "$OUTPUT_DIR"
}

PLAN_TSV="$OUTPUT_DIR/organization_plan.tsv"
SUMMARY_MD="$OUTPUT_DIR/summary.md"

contains_ci() {
  local haystack="$1"
  local needle="$2"
  shopt -s nocasematch
  [[ "$haystack" == *"$needle"* ]]
  local res=$?
  shopt -u nocasematch
  return $res
}

classify_target() {
  local rel="$1"
  local file="$2"
  local ext="$3"
  local combined="$rel $file"

  case "$ext" in
    jpg|jpeg|png|bmp|gif|webp|mp4|mov|mkv|wmv|avi|flv|html|htm)
      echo "06_素材与多媒体/|ext:$ext"
      return
      ;;
    exe|dmg|pkg|wrf)
      echo "00_收件箱_待分类/|ext:$ext"
      return
      ;;
    hxzproj)
      echo "01_客户与项目/|ext:$ext"
      return
      ;;
  esac

  for c in 项目 客户 实施 交付 需求 接口 SOW 周报 POC 集成; do
    if contains_ci "$combined" "$c"; then
      echo "01_客户与项目/|kw:$c"
      return
    fi
  done

  for c in 产品 技术 测试 手册 API 端口 viewer; do
    if contains_ci "$combined" "$c"; then
      echo "02_产品与技术/|kw:$c"
      return
    fi
  done

  for c in 培训 研讨会 考试 题库 教育 课程 讲义 笔记; do
    if contains_ci "$combined" "$c"; then
      echo "03_培训与课程/|kw:$c"
      return
    fi
  done

  for c in 售前 咨询 商机 竞品 competitor "kick off" qbr rebranding 建议; do
    if contains_ci "$combined" "$c"; then
      echo "04_销售与咨询/|kw:$c"
      return
    fi
  done

  for c in 行政 运营 KPI 发票 报销 会议 借贷 license 合同流程; do
    if contains_ci "$combined" "$c"; then
      echo "05_运营与行政/|kw:$c"
      return
    fi
  done

  for c in 学习 数据之道 读书 课程笔记; do
    if contains_ci "$combined" "$c"; then
      echo "个人学习/|kw:$c"
      return
    fi
  done

  echo "00_收件箱_待分类/|fallback"
}

printf 'source_abs\tsource_rel\tsuggested_target\treason\tstatus\n' > "$PLAN_TSV"

while IFS= read -r -d '' path; do
  abs="$(cd "$(dirname "$path")" && pwd)/$(basename "$path")"
  rel="${path#${TARGET_DIR%/}/}"
  if [[ "$path" == "$TARGET_DIR"/* ]]; then
    :
  else
    rel="${path#./}"
  fi

  file="$(basename "$path")"
  ext=""
  [[ "$file" == *.* ]] && ext="${file##*.}"
  ext="$(printf '%s' "$ext" | tr '[:upper:]' '[:lower:]')"

  result="$(classify_target "$rel" "$file" "$ext")"
  target="${result%%|*}"
  reason="${result#*|}"
  status="ready"

  printf '%s\t%s\t%s\t%s\t%s\n' "$abs" "$rel" "$target" "$reason" "$status" >> "$PLAN_TSV"
done < <(find "$TARGET_DIR" -type f ! -path "$OUTPUT_DIR/*" -print0)

TOTAL=$(awk 'END{print NR-1}' "$PLAN_TSV")
UNMAPPED=$(awk -F '\t' 'NR>1 && $4=="fallback" {c++} END{print c+0}' "$PLAN_TSV")

{
  echo "# Organization Plan Summary"
  echo
  echo "- Target directory: $TARGET_DIR"
  echo "- Output directory: $OUTPUT_DIR"
  echo "- Total files scanned: $TOTAL"
  echo "- Fallback (to 00_收件箱_待分类): $UNMAPPED"
  echo
  echo "## Category Counts"
  awk -F '\t' 'NR>1 {c[$3]++} END{for (k in c) print "- " k " " c[k]}' "$PLAN_TSV" | sort
  echo
  echo "Plan file: $PLAN_TSV"
} > "$SUMMARY_MD"

echo "$PLAN_TSV"
echo "$SUMMARY_MD"
