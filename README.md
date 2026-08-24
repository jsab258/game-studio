# Measured Studio

A Claude Code studio template for building games (and other long-running
projects) **measurement-first**. Agents, hooks, rules, skills and document
templates — extracted from a real project that ran autonomously for weeks,
where every rule below was paid for by a named failure before it was written
down.

The premise, and the one design principle that separates this from other
studio frameworks:

> **Every document is a claim, and a claim without an instrument decays.**
> A design doc, a roadmap row, a code comment, an agent's report — all of
> them are claims. The framework's job is not to make more of them; it is to
> attach a number to each one and print it where the next session will look.

Other frameworks give your AI session the *ceremony* of a studio — design
reviews, sign-offs, story workflows. Ceremony validates that documents exist.
This template validates that the thing the documents describe actually
happened: a gate that reads a rendered frame beats a checklist that reads a
heading.

## What's inside

| | what | why |
|---|---|---|
| `CLAUDE.md` | The operating rules, as a template | The distilled epistemics: never assert unchecked, thresholds from printed series, every zero ships a denominator, suspect the instrument first, open the artifact, test guards on the case they should PASS, built-is-not-running |
| `.claude/agents/` | A small tiered roster | Tier 1 decides (Fable), Tier 2 verifies adversarially (Opus), Tier 3 builds (Opus). Verifiers are mechanically read-only — an agent that cannot write code cannot "fix" what it was asked to judge |
| `.claude/hooks/` | Hooks with teeth | The commit gate BLOCKS a commit unless the verify run is green and fresh; the SubagentStart hook logs every spawn to a tracked `.claude/agent-log.tsv`, so "the director was called" is a number rather than a memory — a rule that depends on the model remembering it is a rule that decays |
| `.claude/rules/` | Path-scoped standards | Loaded when editing matching files, so instrument discipline surfaces exactly where instruments are written |
| `.claude/skills/` | Workflow skills | The working loop: queue discipline, batched CI dispatch with ancestry watchers, stills-before-gates review, close-with-the-ladder |
| `tools/` | The verify skeleton | One command; green writes a footer file, red deletes it; commits paste the footer with `-F`. Pluggable checks per project |
| `templates/` | Document templates | Each one carries the question "what number proves this, and where does it print?" |
| `docs/` | Adoption guides | Including how to apply this to an ALREADY-RUNNING project without losing anything |

## The tier model

```
Tier 1 — Direction (model: fable — on-demand)
  studio-director        binding decisions, conflict resolution, premise-keeping

Tier 2 — Verification (model: opus, read-only by construction)
  measurement-auditor    is every number the statistic its name claims?
  claim-auditor          which comments/docs/reports went stale when the code moved?
  artifact-reader        open the actual frame/page/file; a gate is not a picture
  guard-tester           has every guard been run on the case it should ACCEPT?
  reach-auditor          built is not running: what has no caller, no consumer, no frame?

Tier 3 — Execution (model: opus)
  systems-builder        gameplay/simulation code, in the codebase's own idiom
  instrument-builder     probes, gates, verdict keys — the measurement half of every feature
  engine-specialist      engine-specific work, carrying the CONSTRAINT knowledge
                         (what compiles where, what the CI round trip costs)
  content-wrangler       asset fetching, attribution, licence discipline, reach ledgers
```

**Resident session.** In a *human-paced* loop the resident IS the director,
on the top model. In an *autonomous* loop the resident is an opus
coordinator and the director is spawned on mandatory triggers. Pick one at
adoption — the selector question, the trigger list and the gate that blocks
a commit until you answer it are in CLAUDE.md's
["The studio split"](CLAUDE.md) section.

Why capability concentrates at the DIRECTION ROLE and at verification, and
why verification outranks execution: the expensive failure mode of an AI
studio is not bad code, it is a **plausible unverified claim** — an agent
reporting success that nothing checked. Builders produce claims; verifiers
produce accusations; accusations are cheap to check. So the verifiers get a
strong model and no write access, and the direction role gets the strongest
model there is, because judgment is the scarcest resource in the loop.

Whether that role lives in the *resident session* is a separate question,
and it is answered by who paces the loop: the two coincide only when a human
is in the loop. An autonomous resident wakes dozens of times a day on
watchdogs and completions, re-reading its whole context each wake, so a
top-model resident there buys routing at judgment prices — the role moves to
an on-demand agent and the resident becomes a coordinator. Its escalation to
the director is then MECHANICAL rather than discretionary, because the known
failure mode of a cheaper resident is under-escalation, and a session that
does not know what it does not know cannot be asked to notice.

## Quickstart

1. Copy this repository's contents into a new project (or run the adoption
   guide in `docs/adopting.md` against an existing one).
2. Fill in `CLAUDE.md`'s marked sections — the premise block first. It is
   first because a wrong premise quietly re-frames every judgement made on
   top of it, and nothing else in the file will contradict it.
3. Wire `tools/verify.py`'s check list to your project (lint, tests, doc
   checks — whatever must be green before a commit).
4. Set up the one feedback channel that matters: a CI job that runs the
   project headless and **commits its evidence into the repository** —
   screenshots, a `key=value` verdict file, per-run copies. Everything else
   in this template assumes that channel exists, because a feedback channel
   the session cannot read is the highest-leverage bug on any board.
5. Work from `templates/queue.md`. Take from the top; refill from standing
   work; let the line cap force the tidy.

## Provenance

Extracted from LEDGER, an autonomously-developed Unity game, and synthesized
with the packaging ideas of
[claude-code-game-studios](https://github.com/donchitos/claude-code-game-studios)
(MIT) — whose agent-definition format, path-scoped rules and hook wiring are
the best parts of that project. The difference in philosophy is stated at the
top of this file; both things are true at once: their structure is good, and
structure without instruments is a checklist a model fills in.

## License

MIT.
