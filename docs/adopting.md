# Adopting into an existing project

> **STATUS — SPEC.** The procedure for applying this template to a project
> that is already running — including one mid-flight with weeks of history.
> Written against a real case (LEDGER, the project this template was
> extracted from), so the steps are the ones actually needed rather than
> the ones that sound tidy.

## The principle: adoption is ADDITIVE

This template must never require rewriting a working project. Everything it
adds lives in `.claude/` plus a handful of tools; everything the project
already has — its CLAUDE.md, its verify pipeline, its queue, its history —
stays authoritative. Where the project already implements a mechanism this
template ships (its own verify, its own queue), the project's version WINS
and the template's skeleton is simply not copied.

If an adoption step ever asks you to move, rename, or rewrite an existing
working file, the step is wrong — stop and re-read this page.

## Why drift is not a problem

The obvious worry: "the project has evolved past the template." It runs
backwards. A mature project is AHEAD of this template — richer rules, more
checks, sharper instruments — and adoption only fills the gaps where the
template has something the project lacks (usually: the agent roster, the
hooks, path-scoped rules). Nothing is lost because nothing is replaced.

## The procedure

1. **Inventory what exists.** For each template component, does the project
   already have it?

   | component | if the project has one | if not |
   |---|---|---|
   | CLAUDE.md | KEEP THE PROJECT'S — it holds paid-for history the template cannot | copy the template's, fill section 0 first |
   | verify + footer | keep the project's; note its footer path | copy `tools/verify.py`, wire real checks |
   | queue / roadmap discipline | keep the project's | copy `templates/queue.md` |
   | `.claude/agents/` | rare — merge by hand | copy whole |
   | `.claude/hooks/` | merge: keep both sets, dedupe by function | copy whole |
   | `.claude/rules/` | merge | copy whole |
   | escalation kit (agent-log hook, `director_cadence`, dailies) | if the project has its own, keep it | REQUIRED for autonomous, not copied for human-paced |

2. **Choose the variant.** One question: **is every turn paced by a human,
   or does the loop run autonomously?** Answer it in the project's own
   CLAUDE.md, in a "The studio split" section copied from the template's —
   replace `{{VARIANT: human-paced | autonomous}}` with the word.

   - **human-paced** → the resident session IS the director, on the top
     model. The declaration is all that gets set: the trigger list is copied
     as guidance, the escalation kit is not wired, and `director_cadence`
     passes printing `cadence: not enforced (human-paced variant)`.
   - **autonomous** → the resident is an opus coordinator, and the
     declaration additionally commits you to wiring the kit: the
     SubagentStart spawn log, `director_cadence` in verify, and the watchdog
     dailies force-spawn (that last is per-environment code you write — the
     template documents the contract, not an implementation).

   `tools/verify.py` goes RED until the variant is declared, so this step
   cannot be skipped quietly. It is a gate rather than a prompt because the
   failure mode of skipping it is a director that exists and is never
   called, and that failure is invisible from inside the session having it —
   which is the same reason the escalation itself is mechanical.

3. **Copy the `.claude/` layer** (agents, hooks, rules, settings.json).
   If the project already has a `.claude/settings.json`, merge the hook
   entries rather than overwriting — and re-run any existing permission
   lists on top.

4. **Point the commit gate at the project's own verify.** The hook reads
   `VERIFY_FOOTER` (default `tools/.verify-footer`); set it to wherever
   the project's verify writes its footer. If the project's verify does
   not write a footer, add that (write on green, delete on red) — it is
   ten lines and it is what gives the hook teeth.

5. **Customize the two agents that carry project knowledge:**
   - `engine-specialist.md`: replace the example constraint list with the
     project's own (what compiles where, import defaults, licence seats,
     round-trip costs). This list IS the agent's value.
   - `content-wrangler.md`: write the project's hard sourcing rules into
     the marked block (purchase policy, consent rules, licence floors).

6. **Run the both-ways tests before trusting anything:**
   - `bash .claude/hooks/selftest.sh` — all hooks, both outcomes, plus the
     selftest of every pluggable check in `tools/verify.d/` that ships one.
   - Make a trivial change, run the project's verify, commit — the gate
     must PASS a green commit (the accepting case is the half that goes
     unrun, and a commit gate that blocks good commits will be disabled
     within a day, teaching everyone the hooks are noise).
   - Touch a file after verify, attempt a commit — the gate must BLOCK.
   - **The cadence gate, both ways, actually run** (rule 5b) —
     `python3 tools/verify.d/director_cadence.py --selftest` covers it on
     fixtures, and on an autonomous project run it once for real:
     - ACCEPT: a batch over the threshold **with** a `studio-director` row
       newer than HEAD in `.claude/agent-log.tsv` — verify stays green.
       This is the half that goes unrun, and a cadence gate that blocks a
       reviewed batch will be deleted within a day.
     - BLOCK: the same batch with the log stale (or absent) — verify goes
       red and names the changed-line count and the row's age.
   - **The spawn log, both ways:** spawn any agent and confirm one new row
     in `.claude/agent-log.tsv`; then confirm the file is unchanged after
     input the hook cannot parse. An audit trail that records nothing looks
     exactly like a studio that escalated nothing.

