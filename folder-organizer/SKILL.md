---
name: folder-organizer
description: Recursively organize files and subfolders into a standard structure, produce a dry-run reorganization plan, apply safe moves with a manifest, and generate searchable file indexes. Use when users ask to organize folders, classify materials, clean directory structures, or build file location indexes.
---

# Folder Organizer

Use this skill to整理一个目录及其所有子目录内容，并生成可检索索引。

## When To Use

- 用户要求“整理文件夹/归类资料/递归整理子文件夹”
- 用户要求“生成索引，方便查文件位置”
- 用户要求“先预览再执行移动”

## Workflow

1. Run scan and plan (dry-run first):
   - `bash scripts/scan_and_plan.sh "<target_dir>" "<output_dir>"`
2. Review output:
   - `organization_plan.tsv`
   - `summary.md`
3. Apply moves only after confirmation:
   - Dry-run: `bash scripts/apply_moves.sh "<plan_tsv>" "<target_dir>" "<manifest_tsv>"`
   - Apply: `bash scripts/apply_moves.sh --apply "<plan_tsv>" "<target_dir>" "<manifest_tsv>"`
4. Build index after moves:
   - `bash scripts/build_index.sh "<target_dir>" "<index_output_dir>"`

## Safety Rules

- Default to dry-run. Never move files before a plan exists.
- Use non-overwrite behavior and record every action in a manifest.
- If target filesystem is read-only, stop apply and only output plan/index.
- Keep unmapped files in `00_收件箱_待分类/`.

## Output Files

- `organization_plan.tsv`: proposed source -> target mapping
- `summary.md`: counts by category and unmatched summary
- `move_manifest.tsv`: actual move results
- `file_index.tsv`: searchable file index

## Classification Rules

Read `references/rules.md` for the category and keyword mapping.
