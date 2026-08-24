# The work stack

> **STATUS — LIVE**, verified {{DATE}}. What gets picked up next, in order.
> The plan is the roadmap and it wins; this is the next few hours of it.

## Why this file exists, and how to use it

The next items are written down BEFORE a dispatch and taken from the top
afterwards, so no judgement is required at the exact point where judgement
fails — the moment after a dispatch is a decision point, and re-deriving
priorities from a long roadmap at the end of a long turn is friction
enough to lose to. The extracted project measured the failure: four gaps
of twenty to thirty minutes in one afternoon, each right after a dispatch,
with the rule already written.

- **Every item fits inside one build round trip**, or it gets split.
- **CI-needed items are marked** and batched into the next dispatch.
- **Take from the top; move finished items out** — to the history file,
  keeping only the open remainder here. The line cap (enforced by
  docs-check) is what forces the tidy; an item whose closed reasoning
  stays here reads as work outstanding.
- **`## Standing work` never empties.** When `## Now` has nothing
  startable, decompose a standing item into it — a refill signal, not a
  stop signal. An empty list reads exactly like an empty afternoon, and
  the two have opposite next actions.
- **Order by the owner's stated priority sequence, then by what shows on
  screen.** The top of `## Now` is the item a user would notice, every
  time.
- **Before an item is closed, the quality-ladder question:** is this the
  best available result, or the first working one? The next rung gets
  taken now, or goes onto the ladder below with a name.

---

## Now

1. **{{ITEM}}** — {{what, why it is here, what done looks like as
   something measurable, and — if a prior conclusion is involved — which
   number supports it}}

## Standing work

- {{An unbuilt milestone to decompose}}
- {{A system to sweep for decayed comments (claim-auditor)}}
- {{A still/artifact finding to turn into a number (instrument-builder)}}
- {{The reach report's top disconnection to wire (reach-auditor feeds this)}}

## Quality ladder

| aspect | current rung | known next rung |
|---|---|---|
| {{aspect}} | {{what ships today}} | {{the better result already within reach — blank means this row is a research task, not a finished aspect}} |
