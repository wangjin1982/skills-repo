#!/usr/bin/env bash
# version-backup - Save and restore working state snapshots

set -euo pipefail

VERSIONS_DIR=".versions"
INDEX_FILE="$VERSIONS_DIR/index.json"
LOCK_FILE="$VERSIONS_DIR/.lock"
TIMESTAMP_FORMAT="%Y-%m-%d_%H%M%S"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default exclusions
DEFAULT_EXCLUSIONS=(
  "$VERSIONS_DIR"
  "node_modules"
  ".git"
  "dist"
  "build"
  "*.egg-info"
  "__pycache__"
  "*.pyc"
  ".DS_Store"
  "Thumbs.db"
  "*.log"
)

# Logging functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Acquire lock
acquire_lock() {
  # Create versions dir first if it doesn't exist
  mkdir -p "$VERSIONS_DIR"

  if [ -f "$LOCK_FILE" ]; then
    local lock_pid=$(cat "$LOCK_FILE" 2>/dev/null || echo "")
    if ps -p "$lock_pid" >/dev/null 2>&1; then
      log_error "Another version-backup process is running (PID: $lock_pid)"
      exit 1
    fi
    log_warn "Removing stale lock file"
    rm -f "$LOCK_FILE"
  fi
  echo $$ > "$LOCK_FILE"
  trap 'rm -f "$LOCK_FILE"' EXIT
}

# Ensure versions directory exists
ensure_versions_dir() {
  if [ ! -d "$VERSIONS_DIR" ]; then
    mkdir -p "$VERSIONS_DIR"
  fi
  if [ ! -f "$INDEX_FILE" ]; then
    echo '{"versions":[]}' > "$INDEX_FILE"
    log_info "Created index file"
  fi
}

# Generate timestamp
get_timestamp() {
  date +"$TIMESTAMP_FORMAT"
}

# Get ISO 8601 timestamp
get_iso_timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# Build rsync exclude patterns
build_excludes() {
  local excludes=()
  for pattern in "${DEFAULT_EXCLUSIONS[@]}"; do
    excludes+=("--exclude=$pattern")
  done
  echo "${excludes[@]}"
}

# Calculate file checksum
get_checksum() {
  local file="$1"
  if command -v shasum >/dev/null 2>&1; then
    shasum "$file" | cut -d' ' -f1
  else
    sha256sum "$file" | cut -d' ' -f1
  fi
}

# Get git info
get_git_info() {
  if git rev-parse --git-dir >/dev/null 2>&1; then
    local branch=$(git branch --show-current 2>/dev/null || echo "unknown")
    local commit=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    echo "\"branch\": \"$branch\", \"commit\": \"$commit\""
  else
    echo "\"branch\": null, \"commit\": null"
  fi
}

# Update index file
update_index() {
  local version_id="$1"
  local meta_file="$VERSIONS_DIR/$version_id/meta.json"

  if [ ! -f "$meta_file" ]; then
    log_error "Metadata file not found: $meta_file"
    return 1
  fi

  # Read metadata
  local description=$(jq -r '.description' "$meta_file")
  local timestamp=$(jq -r '.timestamp' "$meta_file")
  local tags=$(jq -r '.tags | join(",")' "$meta_file")
  local file_count=$(jq -r '.files | length' "$meta_file")
  local size=$(jq -r '.total_size' "$meta_file")

  # Update index
  jq --arg id "$version_id" \
     --arg ts "$timestamp" \
     --arg desc "$description" \
     --arg tags "$tags" \
     --argjson fc "$file_count" \
     --argjson size "$size" \
     '.versions += [{id: $id, timestamp: $ts, description: $desc, tags: ($tags | split(",")), file_count: $fc, size_bytes: $size}]' \
     "$INDEX_FILE" > "$INDEX_FILE.tmp"

  mv "$INDEX_FILE.tmp" "$INDEX_FILE"
}

