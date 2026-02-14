---
name: version-backup
description: "Use when user wants to save a version snapshot, backup current work state, restore previous version, or manage work checkpoints. Supports creating versioned backups with descriptions, listing all versions, and restoring to any saved version."
version: 1.0.0
---

# Version Backup

Save and restore working state snapshots for long-running tasks.

## Implementation

This skill uses a bash script located at `~/.agents/skills/version-backup/bin/version-backup.sh`.
The script is symlinked to `~/.local/bin/version-backup` for easy access.

**Note**: Make sure `~/.local/bin` is in your PATH. The skill installation should have added:
```bash
export PATH="$HOME/.local/bin:$PATH"
```
to your `~/.zshrc`. If `version-backup` command is not found, run:
```bash
source ~/.zshrc
```

## When to Use

Use this skill when user asks to:
- "Save current version"
- "Create a backup"
- "Checkpoint my work"
- "Restore to previous version"
- "List all versions"
- "Rollback to version X"

## Storage Structure

```
{project-root}/.versions/
├── index.json              # Version metadata index
├── 2025-02-12_143022/      # Version directory (timestamp)
│   ├── meta.json           # Version metadata
│   └── files/              # Backed up files
│       ├── src/
│       ├── package.json
│       └── ...
└── 2025-02-12_150834/
    ├── meta.json
    └── files/
```

## Metadata Schema

### index.json
```json
{
  "versions": [
    {
      "id": "2025-02-12_143022",
      "timestamp": "2025-02-12T14:30:22+08:00",
      "description": "Before refactoring auth module",
      "tags": ["pre-refactor", "auth"],
      "file_count": 15,
      "size_bytes": 245760
    }
  ]
}
```

### meta.json (per version)
```json
{
  "id": "2025-02-12_143022",
  "timestamp": "2025-02-12T14:30:22+08:00",
  "description": "Before refactoring auth module",
  "tags": ["pre-refactor", "auth"],
  "files": [
    {"path": "src/auth.js", "size": 2048, "checksum": "abc123"},
    {"path": "src/auth.test.js", "size": 1024, "checksum": "def456"}
  ],
  "cwd": "/Users/user/project",
  "branch": "main",
  "commit": "a1b2c3d"
}
```

## Commands

**All commands are executed via the `version-backup` bash script.**

### 1. Create Version

```bash
version-backup save "description here" [--tags tag1,tag2] [--files path1,path2]
```

**Examples:**
```bash
# Backup entire project
version-backup save "Before refactoring auth module"

# Backup with tags
version-backup save "API changes" --tags api,feature

# Backup specific files only
version-backup save "Config changes" --files config/,.env
```

**Behavior**:
- Default: Backup entire project (excluding .versions/, node_modules/, .git/)
- With --files: Backup only specified files/directories
- Timestamp auto-generated (YYYY-MM-DD_HHMMSS format)
- Calculate file checksums for integrity verification
- Update index.json

### 2. List Versions

```bash
version-backup list [--detail]
```

**Output format**:
```
ID              Timestamp              Description               Tags
2025-02-12_15   2025-02-12 15:08:34    After API refactor        api,refactor
2025-02-12_14   2025-02-12 14:30:22    Before refactoring auth   pre-refactor,auth
```

With --detail: Show file count, size, git info

### 3. Restore Version

```bash
version-backup restore <version-id> [--dry-run] [--force]
```

**Behavior**:
- --dry-run: Show what would change without actually restoring
- --force: Skip confirmation prompt
- **SAFETY**: Creates pre-restore backup automatically
- Overwrites files with backed up versions
- Report restored file count

### 4. Delete Version

```bash
version-backup delete <version-id>
```

**Behavior**:
- Requires confirmation
- Removes version directory
- Updates index.json

### 5. Compare Versions

```bash
version-backup compare <version-id-1> <version-id-2>
```

**Behavior**:
- Show files added/removed/modified
- File size differences
- Summary of changes

### 6. Export/Import

```bash
version-backup export <version-id> [--output archive.tar.gz]
version-backup import <archive.tar.gz>
```

**Behavior**:
- Export: Create portable archive of a version
- Import: Restore from archive to any project

## Default Exclusions

When creating backups, automatically exclude:
- `.versions/` - Don't backup backups
- `node_modules/` - Dependencies can be reinstalled
- `.git/` - Version control already handles this
- `dist/`, `build/`, `*.egg-info/` - Build artifacts
- `__pycache__/`, `*.pyc` - Python cache
- `.DS_Store`, `Thumbs.db` - OS files
- `*.log` - Log files

User can override with `--include` flag.

## File Operations

### Copying Files
Use `cp -r` or `rsync -a` for recursive copy with permissions preserved:
```bash
rsync -a --exclude='node_modules' --exclude='.git' \
  project/ .versions/{timestamp}/files/
```

### Checksum Calculation
```bash
shasum file.txt  # or sha256sum on Linux
```

### Integrity Verification
```bash
# Verify backup integrity
version-backup verify <version-id>
```

## Error Handling

| Scenario | Action |
|----------|--------|
| Missing .versions/ | Auto-create directory |
| Corrupted index.json | Rebuild from version directories |
| Missing files during restore | Warning, continue with available files |
| Disk space low | Error message with required space |
| Version already exists | Error + suggest new description |

## Safety Features

1. **Pre-restore backup**: Always create backup before restoring
2. **Dry-run mode**: Preview changes before committing
3. **Confirmation prompts**: Require user confirmation for destructive operations
4. **Checksum verification**: Detect corrupted backups
5. **Index validation**: Rebuild index if corrupted

## Usage Examples

### Scenario 1: Before Major Refactor
```bash
version-backup save "Before refactoring authentication module" --tags auth,pre-refactor
# Output: Version 2025-02-12_143022 created with 15 files
```

### Scenario 2: Restore After Failed Experiment
```bash
version-backup list
# User picks version ID
version-backup restore 2025-02-12_143022 --dry-run
# Review changes, then:
version-backup restore 2025-02-12_143022
```

### Scenario 3: Backup Specific Files
```bash
version-backup save "API endpoint changes" --files src/api/,src/routes/api.js
```

### Scenario 4: Clean Old Versions
```bash
version-backup list
version-backup delete 2025-02-10_090000  # Delete old version
```

## Implementation Notes

- Use `date +%Y-%m-%d_%H%M%S` for timestamp generation
- Store index.json as canonical source of truth
- Version directories: `{timestamp}` as folder name
- Lock file `.versions/.lock` for concurrent access safety
- Use atomic file operations (write to temp, then move)

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Version not found |
| 3 | Insufficient disk space |
| 4 | Corrupted backup |
| 5 | Interrupted by user |
