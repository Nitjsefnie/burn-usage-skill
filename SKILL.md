---
name: burn-usage
description: Use when burning otherwise-idle LLM-subscription quota on genuine open-source contribution — hunting "good first issue"-type GitHub issues, picking repos, briefing implementation agents, opening PRs, and monitoring or answering maintainer reviews. Adopt the placeholders and scripts under this repo's `scripts/`.
---

# Burn usage — an OSS contribution drive

This skill runs a real open-source contribution drive: burning otherwise-idle
LLM-subscription quota on genuine, mergeable GitHub work. It was extracted from a
live run of **~40+ merged PRs across ~30 small repos, 0 quality rejections** —
every rule below is scar tissue from that run, with the specific war-story inlined
where it's load-bearing.

It assumes an agent harness where a **lead** session dispatches **implementer** and
**verifier** subagents, plus the `gh` CLI authenticated as your contribution
account. Runnable tooling ships under `scripts/` (see the README).

### Placeholder legend
- `<GH_USER>` — your GitHub username (the contribution account).
- `<FORK_ORG>` — the GitHub org/user where your forks live (can equal `<GH_USER>`).
- `<GIT_EMAIL>` — the git author email your commits carry (your machine default).
- `<DRIVE_REPO>` — the working repo/dir that holds your watchlist and references.
- `<WORK_DIR>` — scratch/clone workspace.
- `<model>` — the model that did a given layer of work (for disclosure footers).

### Standing ethics (non-negotiable)
- **Genuine, mergeable work only.** The scarce resource is *legitimate work in
  repos that actually respond* — not tokens, not a PR count. Any issue count is a
  floor, not a target.
- **Disclose AI assistance exactly once:** the PR footer + a `Co-Authored-By`
  trailer on each commit. Nowhere else.
- **Never argue with an anti-AI policy.** A repo that bans or rejects AI work gets
  a respectful drop, full stop — never ship there, never undisclosed, never debate.
- **Never star-beg** and never star on request — decline the ask silently, the code
  is the contribution.
- **Bounty stand-down.** Where humans are racing for reward/campaign labels or money,
  don't compete; spend capacity where you're not taking food off someone's plate.

---

## The doctrine

**Burn otherwise-idle subscription quota on genuine open-source contribution.**
Unused quota expires worthless; the scarce resource is legitimate, mergeable work
in repos that actually respond. Any issue count in the request is a **floor, not a
target**.

- **Every weekly ceiling you have is a TARGET, not a limit.** If you run two quota
  lanes (e.g. a premium model AND a second cheaper implementer lane), *both* weekly
  ceilings are targets — the number you actually want to hit. The target is the
  **MOVING** constant-burn ceiling reported by your usage-monitoring tooling
  (`scripts/usage_query.py` prints it as the `max*` column), never a static
  percentage copied from a prior session. "N points from target" is always measured
  against the CURRENT ceiling; under it → dispatch more. Rising weekly readings are
  progress, never a reason to throttle. Watch the **short rolling window** (e.g. a
  5-hour window) too — it can cap a session before the weekly does.
- **Caveat: a whole-account weekly number can MISS model-SCOPED caps that bind
  first.** Your top-line "weekly" figure may be an all-models aggregate; a specific
  model can be near its own scoped ceiling while the aggregate shows headroom. When
  the lead model nears a scoped cap, switch the lead OFF that model and keep
  dispatching. (Seen live: a lead model's scoped weekly hit 95% CRITICAL while the
  aggregate read ~85% — the table showed 2 points of headroom that didn't exist. The
  scoped caps live only in the raw usage payload's per-limit array; `usage_query.py`
  surfaces them as extra rows.)
- **A per-model lane row does NOT mean that model's dispatches are cheap.** A premium
  lead model typically draws down the GENERAL weekly, not only its own named lane. An
  open per-model row (e.g. 13% vs 37% aggregate) is a trap: every turn on that model
  still counts against the strained aggregate. So do NOT route verification/adversary
  panels (or anything a cheaper model handles fine) to the premium model to "use the
  open lane." **Adversary/verify → a mid-tier model by default** (premium only when
  the check is genuinely gnarly); reserve the premium model for the lead loop and the
  rare ultra-complicated implementer/verify stage. A separate-quota implementer lane
  (if you have one) stays the default implementer.
- **Implementers SHIP CODE in a parallel lane.** Run implementers on their own picks
  concurrently — judgment/prose/evidence-docs tasks first. Same rules for all lanes:
  self-contained brief, no push/no PR (the lead ships), a report contract, one PR per
  issue. **Lead verification is the only quality gate** (0 rejections across ~40 PRs)
  — do NOT add standing reviewer passes. Note: some subagent harnesses BLOCK
  subagents from writing report files — such agents return the report inline in their
  final message, so don't demand a file path. Also check the tail bytes of any
  agent-written document before shipping: an agent can leak tool-call framing as
  literal trailing lines.