# Command: Save
cmd_save() {
  shift  # Remove "save" from args
  local description="${1:-}"
  shift
  local tags=""
  local files=()

  while [[ $# -gt 0 ]]; do
    case $1 in
      --tags)
        tags="$2"
        shift 2
        ;;
      --files)
        IFS=',' read -ra files <<< "$2"
        shift 2
        ;;
      *)
        log_error "Unknown option: $1"
        exit 1
        ;;
    esac
  done

  if [ -z "$description" ]; then
    log_error "Description is required"
    echo "Usage: version-backup save \"description\" [--tags tag1,tag2] [--files path1,path2]"
    exit 1
  fi

  acquire_lock
  ensure_versions_dir

  local version_id=$(get_timestamp)
  local version_dir="$VERSIONS_DIR/$version_id"
  local files_dir="$version_dir/files"

  mkdir -p "$files_dir"

  log_info "Creating version: $version_id"
  log_info "Description: $description"

  # Copy files
  if [ ${#files[@]} -eq 0 ]; then
    # Backup entire project
    local excludes=$(build_excludes)
    eval "rsync -a $excludes ./ \"$files_dir/\""
  else
    # Backup specific files
    for file in "${files[@]}"; do
      if [ -e "$file" ]; then
        mkdir -p "$files_dir/$(dirname "$file")"
        cp -r "$file" "$files_dir/$file"
        log_info "Backed up: $file"
      else
        log_warn "File not found: $file"
      fi
    done
  fi

  # Calculate file metadata
  local file_metadata="["
  local first=true
  local total_size=0

  while IFS= read -r -d '' file; do
    local rel_path="${file#$files_dir/}"
    local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0)
    total_size=$((total_size + size))

    if [ "$first" = true ]; then
      first=false
    else
      file_metadata+=","
    fi

    file_metadata+="{\"path\":\"$rel_path\",\"size\":$size}"
  done < <(find "$files_dir" -type f -print0)

  file_metadata+="]"

  # Create metadata
  local file_count=$(echo "$file_metadata" | jq 'length')
  local iso_ts=$(get_iso_timestamp)

  cat > "$version_dir/meta.json" <<EOF
{
  "id": "$version_id",
  "timestamp": "$iso_ts",
  "description": "$description",
  "tags": $(echo "$tags" | jq -R 'split(",") | map(select(length > 0))'),
  "files": $file_metadata,
  "total_size": $total_size,
  "cwd": "$(pwd)",
  $(get_git_info)
}
EOF

  log_info "Version created with $file_count files ($((total_size / 1024)) KB)"

  # Update index
  update_index "$version_id"
}

# Command: List
cmd_list() {
  local detail="${1:-}"

  if [ ! -f "$INDEX_FILE" ]; then
    log_warn "No versions found"
    return
  fi

  if [ "$detail" = "--detail" ]; then
    jq -r '.versions | reverse | .[] |
      "\(.id)\t\(.timestamp)\t\(.description)\t\(.tags | join(","))\t\(.file_count) files\t\(.size_bytes) bytes"' \
      "$INDEX_FILE" | column -t -s $'\t'
  else
    printf "%-16s  %-20s  %-30s  %-20s\n" "ID" "Timestamp" "Description" "Tags"
    printf "%s\n" "$(str_repeat '-' 90)"
    jq -r '.versions | reverse | .[] |
      "\(.id[0:16])  \(.timestamp[0:19])  \(.description[0:28])  \(.tags | join(","))"' \
      "$INDEX_FILE" 2>/dev/null || echo "No versions found"
  fi
}

# Command: Restore
cmd_restore() {
  shift  # Remove "restore" from args
  local version_id="${1:-}"
  shift
  local dry_run=false
  local force=false

  while [[ $# -gt 0 ]]; do
    case $1 in
      --dry-run)
        dry_run=true
        shift
        ;;
      --force)
        force=true
        shift
        ;;
      *)
        log_error "Unknown option: $1"
        exit 1
        ;;
    esac
  done

  local version_dir="$VERSIONS_DIR/$version_id"

  if [ ! -d "$version_dir" ]; then
    log_error "Version not found: $version_id"
    exit 2
  fi

  # Get description
  local desc=$(jq -r '.description' "$version_dir/meta.json")

  log_info "Restoring version: $version_id"
  log_info "Description: $desc"

  if [ "$dry_run" = true ]; then
    log_info "DRY RUN - files that would be restored:"
    find "$version_dir/files" -type f | sed "s|$version_dir/files/|  -> |"
    return 0
  fi

  # Create pre-restore backup
  if [ "$force" != true ]; then
    log_warn "This will overwrite current files. Creating pre-restore backup..."
    local backup_id="pre-restore-$(get_timestamp)"
    mkdir -p "$VERSIONS_DIR/$backup_id/files"
    eval "rsync -a $(build_excludes) ./ \"$VERSIONS_DIR/$backup_id/files/" 2>/dev/null || true
    log_info "Pre-restore backup: $backup_id"

    read -p "Continue with restore? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      log_info "Restore cancelled"
      return 0
    fi
  fi

  # Restore files
  rsync -a --delete "$version_dir/files/" ./
  log_info "Restore complete"
}

# Command: Delete
cmd_delete() {
  local version_id="$1"
  local version_dir="$VERSIONS_DIR/$version_id"

  if [ ! -d "$version_dir" ]; then
    log_error "Version not found: $version_id"
    exit 2
  fi

  local desc=$(jq -r '.description' "$version_dir/meta.json")
  log_warn "Deleting version: $version_id"
  log_warn "Description: $desc"

  read -p "Are you sure? [y/N] " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    log_info "Delete cancelled"
    return 0
  fi

  rm -rf "$version_dir"

  # Update index
  jq --arg id "$version_id" '.versions |= map(select(.id != $id))' \
    "$INDEX_FILE" > "$INDEX_FILE.tmp"
  mv "$INDEX_FILE.tmp" "$INDEX_FILE"

  log_info "Version deleted"
}