7. **First session under the new structure:** open with the session-start
   hook's orientation, then have the tier-2 verifiers each run once over
   the existing project (claim-auditor on the highest-traffic file,
   measurement-auditor on the newest instruments, reach-auditor on the
   newest fetch). Their first findings are the adoption's acceptance test
   — on a real project they will find something, and a clean sweep on a
   project with history means the AGENTS are miswired, not that the
   project is perfect (a zero needs a denominator).

## Worked example: LEDGER

State at adoption: ~3 weeks of autonomous history, a 400+ line CLAUDE.md of
paid-for rules, `ledger/verify.py` with ~40 checks writing
`ledger/.verify-footer`, `game-design/queue.md` under a 400-line docs-check
cap, a CI verdict channel with stills — i.e. the project already had the
measurement half of everything, because that is where the template came
from.

What adoption adds there, and the whole list:
- `.claude/agents/` — the ten-agent roster (the project ran single-session
  before; the tier-2 verifiers give it parallel adversarial review it did
  not have).
- `.claude/hooks/verify-gate.sh` with `VERIFY_FOOTER=ledger/.verify-footer`
  — mechanizing a rule its CLAUDE.md could only state.
- `.claude/hooks/session-start.sh` with `QUEUE_FILE=game-design/queue.md` —
  including the rollback detector for a fault it had three times in one day.
- `.claude/rules/` — instrument and CI rules surfacing at edit time instead
  of only at session start.
- `engine-specialist.md`'s constraint list filled from its CLAUDE.md
  mechanics section (Game layer CI-only, the five name-resolution lints,
  the licence seat, the .meta/import trap).
- **The variant declaration: `autonomous`** — LEDGER's loop is watchdog-
  driven with no human pacing it, so step 2 wires the escalation kit. It
  already runs the kit natively (a SubagentStart spawn log, its own
  `director_cadence`, an hourly watchdog), which is where the template's
  version came from; adoption there is a merge, not a copy.

What adoption does NOT touch there: every tool, the queue, the roadmap, the
sim-shots channel, all history. CLAUDE.md gains exactly one section — the
variant declaration from step 2 — and nothing in it is rewritten. Time cost:
under an hour. Loss: nothing, by construction.

## Validation record — 2026-08-24

The template was validated the way its own rules demand — instantiated,
not inspected. A toy project was created from the template and every
component run against it:

- `tools/verify.py` green on the fresh instantiation, with the queue
  check exercising its has-a-queue branch (the template repo itself
  exercises the no-queue branch — both halves have now run).
- The commit gate, in the real flow rather than the selftest's fixtures:
  ACCEPTED a commit immediately after green verify, BLOCKED after a
  post-verify edit (naming the file), ACCEPTED again after re-verify.
- `session-start.sh` printed branch, uncommitted count, and the queue
  head on the toy; the hooks selftest covers its bare-repo case.
- Hooks selftest: 23/23, accepting cases first (7 commit gate and
  session-start, 15 spawn log, 1 pluggable-check selftest), plus
  `director_cadence`'s own 11/11 on fixtures.

## Validation record: the escalation kit — 2026-08-24

Added with the variant decision (`docs/hybrid-spec.md`) and validated on a
fresh instantiation, not on fixtures alone:

- **The variant gate forces the choice.** On the template as shipped the
  check prints `cadence: not armed — template not instantiated`; the moment
  `{{PROJECT_NAME}}` was filled it went RED with `studio variant not
  declared`; declaring `human-paced` turned it green printing
  `cadence: not enforced (human-paced variant)`. Three states, one file.
- **The cadence gate, both ways, in the real flow:** under `autonomous`, a
  320-line uncommitted batch with no `studio-director` row was BLOCKED
  (naming the count and `0 of 1 log rows`); the identical batch with a fresh
  director row was ACCEPTED, `tools/verify.py` green.
- **The fixtures were not enough, which is why this step exists.** Every
  fixture edited a tracked file and passed. The live run found that
  `git status --porcelain` collapses a brand-new untracked DIRECTORY into a
  single non-file path, so a 300-line new module — the commonest shape of a
  builder batch — measured as **0 changed lines** and sailed through. Fixed
  with `-uall`; that shape is now a fixture case of its own.
- **The thresholds remain unvalidated.** 100 changed lines and 12h are
  inherited from LEDGER and marked as such in the check and in CLAUDE.md.
  `--series` printed `0 1013` over this repo's history: n=2 is not a
  distribution, and the series is the instrument, not the evidence. Print
  your own before trusting either number.
