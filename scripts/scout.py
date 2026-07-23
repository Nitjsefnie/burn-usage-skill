#!/usr/bin/env python3
"""Scout freshly-ACTIVE repos worth a one-PR probe.

Signal stack (each candidate must clear all of them):
  1. good-first-issue supply: repos with >=N such issues (gh search repos).
  2. Freshness: repo updated within DAYS days AND at least one issue
     created within DAYS days (a maintainer writing issues now is present now).
  3. Backlog red flag: many stale EXTERNAL open PRs means outsiders' work rots
     -> skip. Maintainers' own WIP is fine.
  4. Not in the known-orbit exclusion list (already probed/frozen/dropped).

Output: ranked shortlist with the evidence per repo. Read-only; vetting the
issue TEXT (specificity, runnability, CLA/assignment gates in CONTRIBUTING)
and the AI/interaction policy stays the lead's job before any dispatch (see
SKILL.md rule 3 — policy verification is a judgment-capable agent job, NOT a
substring grep, so this script deliberately does not attempt it).

Requires the `gh` CLI authenticated as your contribution account.

Exclusion list: repos/owners already probed, frozen, or dropped — plus your own
account and orgs. Seed it from a file (one owner login per line, lowercase,
# comments OK):
  SCOUT_EXCLUDE_FILE   default: $BURN_USAGE_STATE_DIR/scout-exclude.txt
                       (or ~/.burn-usage/scout-exclude.txt)
Keeping it current is what stops the scout re-surfacing repos you've dispatched.

Usage: scout.py [--days 3] [--min-gfi 2] [--stars 0..20] [--limit 40]
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import pathlib
import sys

STATE_DIR = pathlib.Path(os.environ.get(
    "BURN_USAGE_STATE_DIR", os.path.expanduser("~/.burn-usage")))
EXCLUDE_FILE = pathlib.Path(os.environ.get(
    "SCOUT_EXCLUDE_FILE", STATE_DIR / "scout-exclude.txt"))


def load_excludes() -> set:
    """Owner logins to skip (yours, and every repo already probed/frozen/dropped).
    Lowercase, one per line, # comments OK. Missing file -> empty set."""
    try:
        lines = EXCLUDE_FILE.read_text().splitlines()
    except FileNotFoundError:
        return set()
    return {l.strip().lower() for l in lines
            if l.strip() and not l.strip().startswith("#")}


