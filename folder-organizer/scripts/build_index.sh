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

INDEX_TSV="$OUTPUT_DIR/file_index.tsv"
NAME_INDEX_TSV="$OUTPUT_DIR/file_name_index.tsv"

printf 'file_name\trelative_path\tabs_path\ttop_level\text\tsize_bytes\tmodified\n' > "$INDEX_TSV"

while IFS= read -r -d '' path; do
  abs="$(cd "$(dirname "$path")" && pwd)/$(basename "$path")"
  rel="${path#${TARGET_DIR%/}/}"
  if [[ "$path" == "$TARGET_DIR"/* ]]; then
    :
  else
    rel="${path#./}"
  fi

  file="$(basename "$path")"
  top="(root)"
  [[ "$rel" == */* ]] && top="${rel%%/*}"
  ext=""
  [[ "$file" == *.* ]] && ext="${file##*.}"

  size="$(stat -f '%z' "$path" 2>/dev/null || echo 0)"
  mod="$(stat -f '%Sm' -t '%Y-%m-%d %H:%M:%S' "$path" 2>/dev/null || echo '')"

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$file" "$rel" "$abs" "$top" "$ext" "$size" "$mod" >> "$INDEX_TSV"
done < <(find "$TARGET_DIR" -type f ! -path "$OUTPUT_DIR/*" -print0)

{
  printf 'file_name\tcount\tpaths\n'
  awk -F '\t' 'NR>1 {c[$1]++; p[$1]=p[$1] " | " $2} END {for (k in c) printf "%s\t%s\t%s\n", k, c[k], substr(p[k],4)}' "$INDEX_TSV" | sort
} > "$NAME_INDEX_TSV"

echo "$INDEX_TSV"
echo "$NAME_INDEX_TSV"
