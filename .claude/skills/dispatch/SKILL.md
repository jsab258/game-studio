---
name: dispatch
description: "Send a batch to CI and arm the watcher correctly. Use when accumulated changes need the expensive build. Encodes the traps: capture the sha BEFORE dispatching, watch by ancestry not by name, batch to the round trip, respect the concurrency limit, and start the next work item in the same turn."
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash
---

# Dispatch — one batch, one watcher, no waiting

## Before

1. **Verify green, committed, pushed.** The dispatch takes a BRANCH, and
   the runner checks out whatever it points at when it starts — so what is
   pushed is what gets built, and unpushed work silently builds a
   different commit than you think.
2. **Batch.** A round trip costs the same carrying one change or six. If a
   change is still close, finish it into this dispatch rather than
   spending a second trip. (The measured failure the other way: one
   question per dispatch turned a day into two waves of waiting.)
3. **Concurrency.** Respect the project's stated limit (CLAUDE.md
   mechanics). Licence seats and shared runners fail SILENTLY — the
   killed build still reports, and its empty report reads like your code
   broke.
4. **Capture the sha NOW**: `SHA=$(git rev-parse HEAD)` — before the
   dispatch, never at watcher-arm time. A watcher armed later watches a
   commit the runner may never have seen, waits its full timeout, and
   NOTHING about it looks broken.

## Dispatch, then confirm what the runner took

Trigger the workflow, then read back the run's actual `head_sha` from the
runs list. If it differs from yours (someone pushed between), the watcher
watches the ancestry of YOUR sha anyway — see below — but you now know the
answer will carry more than your question.

## The watcher — ancestry, backgrounded, capped

Watch for a landed run whose commit CONTAINS your sha (an ancestry test),
never for the branch to move (your own next push fires it) and never for a
run named after your sha (dispatch does not pin commits). Background it
with a cap (~50 min) so a dead run cannot hang the loop, and distinguish
exit states: landed-with-an-answer, landed-with-NOTHING (re-dispatch, do
not wait), timed out.

```bash
SHA=$(git rev-parse HEAD)          # BEFORE the dispatch
# ... dispatch ...
# background:
for i in $(seq 1 100); do sleep 30
  git fetch -q origin "$BRANCH"
  # "landed" = a kept run whose commit is a descendant of $SHA AND which
  # measured something — the project's landed-tool encodes both.
  tools/landed --contains "$SHA" && exit 0
done; echo timed-out
```

## After — the rule that actually binds

**A dispatch is a reason to switch tasks, not to stop.** Open the queue and
start the next non-CI item in the same turn. Arming the watcher is the
precondition for ending a turn, not permission to end one — the measured
gap pattern was: dispatch, arm, stop, thirty minutes of nothing, with four
startable items sitting on the queue.
