---
name: close
description: "Close a queue item properly: the done-checks, the quality-ladder question, the claim sweep, and the move to history. Use when work on an item appears finished — 'appears' because most of this skill is the checks that have overturned that appearance before."
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Task
---

# Close — an item leaves the queue

## 1. The done-checks, in order

- **Built is not running:** grep the call sites. Something outside the
  tests calls this, or it is not done (rule 6 — a whole milestone once
  shipped with ~40 of 61 APIs called by nothing).
- **The instrument exists:** which number will show the NEXT session this
  works, without reading the code? If none, the item is not done — route
  to instrument-builder.
- **The artifact shows it:** for anything visible, a frame/page/file a
  reader can point at. A green gate does not substitute for the artifact
  it summarizes (rule 4).
- **The claims are swept:** the change falsified comments somewhere —
  yours and other files'. Grep the key nouns; fix what the change made
  false, including the negative claims ("X is not wired") that decay
  fastest. Consider a claim-auditor pass for large changes.
- **The twin is greped:** the fix's distinguishing token, every other hit
  read. One idea, two implementations; the unread one is missing the line.

## 2. The quality-ladder question

**Is this the best available result, or the first working one?** The first
version of anything tends to be the first thing that worked, declared done
because it ran. Name the next rung from resources already available (the
better asset already fetched, the 2K where 1K was wired, the map nothing
samples). Take it now, or write it onto the ladder with a name. A blank
next-rung is a research task, not a finished aspect.

In the autonomous variant this question is the director's call (trigger 5) —
spawn `studio-director`; human-paced, the resident holds the charter.

## 3. The move

- The item's OPEN remainder (if any) stays in the queue, compressed to the
  follow-up and where the full account lives.
- The closed reasoning moves to the history file whole — it is usually the
  valuable part, and the queue's line cap exists to force exactly this
  move. An item whose closed reasoning stays in `## Now` reads as work
  outstanding and sends a future session at it again.
- If the close changes the roadmap's truth, fix the roadmap row NOW — a
  row describing shipped work as open is the second-door-system generator.

## 4. The commit

Verify green, footer pasted from the file, message stating what was
measured — not just what was changed. If tests fail or a step was skipped,
the message says so plainly; a claim of success that a later session
overturns costs more than the honest gap.
