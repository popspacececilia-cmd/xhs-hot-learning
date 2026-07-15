#!/usr/bin/env python3
"""Scan Xiaohongshu material records and safely mark one record processed."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from pathlib import Path


URL_RE = re.compile(r"^\s*链接[：:]\s*(https?://\S+)\s*$", re.MULTILINE)
STATUS_RE = re.compile(r"^(\s*状态[：:]\s*)(.*?)(\s*)$", re.MULTILINE)
HEADING_RE = re.compile(r"(?=^###\s+)", re.MULTILINE)


def split_records(text: str) -> list[tuple[int, str]]:
    starts = [m.start() for m in HEADING_RE.finditer(text)]
    if not starts:
        return [(0, text)] if URL_RE.search(text) else []
    records: list[tuple[int, str]] = []
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(text)
        records.append((start, text[start:end]))
    return records


def parse_file(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    parsed: list[dict[str, object]] = []
    for start, record in split_records(text):
        url_match = URL_RE.search(record)
        if not url_match:
            continue
        status_match = STATUS_RE.search(record)
        status = status_match.group(2).strip() if status_match else ""
        parsed.append(
            {
                "file": str(path),
                "record_start": start,
                "url": url_match.group(1),
                "status": status,
                "pending": status != "已处理",
            }
        )
    return parsed


def command_scan(inbox_dir: Path) -> int:
    records: list[dict[str, object]] = []
    for path in sorted(inbox_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".txt", ".md", ".url"}:
            records.extend(parse_file(path))
    print(json.dumps({"records": records, "pending": [r for r in records if r["pending"]]}, ensure_ascii=False, indent=2))
    return 0


def command_mark(path: Path, url: str) -> int:
    original = path.read_text(encoding="utf-8")
    matches: list[tuple[int, str]] = []
    for start, record in split_records(original):
        url_match = URL_RE.search(record)
        if url_match and url_match.group(1) == url:
            matches.append((start, record))
    if len(matches) != 1:
        raise SystemExit(f"Refusing to update: expected one record for URL, found {len(matches)}")

    start, record = matches[0]
    status_matches = list(STATUS_RE.finditer(record))
    if len(status_matches) != 1:
        raise SystemExit(f"Refusing to update: expected one status field, found {len(status_matches)}")
    updated_record = STATUS_RE.sub(lambda m: f"{m.group(1)}已处理{m.group(3)}", record, count=1)
    updated = original[:start] + updated_record + original[start + len(record) :]

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(updated)
        temp_name = handle.name
    os.replace(temp_name, path)

    verification = path.read_text(encoding="utf-8")
    verified = [r for r in parse_file(path) if r["url"] == url and r["status"] == "已处理"]
    if len(verified) != 1 or url not in verification:
        raise SystemExit("Status update verification failed")
    print(json.dumps({"ok": True, "file": str(path), "url": url, "status": "已处理"}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    scan = subparsers.add_parser("scan")
    scan.add_argument("--inbox-dir", required=True, type=Path)
    mark = subparsers.add_parser("mark")
    mark.add_argument("--file", required=True, type=Path)
    mark.add_argument("--url", required=True)
    args = parser.parse_args()
    if args.command == "scan":
        return command_scan(args.inbox_dir)
    return command_mark(args.file, args.url)


if __name__ == "__main__":
    raise SystemExit(main())
