#!/usr/bin/env python3
"""Broad-coverage GitHub notifications watcher for the OSS contribution drive.

Polls `gh api notifications?all=true` (for a bot-ish account the unread cursor is
often dead — everything arrives pre-read, so we keep our own cursor) and emits one
line per thread whose `updated_at` advanced past the stored cursor. This is the
sole standing watcher: it catches a strict superset of per-PR events — issue-thread
replies (maintainer invites), mentions, PR assigns, and threads you never added to
any watchlist.

Requires the `gh` CLI authenticated as your contribution account.

State (override with env vars):
  BURN_USAGE_STATE_DIR   base dir for state         (default: ~/.burn-usage)
  NOTIF_CURSOR_FILE      cursor {thread_id: updated_at}
                         (default: $BURN_USAGE_STATE_DIR/notif-watch-cursor.json)
  NOTIF_MUTE_FILE        one `owner/repo#number` per line (# comments OK),
                         re-read every cycle; matching threads advance the cursor
                         silently — for threads GitHub keeps notifying about that
                         you can't unsubscribe from without the `notifications`
                         scope. (default: $BURN_USAGE_STATE_DIR/notif-mute.txt)
  NOTIF_POLL_SECONDS     poll interval               (default: 90)

Emits: NOTIF <reason> <repo> <type> #<num-or-?> <title>  (one line = one event)
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

STATE_DIR = Path(os.environ.get("BURN_USAGE_STATE_DIR",
                                os.path.expanduser("~/.burn-usage")))
CURSOR_FILE = Path(os.environ.get("NOTIF_CURSOR_FILE",
                                  STATE_DIR / "notif-watch-cursor.json"))
MUTE_FILE = Path(os.environ.get("NOTIF_MUTE_FILE",
                                STATE_DIR / "notif-mute.txt"))
POLL_SECONDS = int(os.environ.get("NOTIF_POLL_SECONDS", "90"))


def load_mutes() -> set:
    try:
        lines = MUTE_FILE.read_text().splitlines()
    except FileNotFoundError:
        return set()
    return {
        line.split("#", 2)[0].strip() + "#" + line.split("#", 2)[1].strip()
        for line in (l.strip() for l in lines)
        if line and not line.startswith("#") and "#" in line
    }


def load_cursor() -> dict:
    try:
        return json.loads(CURSOR_FILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_cursor(cursor: dict) -> None:
    CURSOR_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = CURSOR_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(cursor))
    tmp.replace(CURSOR_FILE)


def fetch() -> list:
    proc = subprocess.run(
        ["gh", "api", "notifications?all=true&per_page=50"],
        capture_output=True, text=True, timeout=60,
    )
    if proc.returncode != 0:
        print(f"WARN gh api failed: {proc.stderr.strip()[:200]}", file=sys.stderr)
        return []
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return []


def subject_number(subject: dict) -> str:
    url = subject.get("url") or ""
    return url.rsplit("/", 1)[-1] if url else "?"


def main() -> None:
    cursor = load_cursor()
    first_pass = not cursor  # cold start: seed silently, don't replay history
    while True:
        threads = fetch()
        mutes = load_mutes()
        dirty = False
        for t in threads:
            tid = t.get("id")
            updated = t.get("updated_at", "")
            if not tid or cursor.get(tid, "") >= updated:
                continue
            cursor[tid] = updated
            dirty = True
            if first_pass:
                continue
            subj = t.get("subject", {})
            repo_full = t.get("repository", {}).get("full_name", "?")
            if f"{repo_full}#{subject_number(subj)}" in mutes:
                continue
            print(
                f"NOTIF {t.get('reason','?')} "
                f"{t.get('repository',{}).get('full_name','?')} "
                f"{subj.get('type','?')} #{subject_number(subj)} "
                f"{subj.get('title','')[:120]}",
                flush=True,
            )
        if dirty:
            save_cursor(cursor)
        first_pass = False
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
