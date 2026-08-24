---
name: start
description: "Guided setup for a NEW project on this template, in dependency order: premise, feedback channel, verify, queue, constraints. Use once, at project start — or run it against an existing adoption to find which foundations are missing. Each step states why it precedes the next."
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion
---

# Start — foundations, in the order that matters

Work through these WITH the owner — several steps are their call, in their
words, recorded verbatim. Skip nothing silently; if a step is deliberately
deferred, write that down where the step's output would have lived.

## 1. The premise (CLAUDE.md section 0)

Before any code: what IS this project? Setting/domain, the
non-negotiables, what is bought vs fetched, the quality bar — in the
owner's words, dated. This is first because nothing downstream can catch a
wrong premise: every other failure gets caught by a measurement eventually;
this one re-frames the measurements themselves.

## 2. The feedback channel (rule 12)

Before features: how will a session READ what the project actually does?
The answer that has survived: a CI job that runs the project headless and
COMMITS its evidence — rendered frames, a `key=value` verdict naming its
commit on line 1, per-run copies. Set this up before it is needed; every
hour spent here repays itself the first time a gate goes red.

If the project cannot yet run headless, making it runnable IS the first
milestone — not a nice-to-have after features exist.

## 3. Verify and the gate

Wire `tools/verify.py`'s check list to the project (lint, tests, whatever
must be green). Confirm the commit gate on BOTH outcomes: a green commit
passes, a post-verify edit blocks. A gate that blocks good commits gets
disabled within a day and takes the hooks' credibility with it.

## 4. The queue and the roadmap

Instantiate `templates/queue.md`; write the roadmap with milestone entries
per `templates/milestone.md` — each with a MEASURABLE done-state, and where
one cannot be measured yet, the instrument to build is that milestone's
first item. Seed `## Standing work` so the queue cannot empty.

## 5. The constraint lists

Fill `engine-specialist.md`'s constraint list and `content-wrangler.md`'s
sourcing rules with what is known TODAY, and treat both as living: every
constraint discovered expensively later gets written in the day it costs
something, with its incident. An empty constraint list on day one is
honest; an empty one after month one means the learning is being lost.

## 6. First dispatch

One end-to-end pass: a trivial change, verify, commit through the gate,
dispatch, watch by ancestry, `/land` the result. The point is to find
which link is broken while everything is still small — the channels are
the project's nervous system, and debugging them under deadline is how a
night gets spent inferring facts from a step's duration.
