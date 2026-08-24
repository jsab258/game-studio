# CLAUDE.md — how to work on {{PROJECT_NAME}}

Read this first, every session. It is not style guidance. Every rule below
was paid for by a real failure on the project this template was extracted
from; the incidents are summarized so the rules are believable rather than
decorative. **As your project breaks these rules in its own ways, write the
incident in beside the rule** — a rule with a named failure is read
differently from a rule that is merely sensible.

---

## 0. WHAT {{PROJECT_NAME}} IS

> **Fill this in before anything else, and keep it at the top.**
>
> {{One paragraph: the premise. Setting, era, tone, the non-negotiables.}}
>
> {{The standing constraints that must never be re-derived: what is
> purchased vs fetched, whose accounts are used, what the quality bar is
> and who set it, in their words, with the date.}}

This section exists because the extracted project's assistant once asserted
the wrong *decade* for the game's setting — four times in one conversation,
while every document stated it correctly — because nothing it read every
session said what the game WAS. A wrong number gets caught by the next
measurement; a wrong PREMISE quietly re-frames every judgement made on top
of it. Nothing below can catch it. Only this section can.

---

## 1. Never assert what you have not just checked

Before stating a fact about this repo — what exists, what is wired, what
shipped, what a number is — run the command that proves it, in the same
turn. A memory of having checked is not a check. If you cannot check, say
"I have not verified this."

- **Your own comments and docs are not evidence.** Read the code. (Paid for:
  four voice candidates reported as four people were one person four times —
  the claim came from a comment, not the code.)
- **When you change code, you have changed the comments about it.** Before
  finishing a change, re-read the comments on everything it touched —
  including ones you did not edit — and grep for the claim you have just
  falsified elsewhere. A comment is a claim with no test attached; it decays
  silently, and the decay is invisible in a diff that does not touch it.
- **When you fix a bug, grep for the same bug.** One idea, two
  implementations, and the one nobody looks at is the one missing a line.
  The moment a fix works, grep for its distinguishing token and read every
  other hit. Ten seconds against a lost afternoon.

## 2. Never set a threshold you have not measured

If you need a threshold, first make the system PRINT the value, run it,
look, then set the number from the evidence. When a gate is failing, ask
whether the instrument or the subject is wrong before touching either.

The statistics traps, each one paid for:

- **A peak answers "did it ever"; a median answers "is this normal"; neither
  answers the other.** Print the series; a summary is never the evidence.
- **"Is anybody…" is never a median question** — any fault touching fewer
  than half the population is invisible to a median, however severe.
- **Two numbers derived from one variable are one number twice.** Before
  printing a pair as evidence, read the code that produces them and ask
  whether either can move while the other stands still.
- **Two maxima cannot be divided.** Capture the denominator AT THE INSTANT
  the numerator peaks, and name it so (`xAtWorst`).
- **A cumulative number read by a sparse sampler freezes at the last
  sample.** Read lifetime counts where the run ENDS.
- **A number keeps its name when the question it answers moves.** When you
  change what a system does, re-read what its numbers ask.
- **The number most likely to be wrong is the one you wrote an hour ago.**
  Before a new number enters a conclusion, say which of
  peak / median / last-wins / at-worst it is, and whether that answers the
  question being asked. One sentence; it catches most of the above.

## 3. Suspect the instrument first

