#!/usr/bin/env python3
"""Convert MOBI files to UTF-8 TXT without external ebook dependencies."""

from __future__ import annotations

import argparse
import html
import re
import struct
from pathlib import Path
from typing import Iterable


def palmdoc_decompress(data: bytes) -> bytes:
    out = bytearray()
    i = 0
    n = len(data)
    while i < n:
        c = data[i]
        i += 1

        if 1 <= c <= 8:
            out.extend(data[i : i + c])
            i += c
        elif c <= 0x7F:
            out.append(c)
        elif c >= 0xC0:
            out.append(0x20)
            out.append(c ^ 0x80)
        else:
            if i >= n:
                break
            c2 = data[i]
            i += 1
            val = (c << 8) | c2
            distance = (val >> 3) & 0x07FF
            length = (val & 0x0007) + 3
            if distance == 0:
                continue

            start = len(out) - distance
            for j in range(length):
                k = start + j
                if 0 <= k < len(out):
                    out.append(out[k])
                else:
                    break

    return bytes(out)


def extract_mobi_text(raw_mobi: bytes) -> str:
    if len(raw_mobi) < 86:
        raise ValueError("File too small to be a valid MOBI/PDB file")

    record_count = struct.unpack(">H", raw_mobi[76:78])[0]
    if record_count < 2:
        raise ValueError("Invalid MOBI record table")

    offsets = [
        struct.unpack(">L", raw_mobi[78 + i * 8 : 82 + i * 8])[0]
        for i in range(record_count)
    ]

    rec0 = raw_mobi[offsets[0] : offsets[1]]
    compression = struct.unpack(">H", rec0[0:2])[0]
    text_records = struct.unpack(">H", rec0[8:10])[0]

    chunks = []
    for i in range(1, 1 + text_records):
        if i >= len(offsets):
            break
        end = offsets[i + 1] if i + 1 < len(offsets) else len(raw_mobi)
        rec = raw_mobi[offsets[i] : end]
        if compression == 2:
            rec = palmdoc_decompress(rec)
        chunks.append(rec)

    raw_text = b"".join(chunks).decode("utf-8", errors="ignore")

    body_match = re.search(r"(?is)<body[^>]*>(.*)</body>", raw_text)
    text = body_match.group(1) if body_match else raw_text

    text = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", text)

    for pattern in (
        r"(?i)<br\s*/?>",
        r"(?i)</p\s*>",
        r"(?i)</div\s*>",
        r"(?i)</h[1-6]\s*>",
        r"(?i)<mbp:pagebreak\s*/?>",
    ):
        text = re.sub(pattern, "\n", text)

    text = re.sub(r"(?is)<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def convert_one(src: Path, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    content = extract_mobi_text(src.read_bytes())
    out.write_text(content, encoding="utf-8")


def iter_mobi_files(path: Path) -> Iterable[Path]:
    for p in sorted(path.rglob("*.mobi")):
        if p.is_file():
            yield p


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert MOBI to UTF-8 TXT")
    parser.add_argument("input", help=".mobi file path, or folder when --batch is set")
    parser.add_argument("-o", "--output", help="output .txt path for single file mode")
    parser.add_argument("--batch", action="store_true", help="convert all .mobi files under input folder")
    parser.add_argument("--out-dir", help="output directory in batch mode")
    args = parser.parse_args()

    in_path = Path(args.input).expanduser().resolve()

    if args.batch:
        if not in_path.is_dir():
            raise SystemExit(f"Input must be a directory in --batch mode: {in_path}")

        out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else in_path
        files = list(iter_mobi_files(in_path))
        if not files:
            raise SystemExit(f"No .mobi files found in: {in_path}")

        for src in files:
            if args.out_dir:
                rel = src.relative_to(in_path)
                out = (out_dir / rel).with_suffix(".txt")
            else:
                out = src.with_suffix(".txt")
            convert_one(src, out)
            print(f"OK: {src} -> {out}")
        return 0

    if not in_path.is_file() or in_path.suffix.lower() != ".mobi":
        raise SystemExit(f"Input must be a .mobi file: {in_path}")

    out = (
        Path(args.output).expanduser().resolve()
        if args.output
        else in_path.with_suffix(".txt")
    )
    convert_one(in_path, out)
    print(f"OK: {in_path} -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