# Command: Compare
cmd_compare() {
  local version1="$1"
  local version2="$2"

  local dir1="$VERSIONS_DIR/$version1/files"
  local dir2="$VERSIONS_DIR/$version2/files"

  if [ ! -d "$dir1" ] || [ ! -d "$dir2" ]; then
    log_error "One or both versions not found"
    exit 2
  fi

  echo "Comparing $version1 vs $version2"
  echo ""

  echo "Files only in $version1:"
  comm -23 <(cd "$dir1" && find . -type f | sort) \
           <(cd "$dir2" && find . -type f | sort) | sed 's/^/  /' || echo "  (none)"

  echo ""
  echo "Files only in $version2:"
  comm -13 <(cd "$dir1" && find . -type f | sort) \
           <(cd "$dir2" && find . -type f | sort) | sed 's/^/  /' || echo "  (none)"
}

# Command: Export
cmd_export() {
  local version_id="$1"
  local output="${2:-${version_id}.tar.gz}"

  local version_dir="$VERSIONS_DIR/$version_id"

  if [ ! -d "$version_dir" ]; then
    log_error "Version not found: $version_id"
    exit 2
  fi

  log_info "Exporting version: $version_id"
  tar -czf "$output" -C "$VERSIONS_DIR" "$version_id"
  log_info "Exported to: $output"
}

# Command: Import
cmd_import() {
  local archive="$1"

  if [ ! -f "$archive" ]; then
    log_error "Archive not found: $archive"
    exit 2
  fi

  ensure_versions_dir

  log_info "Importing from: $archive"
  tar -xzf "$archive" -C "$VERSIONS_DIR"

  # Find imported version
  local imported_dir=$(tar -tzf "$archive" | head -1 | cut -d'/' -f1)
  local version_id=$(basename "$imported_dir")

  # Update index
  if [ -f "$VERSIONS_DIR/$version_id/meta.json" ]; then
    update_index "$version_id"
  fi

  log_info "Imported version: $version_id"
}

# Command: Verify
cmd_verify() {
  local version_id="$1"
  local version_dir="$VERSIONS_DIR/$version_id"

  if [ ! -d "$version_dir" ]; then
    log_error "Version not found: $version_id"
    exit 2
  fi

  log_info "Verifying version: $version_id"

  local meta="$version_dir/meta.json"
  local files_dir="$version_dir/files"

  # Check metadata
  if [ ! -f "$meta" ]; then
    log_error "Metadata file missing!"
    return 1
  fi

  # Verify files
  local corrupt=0
  local file_count=$(jq -r '.files | length' "$meta")

  log_info "Checking $file_count files..."

  jq -r '.files[].path' "$meta" | while read -r path; do
    local file="$files_dir/$path"
    if [ ! -f "$file" ]; then
      log_error "Missing file: $path"
      corrupt=1
    fi
  done

  if [ $corrupt -eq 0 ]; then
    log_info "All files verified"
  else
    log_error "Some files are corrupted or missing"
    return 4
  fi
}

# Helper: Repeat string
str_repeat() {
  local str="$1"
  local num="$2"
  printf "%${num}s" | tr ' ' "$str"
}

# Main
case "${1:-}" in
  save)
    cmd_save "$@"
    ;;
  list|ls)
    cmd_list "${2:-}" "${3:-}"
    ;;
  restore|res)
    cmd_restore "$@"
    ;;
  delete|del|rm)
    cmd_delete "${2:-}"
    ;;
  compare|diff)
    cmd_compare "${2:-}" "${3:-}"
    ;;
  export)
    cmd_export "${2:-}" "${3:-}"
    ;;
  import)
    cmd_import "${2:-}"
    ;;
  verify)
    cmd_verify "${2:-}"
    ;;
  *)
    echo "version-backup - Save and restore working state snapshots"
    echo ""
    echo "Usage:"
    echo "  version-backup save \"description\" [--tags tag1,tag2] [--files path1,path2]"
    echo "  version-backup list [--detail]"
    echo "  version-backup restore <version-id> [--dry-run] [--force]"
    echo "  version-backup delete <version-id>"
    echo "  version-backup compare <version-id-1> <version-id-2>"
    echo "  version-backup export <version-id> [--output archive.tar.gz]"
    echo "  version-backup import <archive.tar.gz>"
    echo "  version-backup verify <version-id>"
    exit 1
    ;;
esac