When a result is surprising, check the ruler before the reading. When your
own analysis says something is missing, open the file and look — an analysis
(including a doc's "still open" list, including a reach report) is a claim,
not evidence. The extracted project once built a second door system, with
tests, four lines from the call site of the first, because a roadmap said
doors were missing.

## 3b. A zero needs a denominator

Every zero, every "none", every clean result ships with the count of what
was examined — or "nothing found" and "nothing looked at" print identically.
A linter that reports 0 errors must report how many things it walked. A
budget that never refuses anything is indistinguishable from one that is
not wired.

**A truncation is a zero with the same problem:** any cap on what gets
reported must say when it bites (`(+N more not shown)`), or a filter that
quietly stopped telling you things reads as a finding.

## 4. Open the artifact you are shipping

If the deliverable is a page, open it at the size it will be used. If audio,
check duration and metadata. If a file, read it back. If a build, **look at
the rendered frame before reading any gate** — gates report what they were
built to ask, and three visual faults in the extracted project sailed
through green gates that were all asking about something else.

**And looking is not measuring.** A picture is excellent evidence that
something is WRONG and poor evidence of WHAT or WHY. A visual judgement is a
hypothesis; before acting on it, make the run print the quantity and read
that. When a still shows a fault, the durable fix includes a NUMBER that
would have caught it.

## 5. Look before you destroy, and make the guard know the difference

Before any delete or overwrite, look at what is there. Scope destructive
commands to exactly what the operation produced. Copy anything a human spent
time on somewhere the pipeline cannot reach. A guard that cannot tell a
regression from an improvement is a ratchet — "refuse unless perfect"
throws away partial success, and partial success is what real work looks
like.

## 5b. A guard must be tested on the case it should PASS

A guard has two outcomes; shipping it means having watched BOTH. Run it
against input it must accept as well as input it must reject — the expensive
failure is a validator nothing survives, and it reports as "nothing
happened" rather than "something broke". If the accepting case cannot be
produced locally, say so in the commit.

- **The live codebase is the best accepting case there is** for any
  name-matching or convention-checking tool: every hit on today's code is a
  false positive by definition, and it cannot be fooled by a fixture you
  wrote yourself.
- **A probe also needs a run in which the thing it asserts can happen.**
  The fix for a probe that only fires on lucky runs is to PLANT the
  condition, never to loosen the bound.
- **Keep a `--constant` sweep**: list every metric that has never been
  anything but zero across all kept runs. A reading cannot go red; only a
  person noticing "this number never moved" catches a dead branch.

## 6. Built is not running

A feature is not done when its module is tested. It is done when something
calls it and a gate proves the call happened. When you finish a system, grep
for its call sites before saying it is finished. Keep a **reach ledger** —
public APIs with no caller, fetched assets no code names, systems with no
frame that shows them — and treat its entries' *reasons* as decaying
comments (rule 1).

## 7. Estimates name what dominates, or are not given

Before an ETA, check the thing is actually running and what is queued ahead
of it. State what dominates (usually the CI round trip) and what could blow
it up. "I don't know" beats a number you will retract.

## 8. "I will come back to you" requires arming something

Ending a turn does not schedule a wake-up. If you say you will report back,
start a watcher in the same turn that fires on the condition or a timeout.
No watcher, no promise.

## 9. Do not block yourself

Know what your pushes trigger. Expensive CI jobs are opt-in
(`workflow_dispatch`), concurrency groups are scoped to the expensive job
only, and cheap checks never queue behind a stream.

## 10. Documents

- Every doc declares **LIVE / SPEC / LOG** in its first lines, enforced by
  `tools/docs-check.py`: a LOG carries its date and says NOT CURRENT, a
  LIVE plan carries a verified date and stays under 400 lines.
- **The roadmap is the tiebreak for what to do next and contains the plan
  itself** — not a pointer to the plan. History goes to a history file.
- A milestone entry states what is in it, why it sits there, **what done
  looks like as something measurable**, dependencies, and risk.
- The roadmap is a claim about priorities, never a report on what the code
  contains — its "still open" lists decay exactly like comments (rule 3).

## 11. Scope: do the asked thing

A question is a question. Answer it, and offer the work separately.

## 12. If you cannot read the output, fix that before anything else

A blocked feedback channel is not an inconvenience to route around; it is
the highest-leverage bug on the board. Prefer a channel this environment can
definitely read — **in a repo that means a file committed by CI**: rendered
stills, a space-separated `key=value` verdict, per-run copies keyed by
commit. Log-tail APIs, step summaries and artifact hosts have all failed the
extracted project; a committed file has not.

- **A verdict value may not contain a space** — everything that reads
  `key=value` splits on whitespace and truncates silently.
- **The verdict names its commit on line 1** — two builds landing out of
  order otherwise leave the newest file holding the oldest answer.
- **A run that produced nothing must say so** (`NO RUN — nothing was
  measured`), and must not carry forward the previous run's files as if
  they were its own.

---

## Project mechanics

> {{Fill in: what compiles locally vs only on CI, what the CI round trip
> costs, how builds are dispatched and watched, licence/seat constraints,
> what the container/environment can and cannot reach. The extracted
> project's list is a good model: name the traps, with the incident.}}

**Always run `tools/verify.py` before committing, and paste the footer from
the file** (`tools/.verify-footer`; a green run writes it, a red run deletes
it — so a red run has nothing to give you):

    python3 tools/verify.py && git commit -F msg.txt
    # where msg.txt ends with the contents of tools/.verify-footer

Write the message to a FILE — never an unquoted heredoc, which executes
backticked identifiers and commits a sentence with a hole in it.

The commit hook (`.claude/hooks/verify-gate.sh`) enforces the footer's
freshness mechanically. It exists because "remember to run verify" is a
rule, and this file is mostly a list of rules that decayed.

---

## The studio split — choose the variant

**The selector question: is every turn paced by a human, or does the loop
run autonomously?** Answer it here, by replacing the mark below with one of
the two words. `tools/verify.py` FAILS until you do — undeclared is not a
default, because the failure mode of skipping this question is a director
that exists and is never called, and that failure is invisible from inside
the session having it.

    {{VARIANT: human-paced | autonomous}}

Capability concentrates at the DIRECTION ROLE, not at the resident session.
The two coincide only when a human paces the loop.

**Human-paced variant.** The resident session IS the director, on the top
model, and the tier-2/tier-3 roster ships unchanged. The trigger list below
still names the moments that ARE direction moments — read it as guidance,
because here the human is the enforcement and the escalation kit is not
copied. `director_cadence` passes, printing that it is not enforcing.

**Autonomous variant.** The resident is an **opus coordinator that decides
nothing binding**: it routes, spawns, reads landings, and keeps the queue.
The `studio-director` agent is spawned MANDATORILY on these triggers —

1. builder-batch review before any commit of builder work
2. queue reordering or refill
3. a landing that changes a conclusion
4. verifier-vs-builder disagreement
5. close-outs (the quality-ladder question)
6. anything touching the premise, the roadmap, or CLAUDE.md

— and mandatorily means mechanically. A judgment-based "escalate when it
matters" rule asks the cheaper model to know what it does not know, and the
known failure mode of a coordinator is under-escalation. The extracted
project's owner set the condition the whole arrangement is judged against
(2026-08-24): *"we need to be 100% sure it works. no point in having a fable
director if it's never called upon."*

**The triggers bind regardless of the doorway** — a skill step that performs
a trigger act (`/close`'s quality-ladder question, `/land`'s routing of a
finding that changes a conclusion) is a director spawn in the autonomous
variant, not an exemption from one.

**The coordinator's charter is THIS SECTION — there is no coordinator agent
file, and you should not create one.** The resident is the main session, not
a subagent; a charter in an agent file would describe a role nothing spawns.

Three mechanical enforcements, required in the autonomous variant:

- **Every spawn is logged.** `.claude/hooks/agent-log.sh` (SubagentStart)
  appends `when<TAB>agent<TAB>model` to a tracked `.claude/agent-log.tsv`.
  Read it with
  `sed 1d .claude/agent-log.tsv | cut -f2 | sort | uniq -c | sort -rn`.
  Near-zero director rows over a working week, while commits flow, means
  the triggers are not firing — that is the observable that reopens this
  decision, not a feeling that review is thin.
- **`director_cadence` blocks the commit** when more than **{{100}}**
  changed lines under the code tree have no `studio-director` row newer
  than HEAD (`tools/verify.d/director_cadence.py`, run by `verify.py`).
  **The enforced number lives in ONE place: `MAX_UNREVIEWED_LINES` in
  that file.** The mark above only mirrors it for the reader — the check
  never parses prose, so filling the mark alone changes nothing and the
  gate goes on enforcing the constant. Set the constant, then the mark.
- **The watchdog's dailies check force-spawns a director review** if none
  has run in **{{12h}}**. This one cannot ship as portable code — trigger
  systems differ per environment — so it is wiring you must add. The
  precedent implementation is the extracted project's hourly watchdog
  trigger, which re-invokes the loop and carries the current work order in
  its own prompt.

**Both numbers are inherited from the extracted project and UNVALIDATED —
print your own series before trusting them** (rule 2: never set a threshold
you have not measured). `python3 tools/verify.d/director_cadence.py
--series` prints the changed-line count of every recent commit, newest
first, then the median and the peak, so the bound comes from your own
distribution rather than from someone else's.

---

## The working loop

- **`queue.md` is what you pick up.** Next items are written BEFORE a
  dispatch and taken from the top afterwards — the moment after a dispatch
  is a decision point, and re-deriving priorities from a long roadmap at the
  end of a long turn is friction enough to lose to.
- **The queue must not be able to empty.** A `## Standing work` section
  never empties; when `## Now` has nothing startable, decompose a standing
  item into it. That is a refill signal, not a stop signal.
- **Never wait on CI.** Dispatch the build and start the next non-CI item in
  the same turn. Batch several changes per dispatch — a round trip costs the
  same whether it carries one change or six.
- **Watch for a run that CONTAINS your commit** (an ancestry test), never
  for a branch to move or a run named after your sha — CI dispatch takes a
  branch, and the runner checks out whatever it points at when it starts.
  Capture the sha BEFORE the dispatch. And distinguish "the build carried my
  change" from "the build measured anything" — they are different facts and
  only the second is what a watcher waits for.
- **A turn ends only when nothing is startable.** Arming a watcher is the
  precondition for ending a turn, not permission to end one.
- **Commit and push the moment a thing is green.** Ephemeral environments
  roll back; every rollback so far has cost nothing because of this habit
  and nothing else.
- **Before an item is closed, ask the quality-ladder question:** is this the
  best available result, or the first working one? The next rung either gets
  taken now or goes onto the ladder with a name. An aspect whose next rung
  is blank is a research task, not a finished aspect.

---

## The standard

> {{Fill in: the quality bar, in the words of whoever set it, with the
> date. The extracted project's bar was set by its owner twice in one
> conversation over the assistant's hedging — record yours the same way, so
> no future session re-derives it differently.}}
