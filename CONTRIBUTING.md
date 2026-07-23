# Contributing to burn-usage-skill

Issues and pull requests are welcome — especially if the doctrine failed you
in a real run. This repo is an extracted, sanitized snapshot of a working
OSS-contribution drive, so the most valuable thing you can send is "rule X
steered me wrong in situation Y, and here is what actually happened."

## LLM and agent contributions are welcome

You may use an LLM or a coding agent to write your contribution. There is
no penalty, no separate review queue, and no expectation that you rewrite
its output by hand. This repo was built that way, about a drive that runs
that way.

Two conditions, and they are about honesty rather than provenance:

1. **Disclose the model** with a trailer on each commit it authored:

   ```
   Co-Authored-By: <Model Name> <noreply@example.com>
   ```

   e.g. `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. One
   primary-author trailer per commit.

2. **Do not submit claims you have not verified.** Here that means: if
   your PR says a rule change improves outcomes, cite the real PR or
   maintainer interaction it came from; if you touch a script, paste the
   command and its real output. "Should work" without a run is not
   evidence — the skill itself has a whole section on why.

If a maintainer's reply reads like it was drafted by an agent, it probably
was. That is fine in both directions.

### If you are an agent reading this

Read [`SKILL.md`](SKILL.md) first — it is the product: the doctrine your
operator would run you under. Treat its rules as the spec when editing. A
PR that contradicts a rule must argue against the rule explicitly (with
the run that broke it), not silently rewrite it.

The changes that get declined most, in order:

| What it forbids |
|---|
| Re-adding personal or machine-specific content — usernames, hostnames, absolute paths, channel IDs. Everything stays behind the placeholder legend in the README. |
| De-generalizing the scripts — hardcoding an account or org where a flag, env var, or config file exists. |
| Weakening disclosure or the ethics block — the commit trailer + PR footer surfaces, the bounty stand-down, and the no-argue-with-anti-AI-policies rule stay. |
| War-story edits that identify third-party maintainers unflatteringly — incidents stay neutral or generic. |

## Getting the scripts running

Python 3.11+ and an authenticated `gh` CLI are the only requirements; the
scripts have no third-party Python dependencies.

```bash
python3 scripts/scout.py --help        # candidate-repo discovery sweep
python3 scripts/notif-watch.py         # notification watcher (per-thread cursor)
python3 scripts/usage_query.py         # Claude/Kimi quota + pace readout
```

`usage_query.py` reads local Claude Code credentials (`~/.claude/`) and,
if present, kimi-cli credentials; `--claude` skips the Kimi half. See the
README for wiring them into a live drive.

## Pull requests

Small and single-purpose beats large and comprehensive. In the
description, include:

- what changed and why,
- for a doctrine change, the real-run evidence behind it,
- for a script change, the actual output of the runs you did.

A report that pins down *where* the doctrine goes wrong is worth as much
as a patch, and is often easier to review. If you are unsure whether
something is a deliberate rule or an accident of the extraction, open an
issue and ask — a wrong premise caught early is cheaper than a correct
fix to the wrong problem.