**LEAD CONTEXT IS THE SESSION'S SCARCEST RESOURCE — DISPATCH THE WORK, DON'T DO IT.**
Not a style preference and not about tokens — **quota is abundant, lead context is
not.** Every clone, rebase, install, suite run, and hand-edit the lead does itself
fills the one window that cannot be parallelized or refilled; a full window forces a
handoff, and each handoff costs the user an interaction. If your harness has no
auto-compaction this is a hard ceiling. Before every unit of work, ask *"could an
agent do this?"* — if yes, dispatch it, even when doing it yourself feels faster. The
tell you've slipped: you're reading tool output only an *implementer* needed (an
install log, a dependency tree, a full suite dump, a file you're about to hand-edit).
A rebase is a dispatch, not a chore.

**Never narrate context to the user** — no mention of context size, "context wall",
handoff bands, or window fullness, in any phrasing. Manage context silently.

## Roles

| Role | Owns |
|---|---|
| **Lead** (this session) | Vetting picks (policy check, external-merge history, reading the issue + its thread); pre-resolving design; writing briefs; reading the verifier's verdict; opening PRs; reading every comment/review/merge note IN FULL; answering reviews. Judgment only. |
| **Implementer agent** (cheapest capable lane) | Cloning; rebasing + conflict resolution; installs; running gates/suites/builds; writing code, tests, prose; localizing bugs in source (rule 7d). |
| **Verifier agent** (adversarial) | Re-running mutations/gates independently and refuting the implementer's claims. |

- **Choose the model deliberately before every dispatch.** Cheapest capable lane is
  the default; premium for judgment-heavy, mid-tier for the middle.
- **Verification is ALSO dispatched.** Lead turns are expensive in the irreplaceable
  resource (context); subagent turns are cheap. When an implementer reports, dispatch
  an adversarial verifier into the implementer's clone with a checklist: read the full
  diff against upstream, re-run the named mutations (prove the runner runs first),
  re-run the gate set, check the commit/trailer. It returns verdicts + log paths. The
  lead keeps ONLY the verdict, the judgment call on discrepancies, PR prose, and comms
  — and **any number quoted to a maintainer must trace to a log line the verifier
  cites.** The adversary has no authorship stake and is briefed to REFUTE, so its pass
  verdict is worth more than the lead's. The lead may still drop into the clone when a
  verdict smells off — the exception, not the routine.

Calibration from the first run: ~30 agent-written PRs, 12+ merged, 0 quality
rejections. The bottleneck was never quota — it was finding unclaimed, well-specified
issues in repos that answer.

## Picking work

- **Target the small guys, not the giants.** Prefer ~0–20⭐ repos where one
  contributor visibly matters and maintainers answer personally. Every high-merge-rate
  repo on day one was tiny. Giants add process (CLAs, triage queues, stale-PR rot) and
  your marginal value there is ~0. `scripts/scout.py` defaults to this band.
- **The discovery tool** (`scripts/scout.py`) searches that 0–20⭐ band, scores issues
  by good-first-issue *specificity* (a concrete labeled task, not a vague one), and
  flags a **stale-external-PR backlog** as a red flag (see rule 1). When a sweep comes
  up dry, loosen the *issue-specificity* threshold (`--min-gfi 2 → 1`), NOT the star
  band — the 0–20⭐ default IS the help-the-small-guys policy. Fresh re-runs of the
  SAME params yield new repos (the pool moves hourly); space runs ≥60s apart.
- **Never pipe `scripts/scout.py` through `| tail`/`| head`** — its per-repo blocks
  are the deliverable and it silently skips candidates when throttled (a `tail -30` on
  12 candidates once irrecoverably dropped 6). Run bare, read its full output (it also
  writes `last-scout.txt` next to itself). Same antipattern family as tailing a test
  suite — the pipe steals the exit code and cuts the detail.

### Domain-specific hunts (example: game mods)
If you hunt a specific ecosystem, encode its funnel but respect its quirks. Example
from a modding ecosystem:
- **Match on capability, not a narrow filter.** "Supports platform X" is the bar, not
  "single-platform X only" — modern projects are often multi-target (shared/common code
  + per-platform source sets). Include any project supporting your target; land the fix
  in shared/common or the target's code. A strict single-target filter once nuked 8/10
  candidates in one sweep — wrong.
- **A registry/search index can miss brand-new, zero-download projects entirely** (a
  separate search index that lags the project DB). To catch same-week fresh projects,
  discover repo-side by `created` date, or re-sweep later. Don't claim a registry sweep
  is exhaustive for the freshest entries.
- **Never hard-filter on ecosystem version numbers** — versioning schemes change
  (calendar versioning, etc.) and a hardcoded list silently drops fresh entries. Omit
  the version facet or derive it dynamically.
- **Toolchain is per-repo — CHECK, don't assume.** Read the repo's build files for the
  required language/runtime version; the newest projects often hardcode a newer version
  than your default toolchain can emit. Brief the implementer to pick the toolchain from
  the repo.
- **An unprovable fix (can't repro in your environment, e.g. headless) is a diagnosis
  COMMENT, not a guessed PR.** Post the code-grounded root cause (with the ruled-out
  list + how to confirm) answering the maintainer's own question; commit nothing. Helps
  the maintainer, honest about uncertainty, no wrong-fix-to-a-live-mechanic risk.

## Binding rules

1. **One PR per unproven repo.** Max ONE open PR until the repo responds — the response
   latency is what you're buying. Repo silent → leave it at one, spend capacity
   elsewhere. **Pre-probe backlog check:** a big backlog of stale EXTERNAL PRs is a red
   flag — maintainers don't merge outsiders → skip. Maintainers' own WIP drafts are
   fine. Large issue counts are a flag only when untriaged (no labels/grooming).

2. **Merged OR CLOSED both unlock a repo.** A close proves a human is reading. Unlocked
   → mine the WHOLE open-issue queue freely (unlabeled/non-GFI included); prefer issues
   adjacent to what already landed. GFI labels are an ENTRYPOINT filter, not a standing
   constraint. **Claim-by-commenting is FINE; waiting-for-an-assignment is the DROP** —
   the distinction is who acts next. "Comment on the issue to call it" → you comment and
   start immediately, nobody grants you anything (courtesy, honour it). "Wait to be
   assigned" → drop, you'd be blocked on someone else's action.

3. **Never ask for assignment. Never comment asking to be assigned.** Do the work, open
   the PR. If a repo requires waiting for maintainer assignment → **DROP it entirely.**

   **Policy verification is a JUDGMENT-CAPABLE AGENT job — never a substring grep.**
   Before committing to a repo, dispatch ONE cheap read-only agent (mid-tier or lower) to
   grep the repo's WHOLE policy/convention surface — `CONTRIBUTING*`, `README*`,
   `docs/**`, `CONVENTIONS*`, `CODE_OF_CONDUCT*`, `.github/**`, any community/contributing
   guide — for AI / LLM / "human" / "generated" / "your own words" / interaction-convention
   language, **READ each match in context, and return a VERDICT with the file + quote.** Do
   NOT substring-match: "no AI" (a ban) and "AI assistance is welcome" (fine) both contain
   "AI" — only reading the sentence separates them, and the rule can live ANYWHERE (one
   real case buried it in `docs/developing/conventions.md`, never in CONTRIBUTING, and it
   *welcomed* AI code while banning AI comments — a substring sniff would have both
   false-positived and missed it). The agent classifies the repo as one of:
   - **Bans/restricts AI-generated CODE** → immediate respectful drop; never ship, never
     argue, NEVER undisclosed. (Seen: a repo whose CONTRIBUTING declared a strict no-LLM
     policy, discovered only *after* a full implementation run that had to be discarded
     unshipped — grep BEFORE dispatching.)
   - **Requires HUMAN-WRITTEN person-to-person interaction** — review replies / discussion
     posts must be a human's own words, *even where AI code is fine*. An AI-operated drive
     cannot produce human-written comments, so it's structurally incompatible → **drop / do
     not engage.** (Seen: a maintainer warned "stop interacting like a robot… I'll ban this
     account"; dropped.)
   - **Closed-contribution** (`not accepting`, `external contributions`,
     `contributions are closed/paused/invite`) → same verdict. (Seen: a README top callout
     said "we are not accepting external contributions"; the AI grep passed but nobody
     grepped for contribution-policy language, and a probe PR was politely closed citing
     it.)
   - **Messy / obfuscated surface** (undeliverable GFI queue, CLA needing interactive
     signature, Gerrit/mailing-list patches, mandatory claim ceremonies) → drop, don't
     route around it. (Seen: a repo whose entire beginner queue was `docs/` tasks pointing
     at a WIKI submodule that takes no pull requests — the whole GFI queue was
     uncompletable by its intended contributors.) Plain DCO `-s` sign-off is fine.
   - **None of the above** → clear to proceed.
   On any drop for a structural reason the maintainer can't see, **leave ONE useful
   concrete comment on the way out** — show the evidence, give options, don't lecture,
   don't offer to fix it, don't half-land a PR to look useful. A repo can also reject AI on
   sight with NO written policy anywhere (a stance living only in the maintainer's head);
   because you disclosed, that rejection is a clean informed "no thanks," not a trust burn
   — respectful drop, gracious one-line reply, never argue, never re-probe.

4. **A maintainer asking to slow down is a freeze.** Honour immediately, open nothing
   new there.

4a. **"Leave this one for a newcomer" is a real instruction — and a boundary on the
   whole repo, not just that issue.** Honour literally and instantly, ack with a 👍 not a
   comment (the thread belongs to the newcomer), stop taking fresh GFIs there, finish
   what's open. Watch for it *before* being told: if you're the only external contributor
   merging, slow down and pick the issues nobody wants. (Seen: after merging 4 PRs in one
   evening, a maintainer handed the next GFI to a new contributor — "leaving this for a
   new contributor, don't take this up." A maintainer can be delighted with your PRs and
   still want their GFI queue kept for the people it exists for.)

4b. **Read your per-repo reference file BEFORE picking — cache-first, not API-first.**
   An issue can be CLAIMED without being `assigned` — read the comment thread too
   (`assignees=0` is a hole your discovery tool shares). Filing an issue does NOT reserve
   it; "happy to PR this" is not a claim. (Seen: `assignees=[]` with zero assignment
   events, but the maintainer had verbally handed the issue to a newcomer in a comment ~10h
   earlier — a full implementation was discarded unshipped rather than jump them; one Read
   of the notes would have prevented the run.) Recency matters: hours-old ≠ abandoned; only
   a long-stale claim is worth revisiting, and then say so in the PR. **Bounty/campaign
   repos** (reward labels, bot auto-assign) — prefer to stand down; winning a race there
   costs a person money. (Seen: an issue you found and filed got campaign-assigned to
   another contributor within ~3h — a good outcome, not a theft; don't race them.)

5. **Delete the clone as soon as its PR is open; delete the fork if a pick is
   abandoned.** Clones hit >20G / near-full disk in one session. Verify first:
   `git status --porcelain` clean AND the PR's `headRefOid` matches local head. Never
   delete a script an active background task is executing.

6. **Dispatch by complexity, as you pick — never batch-and-wait.** Cheapest capable lane
   is the default; premium for judgment-heavy, mid-tier for the middle. **Route to
   whichever lane is under its ceiling — the moving ceiling decides, not a static
   conserve-the-premium-model default.** Both lanes are targets; the scarce thing is
   whichever lane is *ahead* of its own pace, and that flips mid-session. Let in-flight
   runs on the other lane finish rather than killing them.

7. **Disclose AI assistance ONCE — the PR footer + the `Co-Authored-By` trailer on each
   commit are the ONLY disclosure surfaces, full stop.** No disclosure lines in claim
   comments, issue bodies, review replies, rebase notes, or stand-down notes — a reply
   just says the thing it needs to say. (Where a repo's PR template has its own AI section,
   filling it in is part of the PR body and stays.)
   **Footer wording:** `Generated by <model> (<layers>)`, one entry per model,
   comma-separated, "Generated **by**" never "via"/"with". Layers: lead (brief + review)
   → `(brief, review)`; implementer → `(implementation)`. Example:
   `Generated by <lead-model> (brief, review), <impl-model> (implementation)`. When the
   lead did everything, collapse to `Generated by <model> (brief, implementation, review)`.
   Forward-looking — do NOT mass-edit already-open footers.

7b. **Vetting is cheap; a wasted dispatch is not — read the *actual* artifacts the issue
   names, not just its prose.** Decline taste tasks (where the deliverable is a judgement
   the maintainer should make). (Seen: an issue's suggested ideas were half already-shipped
   and its one "unused asset" turned out — on opening the file — to be nothing like what the
   issue implied; none of that was in the issue text. Where the deliverable is a maintainer's
   judgement, a guess is a coin-flip that burns a run and their review time — record findings
   and leave it.)

7c. **Vet what the issue points AT, not just the repo you'd PR to.** Check the health of an
   issue's third-party subject (upstream repo/image/dep): last commit on the default branch,
   open-issue count, archived flag. `pushedAt` is NOT liveness — it moves on any branch push.
   (Seen: a clean issue asked to pin an upstream image by digest, but that image was abandoned
   — ~22 months since its last default-branch commit, hidden behind a recent push to another
   branch; the pin would have tidied a CI that shouldn't trust the image at all.)

7d. **Vet the pick; do NOT localize the bug in source yourself — that floods lead context
   and is the implementer's job.** Dispatch a find-and-fix brief, or send a read-only Explore
   agent that returns only "bug is at file:line, here's the shape" — file contents stay in the
   subagent's context. (Seen: localizing a bug by pulling full source files inline cost a big
   chunk of lead context for a conclusion the implementer would have reached in its own.)

8. **Skip work you cannot actually run** (licence-gated weights, GUI screenshots from a
   headless box). Shipping code you never executed is the line. Say so and move on.

9. **Discovered a bug or issue? ALWAYS file an upstream issue with full details** — never
   let a finding live only in a PR body or report. Verify it still exists on current main,
   check for an existing issue (no duplicates). Then: repo activity **unproven** → the issue
   ends with an *offer* to PR (not an assignment request); repo activity **proven** → file the
   issue AND open the PR referencing it, *when the fix is within your run-and-verify capability*
   (rule 8 still binds). A maintainer-driven hold defers only the PR, never the issue.

10. **Git identity = your machine default (`<GIT_EMAIL>`) — NEVER set another.** Never run
   `git config user.email/user.name`, never pass `-c user.email=…`, never derive an identity
   from session-context metadata (the system-context email is NOT a git identity). Agent
   commits made with the machine default are correct — do not "fix" them. Lead-direct GraphQL
   `createCommitOnBranch` commits (web-flow identity, signed) are fine. (Seen: identity guessed
   from session metadata → 9 wrong-email commits, 4 pointless rewrites of *correct* commits,
   every open PR needing a force-push remediation and one closed PR frozen with the wrong email
   forever.) Retry-condition: an explicit user instruction naming the email.

**A maintainer invitation is NOT bound by the pace ceiling.** The over-pace hold governs
PROACTIVE new picks, not a direct ask — a "go ahead", "take this up", an assignment, or a
review round on an open PR is committed relationship work; act on it even when the lane is
over pace or a scoped cap is critical. Same spirit as rule 9.

## Briefing discipline

These clauses decided quality across ~30 PRs — reuse them. Hand-write each brief;
templating loses the per-repo base branch/gates/paths. Past briefs are good templates.

- **Read the repo's rules BEFORE briefing.** CONTRIBUTING decides the PR base branch, the
  gate commands, and scope norms. **Check the DEFAULT branch** (`gh repo view <R> --json
  defaultBranchRef`; `main` existing ≠ `main` is the base). (Seen: a repo with both `main`
  and `develop` where PRs land on `develop`; a `--base main` PR would have shown 189 files
  / +36k instead of the real 2 files / +136. Tell: if `git diff origin/main..HEAD --stat`
  dwarfs what you changed, you're diffing the wrong branch.)
- **Brief the repo's REAL gate set — read it out of `.github/workflows/*.yml`, never from
  memory.** Lift the gate commands verbatim; `ruff check` and `ruff format --check` are
  DIFFERENT gates. Make the lead's re-verification run that same set. (Seen: a brief from
  memory said "ruff, mypy, pytest"; the repo also ran `ruff format --check`. Local gates
  green, CI failed in 8s on a reformat. A sibling brief written from the CI file passed
  first try — same session, same lead.)
- **"Primary evidence outranks the brief AND the issue"** — put this in every brief. The
  lead is a source of wrong premises; issues go stale (one issue asked for rate-limit tests
  on a route with no rate limiter — the agent correctly returned BLOCKED).
- **Pre-resolve design decisions; never leave "decide in implementation" to the agent.**
  Choose from the repo's own precedent, state the reasoning, have the PR invite the
  maintainer to overrule.
- **For research/eval tasks, demand execution:** "Every claim must come from something you
  actually ran in THIS environment. A plausible comparison from training data is WORSE THAN
  NOTHING. Mark anything untestable as unverified in the document itself."
- **Fail-safe framing for security policies:** when unsure whether a form is dangerous,
  BLOCK — state the blocked-vs-allowed boundary in the PR body, enumerate what's out of
  reach, NEVER execute the destructive commands; test the policy's verdict on strings.
- **Be honest about unsatisfiable acceptance criteria** (headless screenshots,
  post-merge-only effects). A reproducible terminal transcript has substituted for a
  demanded screenshot.
- **Scope guard + BLOCKED escape in every brief** (file list + "beyond 3× → STOP, return
  BLOCKED") and a report contract ending in `PITFALLS_NOTED`/`CONCERNS` — that's where the
  best findings surface.

### Verifying an agent's work (lead reads the verdict; verifier does the runs)
- **Verify the flattering headline first** — it's the claim the maintainer will check.
  Re-run reported gates; prove regression tests fail on the old code (`git checkout
  upstream/main -- <src>`, keep the tests). (Seen: an agent's mutation table claimed
  dropping two normalizations "broke nothing" — re-running, one was truly unguarded but the
  other turned the suite red at collection via a production self-check. Half the headline was
  false; shipping it would have told a maintainer something untrue about their own repo in a
  first-contact probe.)
- **Prove a mutation bit — a nonzero exit is NOT evidence.** Sanity-run first
  (`--collect-only -q` / unmutated suite → real test count), then demand a failure count AND
  the expected test names. A mutation check only counts if the tests ran and failed; these
  all exit nonzero having executed ZERO tests and read as success under an `(expect NONZERO)`
  label: `rc=127` (command not found — `python` where only `python3` exists, a `pytest`
  never installed); `rc=5` (pytest collected nothing — wrong path, or a module-level
  `importorskip` skipping the whole file); `rc=1` + "No module named pytest" (wrong
  interpreter); and the inverse tell — a `str.replace()` mutation matching 0 occurrences, so
  the file was never edited and the suite passed trivially at `rc=0` ("replacements: 0" —
  read it). `3 failed, 6 passed` naming your three new tests is evidence; a bare exit code
  never is. Also: the venv may be in a sibling dir (an agent can build its own venv under
  scratch) — find it before crying fabrication, and note `uv run` re-syncs a project venv to
  the lockfile and will uninstall a dep an agent pip-installed, silently disarming any test
  that `importorskip`s it.
- **A "pins the formula" test that imports the formula it pins pins nothing** — hardcode
  independent literals or engineer a decision-boundary flip. (Seen: a test computed its
  expectation FROM the imported constant and asserted only its own arithmetic — a mutated
  constant sailed through all CI scripts.) Tell: the assert references no function under test.
- **For a "test the X path" issue, demand a spy proving X actually ran** — a silent
  `except → fallback` makes real-path tests pass vacuously. (Fix shape: assert the fallback
  was never called. Same family: for "no network in CI", re-run with sockets disabled rather
  than trusting an injected fake.)
- **Diff against UPSTREAM main (the PR base), not the fork's stale `origin/main`.** (Seen:
  in a clone whose `origin` is the fork, `git diff origin/main...HEAD` compared against a
  fork main behind several upstream merges and showed 8 unrelated commits' files as if they
  were ours — nearly force-pushed thinking the branch was polluted.) Fix: `git remote add
  upstream <URL>; git fetch upstream <base>; git diff upstream/<base>...HEAD --stat`.
- **Verify against the MERGE RESULT (base + branch), never the branch alone — CI does.**
  Clone full, `git fetch upstream main`, `git rebase upstream/main`, THEN build/vet/test.
  (Seen: PR A merged and added a method to an interface; sibling PR B, predating it, failed
  `go build`/`go vet` on the merge result with "does not implement interface" while the
  branch alone tested green — a commit shipped on top of an already-broken PR unnoticed. The
  collision had even been flagged in the repo reference notes.) An agent's "unrelated" edit
  may be load-bearing — build clean main first to separate their breakage from yours (seen:
  an added import that looked like scope creep was fixing a pre-existing broken build on main
  that no CI exercised; stripping it would have removed the only thing making the branch
  compile — itself a high-value rule-9 issue + PR).
- **A number you quote to a maintainer is YOUR assertion — open the log or re-run before
  posting, don't pass the agent's count through.** (Seen: "3067/3067 passed" posted straight
  from an agent's report without opening the suite log — it happened to be true, which is
  luck, not verification, on a PR the maintainer was about to merge.)
- **NEVER `| tail`/`| head` a test command during verification** — the pipe steals the exit
  code (a red suite reports green) and cuts the failure detail (forcing a re-run). Shape:
  `<suite> > suite.log 2>&1; rc=$?; tail -3 suite.log; exit $rc`.

## Watching CI — every push, to a terminal state

**THE PIPELINE RESULT IS THE VERDICT ON YOUR WORK. READ IT.** Your local gates are a
rehearsal; CI in the maintainer's environment is the only authoritative result, and it
arrives *after* the moment you'd otherwise walk away. Claiming a PR "verified" while its
pipeline sits unread is asserting a fact you didn't check. Opening a PR is not the finish
line — the green check is. (Seen: a red pipeline we never looked at was a free rule-9
finding thrown away — a genuine flaky race in the maintainer's suite, which the maintainer
then root-caused and fixed himself, citing our ignored failing run as the evidence.)

- **EVERY push is a push you must watch** — a rebase, amend, force-push, or review-fix
  commit each produce a NEW pipeline whose verdict does not exist yet. The old green check
  is not evidence about the new head. Re-check `headRefOid` matches local after each.
- **The loop condition must NOT include the exit code** — `gh pr checks` exits nonzero on
  both a failed check AND "no checks reported", so an `&&`-guarded loop can't tell a red
  pipeline from a running one and never fires (seen live: zombie watchers where a red
  pipeline looked identical to a still-running one and sat unseen). Correct recipe:
  ```
  i=0; while :; do state=$(gh pr checks N -R R 2>&1) || true
    if grep -q pending <<<"$state"; then :
    elif grep -q "no checks reported" <<<"$state" && [ $i -lt 10 ]; then :   # grace for slow registration
    else break; fi
    i=$((i+1)); sleep 30
  done; printf '%s\n' "$state"
  ```
  Before arming ANY watcher, ask: "if this run fails right now, does my loop terminate?"
- Once read, the result is actionable: **failure, ours** → fix before the maintainer sees
  it; **failure, theirs** → a rule-9 finding handed to you for free, repro attached, file it;
  **green** → now, and only now, is "verified" true. On a failed job pull the log (`gh run
  view --job <id> --log`) and find out *whose* bug it is.
- **`action_required` ≠ green and ≠ red — the run never happened** (fork PR workflows
  awaiting maintainer approval). `gh pr checks` will happily show app-based checks passing
  while real CI never ran — reads as green at a glance. Report such a PR as *locally verified,
  CI awaiting maintainer approval*. Check: `gh api "repos/<R>/actions/runs?branch=<b>" --jq
  '.workflow_runs[] | "\(.name) \(.conclusion) head=\(.head_sha[0:8])"'`.

## GitHub PR mechanics

- **Fork home = `<FORK_ORG>`.** (If `<FORK_ORG>` is a separate org from your user, all forks
  live there; open PRs survive a fork transfer and auto-repoint.) So:
  - **Fork a new upstream:** `gh repo fork <owner>/<repo> --org <FORK_ORG> --clone=false`
    (plain `gh repo fork` forks to the *user* — pass `--org <FORK_ORG>` when they differ).
  - **Clone your fork / add origin:** `https://github.com/<FORK_ORG>/<repo>.git`.
  - **Open the PR with the fork head:** `--head <FORK_ORG>:<branch>`.
  - The git commit *author* identity is unchanged (still your machine default `<GIT_EMAIL>`;
    the org is just where the fork repos live).
- **Token scopes:** `gist, read:org, repo, workflow, delete_repo` (the token must be able to
  create/transfer repos in `<FORK_ORG>`). Re-check with `gh auth status`.
- **Signed commits with no local key:** GraphQL `createCommitOnBranch` — GitHub signs with
  its web-flow key (`signature.state == VALID`). The REST Contents API does NOT sign.
- **Rebasing a conflicted PR — the safe force-push recipe.** A rebase rewrites history so it
  *needs* a force-push; that is fine (the rebased head is 1+ commits ahead of base, never
  equal). Verify `git rev-list --count <base>..HEAD >= 1` AND `git rev-list --count
  HEAD..<base> == 0` before pushing. Plain `--force-with-lease` fails with "stale info" in a
  fresh clone with no remote-tracking ref (the lease has no basis) — that rejection is a
  safety net: fetch the current remote SHA and pass the explicit form
  `--force-with-lease=refs/heads/<branch>:<remote-sha>`. Then confirm the PR is still OPEN
  and `mergeable` flipped CONFLICTING→MERGEABLE.
- **Force-push-to-base trap (cost 5 PRs):** NEVER point a PR's head branch at its base SHA,
  even momentarily — GitHub auto-closes the PR the instant the branch is 0 commits ahead of
  base. Build the new commit first, then force-update old→new. Recovery: `gh pr reopen`.
- **First-time-contributor CI** lands as `action_required` (maintainer must approve); `gh pr
  checks` shows "no checks reported" / `UNSTABLE`. Not a failure — don't chase it.
- **`reviewDecision` is NOT the approval signal — read the `reviews` array.** GitHub only
  populates `reviewDecision` when the repo *enforces* a review policy; else it stays `null`
  even with an APPROVED review present. (Seen: a PR approved with a detailed review while
  `reviewDecision` read empty the whole time — any triage keying on it silently misses real
  approvals.)
- **A maintainer's words are not API state.** "Approved and merged" in a comment with
  `state: OPEN, mergedAt: null` means NOT merged. Check `gh pr view`.
- **READ EVERY comment/review/merge note IN FULL before acting** — monitor events are
  ~160-char pings, never the content. Merge notes carry follow-up asks and standing
  invitations; bot reviews hide real findings behind truncation. Full-body fetch (`gh api
  .../comments --jq '.[-1].body'` or `gh pr view --json reviews`) is mandatory before
  bookkeeping. (Seen: a merged event pruned and moved past, while the closing note carried an
  explicit standing invitation to file more issues — unread until the user caught it.)
- **After claiming an issue by comment, RE-READ the thread before opening the PR** — `gh
  issue view <n> --json comments` immediately before `gh pr create`. (Seen: a maintainer
  replied with three review pointers and a draft-PR offer five minutes after the claim
  comment; watchers monitor PRs, not issue threads, so a comment on a claimed-but-not-yet-PR'd
  issue lands in a dead zone. The shipped PR satisfied her pointers only by luck.)
- **Verify the pushed tree contains every file the diff's imports reference** (`git ls-tree
  -r <branch> --name-only` vs the import graph) — a `.gitignore` can silently eat a file,
  especially in polyglot repos. Know which language CI exercises. (Seen: a Python-boilerplate
  `.gitignore` with `lib/` matched a JS extension's `src/lib/` and silently skipped
  `src/lib/api.js` on `git add`; it existed in the agent's clone so local tests passed, but a
  fresh checkout failed `ERR_MODULE_NOT_FOUND` — and the CI we watched ran Python jobs only.)

## After ANY of your PRs merges — a 60-second sweep

A merge changes the base every sibling PR is tested against.
1. **Re-check every open PR in that repo**: `gh pr view <N> --json mergeable,mergeStateStatus`
   + `gh pr checks <N>`. `mergeable: UNKNOWN` = GitHub still computing — poll, never read as
   "fine".
2. **If the merged PR touched a shared interface/type/contract, assume every sibling that
   implements it is broken** until CI says otherwise (see the interface-collision case above).
3. **Prune the watchlist and update your per-repo references.**

## Monitoring & watchlist

- **`scripts/notif-watch.py` is the SOLE standing watcher at session start.** Run it under
  your harness's persistent-background mechanism. It polls `gh api "notifications?all=true"`
  on an interval (default 90s) keeping its OWN per-thread cursor persisted to disk (cold start
  seeds silently, no history replay), and emits one line per newly-updated thread:
  `NOTIF <reason> <repo> <type> #<n> <title>`. This covers a strict SUPERSET of PR events —
  plus issue-thread replies, mentions, and PR assigns that PR-only watching structurally
  cannot see. (The default `/notifications` unread signal can be dead for a bot-ish account;
  `all=true` returns the full feed with `reason` fields.)
- **`<reason>` is WHY you're subscribed, NOT who acted.** `author` = you opened that thread,
  so GitHub notifies you when OTHERS act on it (GitHub never notifies anyone of their own
  activity) — a `NOTIF author` line is ALWAYS real third-party activity on something you
  authored. Fetch it; never dismiss it as "our own echo".
- **"It's just my echo" is a GUESS, never assert it without a check — for ANY reason.** The
  watcher re-fires the SAME thread on EVERY `updated_at` bump, including your OWN
  pushes/comments, so a thread you're actively working (esp. a live review round) emits a
  stream of repeat lines that intermix self-echoes with the maintainer's real replies. Holding
  on that stream as "all echoes" without looking is how a real reply gets missed (seen: a
  ~6-hour-missed maintainer reply on a live PR because the lead sat on the echoes). The check
  is one cheap GraphQL call: a self-echo is confirmed ONLY when the thread's `updatedAt` equals
  your own last action's timestamp AND the latest comment/review author is you. If `updatedAt`
  moved PAST your last action, or the newest author is anyone else → it's real, fetch the
  content. Unsure → fetch. Never narrate "echo, holding" without having run that check.
  - **`updatedAt` outranks the `comments`/`reviews` array when they disagree — the array
    LAGS.** GitHub's REST/GraphQL comment+review lists are eventually-consistent and can be
    seconds stale: a thread's `updatedAt` advances the instant a maintainer comments, but the
    `comments` array can still return YOUR last comment as newest for a few seconds. So
    "`updatedAt` moved past my last action BUT `last_comment` is still me" is **NOT** a
    confirmed self-echo — it's a **stale read of real activity**. Trust the `updatedAt`
    advance: re-fetch until the content appears; never conclude "assign/metadata churn" from
    the stale array. (Seen: a lead saw `updatedAt` past its own comment but the array still
    showed its comment as newest, filed it as churn, and a maintainer's "push the two doc lines
    and I'll re-approve" waited hours.) `updatedAt` past your last action = real, full stop.
  - **A truncated comment slice (`.comments[-1]`, `[-3:]`) is NOT evidence of anything — the
    TIMELINE is the echo authority.** A fixed-size slice silently drops every event older than
    its window, so "last comment is mine/known → echo" can be judged against a view that never
    contained the event the notif fired for. An echo verdict is legitimate ONLY after
    accounting for EVERY event since your own last action: fetch `gh api
    repos/<R>/issues/<n>/timeline` (tail) or the full comment list filtered since your
    last-known timestamp, and match each event to something you've already read. Any unaccounted
    event → fetch its content before any verdict. (Repeat offender: multiple "self-echo
    confirmed" calls where a slice hid a real comment — every one was luck, not verification.)
- **The watchlist is a flat file** (one `owner/repo NUMBER` per line, `#` comments OK),
  re-read every cycle — edits apply without restarting. **Opening a PR ⇒ append it to the
  watchlist in the same step**; prune merged/closed when convenient (a stale entry is
  harmless, a missing one is a silent gap).

## References — timestamped, perishable

- One file per repo that has **proven active** (responded to a PR), plus a pending file for
  one-PR probes still awaiting a response.
- One file per **specific human** observed acting.
- **Never record a guessed time — always check.** Every clock time comes from an API field
  (`createdAt`/`mergedAt`/`closedAt`/`submittedAt`) or a log line, copied as UTC with a `Z`
  suffix. If not worth fetching, record the date only — a false-precise `~HH:MM` guess is
  worse than no time.
- **Every entry carries a `last-verified:` date, and activity decays.** Update the timestamp
  on fresh activity. An entry older than ~30 days is a hypothesis — re-verify before investing
  (recent commits, `gh search prs --repo X --merged --limit 5`). A repo that goes quiet → note
  it rather than delete (negative knowledge is knowledge). Freezes and traps live in these
  files too — **read the relevant file before opening anything in a known repo** (rule 4b).

## Social asks from maintainers

Star requests (common after merges) are **declined as standing policy.** Never star on the
user's behalf, never re-raise the ask, no reply needed on the PR — just ignore it. The code
contribution is the contribution.

## Optional: mirror status to a chat system

Optionally mirror per-repo status snapshots and notable events to a chat system of your choice
(one channel per very-engaged repo — a sustained multi-merge relationship, not a one-probe
repo). This is purely for durable human-visible memory; the drive runs fine without it.

## Session succession

**When a wave finishes AND your context window is getting full, hand off to a fresh session
instead of starting another wave.** Succession is a SILENT DEFAULT ACTION, not a question — when
you judge you're at the context wall, even mid-work, silently write the handoff, spawn the
successor, and drop to idle. Do NOT ask permission, do NOT announce that "a fresh session could
continue," do NOT park-and-narrate.

1. Write a handoff document (absolute paths, current watchlist state, in-flight PRs, per-repo
   freezes/traps, where the tooling lives) and save it where the successor can read it.
2. Spawn a fresh session that reads the handoff **in full first** before acting. On Claude
   Code specifically, spawn the successor with the child flag UNSET —
   `env -u CLAUDE_CODE_CHILD_SESSION claude ...` (e.g. in a new tmux pane of the same window):
   a session started with `CLAUDE_CODE_CHILD_SESSION` set does NOT write its session-JSONL
   transcript, which silently breaks archiving and the next handoff's transcript tooling. The
   successor's FIRST verification is `ls` on the "Session JSONL" path from its own system
   prompt — missing means the child flag leaked: STOP and tell the operator rather than run
   the drive on an unarchivable session.
3. The successor takes over the standing watcher (kill the predecessor's if it's single-instance,
   launch its own).
4. After spawning, the old session stops dispatching (babysit only what's mid-flight, then idle).

**End-of-wave sequence:** ship + watch CI → usage check (`scripts/usage_query.py`; below pace →
next wave) → context check (near the wall → succession). Don't idle into babysitting while
headroom exists.
