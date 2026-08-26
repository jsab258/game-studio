---
name: land
description: "Read a CI landing in the mandated order: provenance, stills, verdict, gates — then route findings. Use the moment a build lands, before any conclusion about what it showed. The order is the content: every step exists because reading them in another order produced a wrong published conclusion."
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Task
---

# Land — read a build

The order below is not a preference. Each step is upstream of the next
because reading them the other way round has each produced a specific,
recorded wrong conclusion.

## 1. Provenance — whose evidence is this?

Read the verdict's line 1 (the commit and timestamp) BEFORE anything else,
and check it is the commit you dispatched — the newest file can hold the
older answer when two builds land out of order, and a specific question is
answered from the per-run copy (`runs/<sha>.txt`-style), never the default
file.

Then the no-run check: if the verdict says the equivalent of `NO RUN`, stop
here — a failed run may still have committed its stale checkout's stills,
and a picture in the output directory is only evidence about the commit
named beside it if that commit actually ran. Read the compile/error block
before re-dispatching anything.

## 2. The artifacts, whole — before any gate

Open every still (or spawn the artifact-reader to do it). A gate reports
what it was built to ask; the frame reports what is there. Faults found by
a person opening a picture, after gates certified the build green,
outnumber faults found by gates in the extracted project's history.

Anything wrong in a frame is a HYPOTHESIS (a picture is good evidence that
something is wrong and poor evidence of what) — the deliverable for each
visual finding is the quantity to print next run, not a fix chosen by eye.

## 3. The verdict, with statistics discipline

- Distinguish "the run completed" from "the run measured anything" — a
  truncated run's missing done-line means every end-of-run metric reads as
  absent, which is not the same as zero.
- Any new number lands with its classification (peak / median / last-wins
  / cumulative) before it enters any conclusion.
- A red gate is read against its detail operands, then against the frame.
  A red does NOT mean the build is broken — a red gate marks the whole job
  failed on most CI, and the colour is the least informative thing about a
  run.

## 4. Route

For each finding: a fix this session (queue top), a number to add
(instrument-builder), a decayed claim discovered (claim-auditor confirms,
then fix), or a question for the owner (rare — only if a decision is
genuinely theirs). Update the queue BEFORE starting the next work item, so
the landing's knowledge survives the session.

Where a finding changes a conclusion, that is trigger 3 in the autonomous
variant — the routing decision is the director's.
