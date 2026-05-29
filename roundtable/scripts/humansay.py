#!/usr/bin/env python3
"""Create a human message in a file-system roundtable."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


MESSAGE_RE = re.compile(r"^(\d+)-([a-z0-9_-]+)\.md$")


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def list_message_numbers(messages_dir: Path) -> list[int]:
    numbers: list[int] = []
    if not messages_dir.exists():
        return numbers
    for path in messages_dir.iterdir():
        match = MESSAGE_RE.match(path.name)
        if match:
            numbers.append(int(match.group(1)))
    return sorted(numbers)


def read_message(args: argparse.Namespace) -> str:
    if args.file:
        return Path(args.file).read_text(encoding="utf-8").strip()
    if args.message:
        return " ".join(args.message).strip()
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    fail("provide a message argument, --file, or stdin")


def main() -> None:
    parser = argparse.ArgumentParser(description="Post a human message to .roundtable/messages")
    parser.add_argument("--root", default=".", help="project root containing .roundtable")
    parser.add_argument("--file", help="read the human message from a file")
    parser.add_argument("message", nargs="*", help="human message text")
    args = parser.parse_args()

    content = read_message(args)
    if not content:
        fail("human message is empty")

    table = Path(args.root).resolve() / ".roundtable"
    messages_dir = table / "messages"
    messages_dir.mkdir(parents=True, exist_ok=True)

    numbers = list_message_numbers(messages_dir)
    next_num = (numbers[-1] + 1) if numbers else 1
    target = messages_dir / f"{next_num:04d}-human.md"
    if target.exists():
        fail(f"target already exists: {target}")

    created_at = datetime.now(timezone.utc).isoformat()
    body = f"---\nspeaker: human\ncreated_at: {created_at}\n---\n\n{content}\n"

    target.write_text(body, encoding="utf-8")
    print(f"Posted {target}")


if __name__ == "__main__":
    main()