def sh(args):
    r = subprocess.run(args, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        print(f"WARN: {' '.join(args[:4])}...: {r.stderr[:150]}", file=sys.stderr)
        return None
    return r.stdout


def jq(args):
    out = sh(args)
    return json.loads(out) if out else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=3)
    ap.add_argument("--min-gfi", type=int, default=2)
    # help the small guys, not the giants: keep the low star band, loosen --min-gfi
    # when a sweep comes up dry (see SKILL.md "Picking work").
    ap.add_argument("--stars", default="0..20")
    ap.add_argument("--limit", type=int, default=40)
    args = ap.parse_args()

    exclude_owners = load_excludes()
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=args.days))
    since_date = since.strftime("%Y-%m-%d")

    repos = jq(["gh", "search", "repos",
                "--good-first-issues", f">{args.min_gfi - 1}",
                "--updated", f">{since_date}",
                "--stars", args.stars,
                "--archived=false",
                "--include-forks=false",
                "--sort", "updated",
                "--limit", str(args.limit),
                "--json", "fullName,stargazersCount,language,updatedAt,description"]) or []

    kept = []
    for r in repos:
        nwo = r["fullName"]
        owner = nwo.split("/")[0].lower()
        if owner in exclude_owners:
            continue

        # Fresh-issue pulse: any issue created in the window?
        pulse = jq(["gh", "search", "issues", "--repo", nwo,
                    "--created", f">{since_date}", "--limit", "1",
                    "--json", "createdAt"])
        if not pulse:
            continue

        # Backlog red flag: stale external open PRs.
        prs = jq(["gh", "pr", "list", "-R", nwo, "--state", "open",
                  "--limit", "50", "--json", "createdAt,author"]) or []
        ext_stale = sum(1 for p in prs
                        if p["author"]["login"].lower() != owner
                        and not p["author"]["login"].endswith("[bot]")
                        and p["createdAt"] < (since - dt.timedelta(days=11)).isoformat())
        if ext_stale >= 3:
            print(f"  skip {nwo}: {ext_stale} stale external PRs (red flag)",
                  file=sys.stderr)
            continue

        # NOTE: AI/human-interaction policy is NOT verified here.
        # Substring-matching CONTRIBUTING for "no ai"/"ai-generated" is wrong:
        # (1) the rule can live anywhere (one real case buried a human-only-comments
        #     convention in docs/developing/conventions.md, never in CONTRIBUTING);
        #     and
        # (2) AI/LLM policy language can be POSITIVE ("AI assistance is welcome") as
        #     easily as a ban, so a substring can't judge it.
        # Policy verification is a pick-time AGENT job that greps the whole policy
        # surface and interprets it — see SKILL.md rule 3.

        gfi = jq(["gh", "issue", "list", "-R", nwo, "--state", "open",
                  "--label", "good first issue", "--limit", "30",
                  "--json", "number,title,assignees,body"]) or []
        unassigned = [i for i in gfi if not i["assignees"]]
        if len(unassigned) < args.min_gfi:
            continue

        # Issue-text vetting: score specificity, sniff claim ceremonies.
        def spec_score(body):
            b = body or ""
            s = 0
            s += min(len(b) // 200, 4)                      # substance
            s += 2 * b.count("```")                          # code blocks
            s += 2 if any(m in b.lower() for m in
                          ("acceptance", "- [ ]", "expected behavior")) else 0
            s += 2 if re.search(r"[\w/]+\.(py|rs|go|ts|js|md|yaml|toml):?\d*", b) else 0
            return s
        for i in unassigned:
            i["score"] = spec_score(i.get("body"))
        unassigned.sort(key=lambda i: -i["score"])
        claim_bot = any(m in (i.get("body") or "").lower()
                        for i in unassigned[:5]
                        for m in ("/take", "claim this issue", "assign yourself",
                                  "comment to be assigned"))
        best = unassigned[0]["score"] if unassigned else 0
        if best < 4:
            print(f"  skip {nwo}: best GFI specificity score {best} < 4 "
                  f"(thin issue bodies)", file=sys.stderr)
            continue
        if claim_bot:
            print(f"  skip {nwo}: claim-ceremony markers in issues", file=sys.stderr)
            continue

        kept.append({
            "repo": nwo, "stars": r["stargazersCount"],
            "lang": r.get("language") or "?",
            "pushed": r["updatedAt"][:10],
            "open_prs": len(prs), "stale_ext_prs": ext_stale,
            "gfi_unassigned": len(unassigned),
            "sample": [f"#{i['number']} (spec={i['score']}) {i['title'][:64]}" for i in unassigned[:3]],
            "desc": (r.get("description") or "")[:80],
        })

    kept.sort(key=lambda k: (-k["gfi_unassigned"], k["open_prs"]))
    lines = []
    for k in kept:
        lines.append(f"\n{k['repo']}  [{k['lang']}] ⭐{k['stars']}  pushed {k['pushed']}  "
                     f"openPRs={k['open_prs']} (staleExt={k['stale_ext_prs']})  "
                     f"unassigned-GFI={k['gfi_unassigned']}\n  {k['desc']}")
        for s in k["sample"]:
            lines.append(f"    {s}")
    lines.append(f"\n{len(kept)} candidates (from {len(repos)} search hits)")
    report = "\n".join(lines)
    print(report)
    # stdout can be truncated downstream (a `| tail` cost 6/12 candidates once);
    # the full report always survives here.
    (pathlib.Path(__file__).resolve().parent / "last-scout.txt").write_text(report + "\n")


if __name__ == "__main__":
    main()
