#!/usr/bin/env bash
set -euo pipefail

APPLY=0
if [[ "${1:-}" == "--apply" ]]; then
  APPLY=1
  shift
fi

PLAN_TSV="${1:-}"
TARGET_ROOT="${2:-}"
MANIFEST_TSV="${3:-}"

if [[ -z "$PLAN_TSV" || -z "$TARGET_ROOT" || -z "$MANIFEST_TSV" ]]; then
  echo "Usage: bash apply_moves.sh [--apply] <plan_tsv> <target_root> <manifest_tsv>" >&2
  exit 1
fi

if [[ ! -f "$PLAN_TSV" ]]; then
  echo "Plan file not found: $PLAN_TSV" >&2
  exit 1
fi

if [[ ! -d "$TARGET_ROOT" ]]; then
  echo "Target root not found: $TARGET_ROOT" >&2
  exit 1
fi

mkdir -p "$(dirname "$MANIFEST_TSV")"
printf 'timestamp\tmode\tsource_abs\tdest_abs\tresult\tnote\n' > "$MANIFEST_TSV"

if [[ $APPLY -eq 1 ]]; then
  TEST_FILE="$TARGET_ROOT/.folder_organizer_write_test"
  if ! touch "$TEST_FILE" 2>/dev/null; then
    echo "Target filesystem is read-only: $TARGET_ROOT" >&2
    exit 2
  fi
  rm -f "$TEST_FILE"
fi

while IFS=$'\t' read -r source_abs source_rel suggested_target reason status; do
  [[ "$source_abs" == "source_abs" ]] && continue

  dest_dir="$TARGET_ROOT/$suggested_target"
  file_name="$(basename "$source_abs")"
  dest_abs="$dest_dir/$file_name"
  ts="$(date '+%Y-%m-%d %H:%M:%S')"

  if [[ ! -e "$source_abs" ]]; then
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$ts" "$([[ $APPLY -eq 1 ]] && echo apply || echo dry-run)" "$source_abs" "$dest_abs" "skip" "source_missing" >> "$MANIFEST_TSV"
    continue
  fi

  if [[ $APPLY -eq 0 ]]; then
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$ts" "dry-run" "$source_abs" "$dest_abs" "planned" "$reason" >> "$MANIFEST_TSV"
    continue
  fi

  mkdir -p "$dest_dir"

  if [[ -e "$dest_abs" ]]; then
    stem="${file_name%.*}"
    ext=""
    [[ "$file_name" == *.* ]] && ext=".${file_name##*.}"
    dest_abs="$dest_dir/${stem}_$(date '+%Y%m%d_%H%M%S')$ext"
  fi

  if mv "$source_abs" "$dest_abs"; then
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$ts" "apply" "$source_abs" "$dest_abs" "moved" "$reason" >> "$MANIFEST_TSV"
  else
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$ts" "apply" "$source_abs" "$dest_abs" "failed" "mv_error" >> "$MANIFEST_TSV"
  fi
done < "$PLAN_TSV"

echo "$MANIFEST_TSV"
