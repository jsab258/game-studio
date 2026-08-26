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
- **A PROBE MUST REPRODUCE THE FAULT BEFORE IT CAN SAY WHAT FIXES IT**, and
  this is 5b aimed at the other half of the pair. A guard is tested on the
  case it should PASS; a probe is worthless on a case where the fault does
  not OCCUR. Named incident: two A/B probes were run to decide whether a
  prompt change had removed a text artefact from a generated texture. Both
  came back clean, the change was declared unnecessary, and the full-size
  image landed hours later carrying the artefact. **Neither probe had ever
  exhibited it.** "Both clean" reads as *the fix is unnecessary*; the only
  honest reading is *this probe did not reproduce the fault, so it measured
  nothing about the fault*. The caveat was even written down — "a probe
  result may not transfer" — and quoted in the same breath as the conclusion
  that ignored it. **Before a probe decides anything, ask what it would look
  like if the fault were present, and confirm the control case shows it.**
- **A guard that refuses the accepting fixture is WITHDRAWN, not tuned.**
  Live instance: a screen written to reject clips named after costumed
  characters was run against the 65 shipped animation clips and refused two —
  the intended one, and the default idle every character in the game plays
  while standing still. The names could not distinguish "the motion is a
  monster's" from "the file was exported off a monster rig". Shipping it
  would have emptied the most-used asset in the project to fix one nobody had
  looked at. The replacement screened the axis the fault was actually on and
  refused exactly one of 65. **Put the fixture it wrongly refused into the
  accepting table BY NAME**, so the withdrawal cannot be quietly undone.

## 6. Built is not running

A feature is not done when its module is tested. It is done when something
calls it and a gate proves the call happened. When you finish a system, grep
for its call sites before saying it is finished. Keep a **reach ledger** —
public APIs with no caller, fetched assets no code names, systems with no
frame that shows them — and treat its entries' *reasons* as decaying
comments (rule 1).

**THE WIRING IS ASSERTED IN THE TEST, READ OFF THE SOURCE.** A class can be
complete, careful, and constructed nowhere. Named incident: a 170-line
publisher — plain-English message for every failure path, incremental
delivery so a four-hour run that dies at hour three has still delivered —
was never instantiated. Its only live call site passed `publisher=None`;
every other call to it was a selftest. It sat dead for eleven days while a
person carried files by hand, and the report told them it had sent. **A test
that the class behaves correctly is worth nothing while nothing calls it**,
so the selftest now parses this file's own source and asserts the live entry
point constructs it and passes it. Removing the argument turns the test red.

**AND MADE IS NOT DELIVERED.** The same run had a second half of the same
fault: only items it WROTE were handed to the publisher, so a run where
everything was already on disk pushed the manifest, the report, and not one
of the fourteen files it existed to deliver. **The question an output stage
answers is "is this artefact where it needs to be", never "did this run make
it."** Assert the COUNT, not that something was offered — one missing name is
one artefact nobody backs up.

**AND A FIX CANNOT DELIVER ITSELF.** A self-updating script that pulls before
running cannot fix its own first run: the copy on the machine is the old one,
without the pull. **The first run after any change to a launcher is always
the old launcher.** Fingerprint the file across the update, and if it changed,
re-launch once — guarded so it is strictly once, because a loop there is
worse than the hole. This also closes a quieter fault: a shell reads a script
line by line AS IT RUNS, so an update that rewrites it mid-run leaves the
shell reading from a byte offset into different text.

## 7. Estimates name what dominates, or are not given

Before an ETA, check the thing is actually running and what is queued ahead
of it. State what dominates (usually the CI round trip) and what could blow
it up. "I don't know" beats a number you will retract.

## 8. "I will come back to you" requires arming something

Ending a turn does not schedule a wake-up. If you say you will report back,
start a watcher in the same turn that fires on the condition or a timeout.
No watcher, no promise.

