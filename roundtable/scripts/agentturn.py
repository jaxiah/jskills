#!/usr/bin/env python3
"""Helper for agent participation in a file-system roundtable."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


AGENT_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
MESSAGE_RE = re.compile(r"^(\d+)-([a-z0-9_-]+)\.md$")


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def normalize_agent(agent: str) -> str:
    agent = agent.strip().lower()
    if not agent:
        fail("--agent is required")
    if not AGENT_RE.match(agent):
        fail("--agent must match [a-z0-9][a-z0-9_-]*")
    return agent


def roundtable_root(root: Path) -> Path:
    return root / ".roundtable"


def ensure_dirs(table: Path) -> None:
    (table / "messages").mkdir(parents=True, exist_ok=True)
    (table / "drafts").mkdir(parents=True, exist_ok=True)
    (table / "state").mkdir(parents=True, exist_ok=True)


def list_messages(table: Path) -> list[tuple[int, str, Path]]:
    messages_dir = table / "messages"
    if not messages_dir.exists():
        return []

    messages: list[tuple[int, str, Path]] = []
    for path in messages_dir.iterdir():
        match = MESSAGE_RE.match(path.name)
        if match:
            messages.append((int(match.group(1)), match.group(2), path))
    return sorted(messages, key=lambda item: item[0])


def state_path(table: Path, agent: str) -> Path:
    return table / "state" / f"{agent}.json"


def read_last_read(table: Path, agent: str) -> int:
    path = state_path(table, agent)
    if not path.exists():
        return 0
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        fail(f"invalid state file: {path}")
    return int(data.get("last_read", 0))


def write_last_read(table: Path, agent: str, last_read: int) -> None:
    path = state_path(table, agent)
    data = {
        "agent": agent,
        "last_read": last_read,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def command_read(args: argparse.Namespace) -> None:
    agent = normalize_agent(args.agent)
    table = roundtable_root(Path(args.root).resolve())
    ensure_dirs(table)

    last_read = read_last_read(table, agent)
    messages = list_messages(table)
    new_messages = [(num, speaker, path) for num, speaker, path in messages if num > last_read]

    if not new_messages:
        print("No new tabletop messages.")
        return

    for num, speaker, path in new_messages:
        print(f"\n--- {num:04d}-{speaker}.md ---")
        print(path.read_text(encoding="utf-8").rstrip())

    write_last_read(table, agent, max(num for num, _, _ in new_messages))


def command_post(args: argparse.Namespace) -> None:
    agent = normalize_agent(args.agent)
    table = roundtable_root(Path(args.root).resolve())
    ensure_dirs(table)

    draft = table / "drafts" / f"{agent}.md"
    if not draft.exists():
        fail(f"draft not found: {draft}")

    content = draft.read_text(encoding="utf-8").strip()
    if not content:
        fail(f"draft is empty: {draft}")

    messages = list_messages(table)
    next_num = (messages[-1][0] + 1) if messages else 1
    target = table / "messages" / f"{next_num:04d}-{agent}.md"
    if target.exists():
        fail(f"target already exists: {target}")

    created_at = datetime.now(timezone.utc).isoformat()
    body = f"---\nspeaker: {agent}\ncreated_at: {created_at}\n---\n\n{content}\n"

    draft.write_text(body, encoding="utf-8")
    draft.replace(target)
    write_last_read(table, agent, next_num)
    print(f"Posted {target}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Roundtable helper for agents")
    parser.add_argument("--root", default=".", help="project root containing .roundtable")
    parser.add_argument("--agent", required=True, help="agent identity for this turn")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("read", help="read unread tabletop messages")
    subparsers.add_parser("post", help="move this agent's draft to the tabletop")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "read":
        command_read(args)
    elif args.command == "post":
        command_post(args)
    else:
        fail(f"unknown command: {args.command}")


if __name__ == "__main__":
    main()
