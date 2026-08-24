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

2. **Copy the `.claude/` layer** (agents, hooks, rules, settings.json).
   If the project already has a `.claude/settings.json`, merge the hook
   entries rather than overwriting — and re-run any existing permission
   lists on top.

3. **Point the commit gate at the project's own verify.** The hook reads
   `VERIFY_FOOTER` (default `tools/.verify-footer`); set it to wherever
   the project's verify writes its footer. If the project's verify does
   not write a footer, add that (write on green, delete on red) — it is
   ten lines and it is what gives the hook teeth.

4. **Customize the two agents that carry project knowledge:**
   - `engine-specialist.md`: replace the example constraint list with the
     project's own (what compiles where, import defaults, licence seats,
     round-trip costs). This list IS the agent's value.
   - `content-wrangler.md`: write the project's hard sourcing rules into
     the marked block (purchase policy, consent rules, licence floors).

5. **Run the both-ways tests before trusting anything:**
   - `bash .claude/hooks/selftest.sh` — all hooks, both outcomes.
   - Make a trivial change, run the project's verify, commit — the gate
     must PASS a green commit (the accepting case is the half that goes
     unrun, and a commit gate that blocks good commits will be disabled
     within a day, teaching everyone the hooks are noise).
   - Touch a file after verify, attempt a commit — the gate must BLOCK.

6. **First session under the new structure:** open with the session-start
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

What adoption does NOT touch there: CLAUDE.md, every tool, the queue, the
roadmap, the sim-shots channel, all history. Time cost: under an hour.
Loss: nothing, by construction.

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
- Hooks selftest: 7/7, accepting cases first.