**AND AN UNATTENDED RUN MUST NEVER BE ABLE TO WAIT FOR A HUMAN.** Every
script that shells out to a tool which can open an editor or prompt for a
credential must say so up front, or it hangs in a window nobody is watching
and looks identical to slow work. Swept once on a real project: **22 scripts
ran `git`, and not one guarded the editor.** One of them made a merge commit,
`vim` opened, the window was closed, and the half-finished merge blocked every
update afterwards behind a message that named the state and not the cause.

- Set the guard **in the clone or the config, not only in the shell** that
  runs your own scripts — the same person also runs the tool by hand and from
  a desktop client, and a variable set in one script reaches none of that.
- Prefer **a fast named failure over a wait**: an unattended run that stops
  and says "could not sign in" is a sentence in a file; the same run waiting
  on a prompt is a lost night with no diagnosis.
- **Recovery must FINISH the succeeded case, not undo it.** A merge stopped at
  the message has already merged every file and conflicted on none — aborting
  it throws away good work and re-runs the same prompt next time. Ask whether
  there are unmerged paths; that is the question that separates the two.
- **A lint that greps every script for the guard is the cheap half.** The
  sweep is what found 22 of 22; a rule that relies on remembering decays.

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

### MEASURE THE STUDIO'S OWN OVERHEAD, or it eats the project

This framework is an instrument pointed at a project. Nothing in it was
pointed at ITSELF until an owner asked why a night had cost so much, and the
answer had to be measured rather than recalled:

> **110 agent spawns in one day. 39 were instrument-builders, 23 were the
> director. 78 of 110 — 71% — were the project working on itself; 32 built
> the game.**

Every one of those spawns was defensible on its own. The proportion was not,
and nobody could see the proportion, because the spawn log recorded WHICH
AGENT and never WHICH KIND OF WORK. A studio framework is uniquely prone to
this: it makes measuring, reviewing and auditing cheap and legible, so those
grow, and building the thing stays as hard as it was.

**The instrument is one column and a share, printed where nobody has to
remember to look.** Split the agent roster into the ones that BUILD THE
PRODUCT and the ones that measure, review or audit it, count the day's
spawns each way, and print the share into the verify footer that rides into
every commit message. `gameShareDay=32/110@<date>`.

- **A literal set, not a naming rule.** No convention carries this: an agent
  called `instrument-builder` is a builder by name and overhead by purpose.
  Names in neither list count as overhead — an unrecognised agent is not
  evidence that the product got built.
- **Print it, do not gate it, until there is a landed series.** A bound set
  from one day is invented (rule 2). What the number is for at first is a
  person seeing `0/22` on a day that felt productive.
- **The same discipline as any other reading**: it is a COUNT over one UTC
  day, the date is carried in the value so a quiet log cannot read as today,
  and it ships its denominator.

### THE PARK-AND-RESUME TEST

**The benchmark this framework is built against: someone clones the repo cold
and continues at full speed, losing nothing about HOW the work is done.** Not
the code — the process. That is a testable claim and it is worth testing,
because every mechanism here decays toward "the person who set it up
remembers".

Ask it as a question with a checkable answer. On any parked project:

- **Does the first screen of `queue.md` say what to do FIRST, and why that
  order?** Not the most interesting item — the one that makes the others
  cheaper or possible. A prioritised list is not a starting point.
- **Does it say what state the project is IN?** Parked, mid-flight, blocked,
  waiting on a person. "Nothing is broken and nothing is running" is a fact
  the next session cannot derive and will waste a turn establishing.
- **Are the restart mechanisms named by ID, with the action spelled out?** A
  disabled watchdog and a dead one look identical.
- **Does `CLAUDE.md` still describe the machinery that exists?** It is the
  file read every session, so a false sentence there is the most expensive
  kind. When one is found, CORRECT IT IN PLACE AND QUOTE THE OLD WORDING —
  a deleted error is one the next reader re-derives from scratch, and the
  most convincing false sentences are the ones that were true when written.
- **Is the tree clean and pushed?** An ephemeral environment holding
  uncommitted work is a project that can stop silently.

---

## The standard

> {{Fill in: the quality bar, in the words of whoever set it, with the
> date. The extracted project's bar was set by its owner twice in one
> conversation over the assistant's hedging — record yours the same way, so
> no future session re-derives it differently.}}
