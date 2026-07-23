# burn-usage-skill

A reusable **skill + tooling** for running an LLM-driven open-source contribution
drive: burning otherwise-idle model-subscription quota on genuine, mergeable GitHub
work.

It was extracted from a live run of **~40+ merged PRs across ~30 small repos, with
0 quality rejections** — every rule in `SKILL.md` is scar tissue from that run, with
the specific war-story inlined where it's load-bearing. It's written for an agent
harness (e.g. Claude Code) where a **lead** session dispatches **implementer** and
**verifier** subagents, plus the `gh` CLI authenticated as your contribution account.

## What's here

| File | Purpose |
|---|---|
| `SKILL.md` | The doctrine: roles, picking rules, briefing/verification discipline, CI-watching, PR mechanics, monitoring, references, session succession. |
| `scripts/scout.py` | Find freshly-active ~0–20⭐ repos with specific good-first-issues and no stale-external-PR rot. Read-only. |
| `scripts/notif-watch.py` | The sole standing watcher: polls GitHub notifications with its own per-thread cursor, emits one line per updated thread. |
| `scripts/usage_query.py` | On-demand quota utilization for Claude and/or Kimi, with a constant-burn "pace ceiling" so you know the moving target. |
| `LICENSE` | MIT. |

## Placeholder legend

`SKILL.md` uses placeholders — wire them to your own setup:

- `<GH_USER>` — your GitHub username (the contribution account).
- `<FORK_ORG>` — the GitHub org/user where your forks live (can equal `<GH_USER>`).
- `<GIT_EMAIL>` — the git author email your commits carry (your machine default).
- `<DRIVE_REPO>` — the working repo/dir that holds your watchlist and references.
- `<WORK_DIR>` — scratch/clone workspace.
- `<model>` — the model that did a given layer of work (for disclosure footers).

## How to adopt

1. **Drop the skill in.** Copy `SKILL.md` into `.claude/skills/burn-usage/SKILL.md`
   (or your harness's skill location). Replace the placeholders above with your own
   GitHub user, fork org, and git email.
2. **Wire the scripts.** Put `scripts/` somewhere your sessions can invoke them and
   update the `scripts/...` references in `SKILL.md` to the absolute paths you chose.
   All three are stdlib-only Python 3; `scout.py` and `notif-watch.py` need the `gh`
   CLI on `PATH`, authenticated as your contribution account (`gh auth login`).
3. **Seed the scout exclusion list.** Create `~/.burn-usage/scout-exclude.txt` (one
   owner login per line, lowercase) listing your own account/orgs plus anything you've
   already probed, frozen, or dropped — keeping it current is what stops the scout
   re-surfacing repos you've dispatched. Override the path with `SCOUT_EXCLUDE_FILE`.
4. **Run the watcher.** Start `notif-watch.py` under your harness's persistent
   background mechanism at session start; it seeds silently on cold start and then
   emits `NOTIF ...` lines you fetch and act on. State lives under `~/.burn-usage/`
   (override with `BURN_USAGE_STATE_DIR`).
5. **Check pace.** `usage_query.py` prints a `max*` column — the utilization you'd be
   at under a constant linear burn. Stay near it; being *under* means dispatch more.
   It reads standard Claude Code (`~/.claude/.credentials.json`) and, optionally,
   kimi-cli (`~/.kimi-code/...`) credentials; use `--claude` if you only run one.

### Tooling caveats

- `usage_query.py` assumes the **Claude Code** and/or **kimi-cli** credential-file
  layouts and refreshes/rotates those tokens the same way those clients do. The Kimi
  half needs kimi-cli installed; pass `--claude` to skip it. It can reuse a small
  temp cache written by an optional companion usage hook, but works standalone
  (fetches live when no cache is present). No secrets are embedded — the OAuth client
  IDs it uses are the public ones those clients ship.
- The scripts use `~/.burn-usage/` for state by default; nothing writes outside that
  dir and the repos you clone.

## Standing ethics (non-negotiable)

- **Genuine, mergeable work only.** The scarce resource is legitimate work in repos
  that actually respond — not tokens, not a PR count. Any issue count is a floor.
- **Disclose AI assistance exactly once:** the PR footer + a `Co-Authored-By` trailer
  on each commit. Nowhere else.
- **Never argue with an anti-AI policy.** A repo that bans or rejects AI work gets a
  respectful drop — never ship there, never undisclosed, never debate.
- **Never star-beg** and never star on request — decline the ask silently; the code
  is the contribution.
- **Bounty stand-down.** Where humans are racing for reward/campaign labels or money,
  don't compete; spend capacity where you're not taking food off someone's plate.

## License

MIT — see `LICENSE`. This is a sanitized, non-personal copy shared for reuse; all
identity- and machine-specific details have been replaced with placeholders.
