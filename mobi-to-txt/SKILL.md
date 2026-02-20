---
name: mobi-to-txt
description: Convert .mobi ebooks to clean UTF-8 .txt files. Use when users ask to convert mobi to txt, export mobi text, batch-convert mobi books, or recover readable text from MOBI without Calibre.
---

# MOBI to TXT

Convert MOBI files into readable UTF-8 TXT output.

## When to use

Use this skill when the user asks to:
- convert `.mobi` to `.txt`
- batch convert MOBI books
- extract readable text from MOBI without external ebook tools

## Workflow

1. Confirm source path(s) and output location.
2. Run the bundled converter script.
3. Verify generated file exists and provide output path(s).

## Commands

Single file:

```bash
python3 scripts/mobi_to_txt.py "/path/to/book.mobi"
```

Custom output path:

```bash
python3 scripts/mobi_to_txt.py "/path/to/book.mobi" -o "/path/to/book.txt"
```

Batch conversion:

```bash
python3 scripts/mobi_to_txt.py "/path/to/folder" --batch
```

Batch with output directory:

```bash
python3 scripts/mobi_to_txt.py "/path/to/folder" --batch --out-dir "/path/to/output"
```

## Notes

- Output is UTF-8 text.
- The script handles PalmDOC-compressed MOBI.
- If conversion quality is poor for a specific file, prefer `ebook-convert` when available.
