# Decision: Resident model — hybrid is a VARIANT, keyed on loop pacing

> **STATUS — LOG, 2026-08-24. NOT CURRENT as a work order.** Implemented and
> validated this date (see the validation records in `docs/adopting.md`).
> The living text is CLAUDE.md "The studio split" and
> `tools/verify.d/director_cadence.py`; this file remains the decision
> record — the rationale, what it ruled out, and what would reopen it.

**Decided by:** studio-director (Fable), 2026-08-24, within the frame Jafar
set today in LEDGER: the split itself ("everything on fable doesn't conform
to what we agreed and consumes too much"), the hybrid resolution he accepted
(Opus resident coordinator + on-demand Fable director), and his condition on
it ("we need to be 100% sure it works. no point in having a fable director
if it's never called upon"). Quote his words verbatim wherever they appear
below when implementing.

**The question.** The template teaches "resident session = top model." The
extracted project just moved to an Opus resident coordinator with Fable as an
on-demand director. Does the hybrid REPLACE the teaching, or become a
documented VARIANT — and are the escalation triggers and cadence gate
required or optional?

**The decision.** VARIANT, selected by one question at adoption: *is every
turn paced by a human, or does the loop run autonomously?* The deeper
teaching is REWRITTEN, not retired: **capability concentrates at the
DIRECTION ROLE, not at the resident session.** The two coincide only in a
human-paced loop. In an autonomous loop the resident wakes dozens of times a
day and re-reads its whole context each wake, so a top-model resident buys
routing at judgment prices; direction moves to an on-demand top-model agent,
and escalation to it is MECHANICAL, never discretionary — because the known
failure mode of a cheaper resident is under-escalation: it does not know
what it does not know. The escalation kit (trigger list, spawn log, cadence
gate, watchdog dailies) is REQUIRED in the autonomous variant and the
trigger LIST alone is retained as guidance in the human-paced variant, where
the human is the enforcement.

**The evidence it rests on.**
- Observed in LEDGER today (reported by the resident, accepted by Jafar; not
  a printed series — say so where cited): an autonomous resident wakes ~25x/
  day on watchdogs, builder completions and build watchers, re-reading the
  conversation each wake. This is the cost that broke "resident = Fable";
  it does not exist in a human-paced loop, so the original argument stands
  there untouched.
- The framework this template borrowed packaging from never puts a director
  in the resident session at all — its directors are on-demand top-tier
  subagents and its resident is a router — and it works because a human
  paces it. Jafar's objection ("theirs is human in the loop, ours is
  autonomous") is precisely the selector this decision keys on.
- LEDGER already runs the hybrid live: mandatory triggers, a SubagentStart
  spawn log (`.claude/agent-log.tsv`), a `director_cadence` verify check,
  an hourly watchdog dailies check. The template ships what a real project
  runs, which is this template's provenance rule.
- The `100 changed lines` and `12h` thresholds are inherited from LEDGER
  and NOT yet validated by a printed series (the cadence check is being
  built today). Ship them as defaults explicitly marked unvalidated, with
  the instruction to print the series and reset them from evidence (rule 2).

**What it rules out.**
- *Full replacement* (autonomous-only teaching): sacrifices the human-paced
  case, where an on-demand-only director adds hop latency and a router
  resident adds nothing — the cost argument that justifies the hybrid is
  absent there.
- *Keeping "resident = top model" unconditionally*: refuted by today's
  measured-in-practice cost in LEDGER and by the owner's direct correction.
- *Hybrid with discretionary escalation*: ruled out hardest. A judgment-
  based "escalate when it matters" rule asks the cheaper model to know what
  it does not know, and this file's whole lineage is rules that decayed
  without a trigger point.

**What would reopen it.**
- `.claude/agent-log.tsv` in an adopting autonomous project shows near-zero
  director rows over a working week despite commits flowing — the triggers
  are not firing and Jafar's condition ("never called upon") is being
  violated; the kit, not the variant, gets redesigned.
- A wrong direction is pursued autonomously for hours DESPITE the triggers
  firing — the safeguard itself failed; reopen the whole variant question.
- Model pricing/caching changes make a top-model resident's ~25-wake day
  cost comparable to Opus — the cost leg of the argument lapses.

**Where it is enforced.** In the template's own files, as follows. This is
the builder's work order; no judgement required.

---

## Builder work order (file by file)

### 1. README.md
- In the tier diagram, change `Tier 1 — Direction (model: fable)` to
  `Tier 1 — Direction (model: fable — on-demand)` and add directly under
  the diagram a two-line "Resident session" note: **human-paced loop →
  the resident IS the director (top model); autonomous loop → the resident
  is an opus coordinator and the director is spawned on mandatory
  triggers.** Point to CLAUDE.md's "The studio split" section for the
  selector.
- Rewrite the "Why capability concentrates at the top" paragraph (lines
  57–63) to say: capability concentrates at the DIRECTION ROLE and at
  verification; whether the direction role lives in the resident session
  depends on who paces the loop. Keep the existing
  claims/accusations reasoning verbatim — it survives unchanged. Add one
  sentence: an autonomous resident is a coordinator, and its escalation to
  the director is mechanical because under-escalation is invisible to the
  session doing it.

### 2. CLAUDE.md (template)
Add a new section between "Project mechanics" and "The working loop",
titled `## The studio split — choose the variant`, containing:
- The selector question and a `{{VARIANT: human-paced | autonomous}}` fill
  mark, with instruction that `tools/verify.py` fails until it is declared
  (see item 6).
- **Human-paced variant** (3–4 lines): resident is the director on the top
  model; tier-2/3 as shipped; the trigger list below still names the
  moments that ARE direction moments — the human enforces them.
- **Autonomous variant**: resident is an opus coordinator that decides
  nothing binding; the studio-director agent is spawned MANDATORILY on
  these triggers (copy this list exactly):
  1. builder-batch review before any commit of builder work
  2. queue reordering or refill
  3. a landing that changes a conclusion
  4. verifier-vs-builder disagreement
  5. close-outs (the quality-ladder question)
  6. anything touching the premise, the roadmap, or CLAUDE.md
- State the three mechanical enforcements: every spawn logged to a tracked
  `.claude/agent-log.tsv` by a SubagentStart hook; `director_cadence` in
  verify goes RED — blocking the commit — when more than {{100}} changed
  lines under the code tree have no director row newer than HEAD; the
  watchdog's dailies check force-spawns a director review if none in
  {{12h}}. Mark both numbers "inherited from the extracted project,
  unvalidated — print your own series before trusting them" (rule 2).

  > **CORRECTION, 2026-08-25 — the words "no director row newer than HEAD"
  > above are now FALSE.** They are left standing because this file is the
  > decision record and rewriting its history would destroy the thing it is
  > for; they are quoted here so the claim cannot be re-derived as truth by
  > the next reader, who will find it as plausible as its author did. The
  > reference is **the last commit that TOUCHED CODE**, not HEAD: comparing
  > against HEAD let a docs commit — or CI committing its own evidence back
  > into the repository — invalidate a review that was still valid, which
  > fired three times in one night and forced a fresh top-tier spawn each
  > time. The living text is CLAUDE.md "The studio split" and
  > `tools/verify.d/director_cadence.py`, as this file's own status block
  > already says.
- One line of rationale with Jafar's condition quoted: mechanical, not
  discretionary, because "no point in having a fable director if it's
  never called upon."
- State explicitly: the coordinator's charter lives HERE, not in a new
  agent file — the resident is the main session, not a subagent. Do NOT
  create a coordinator agent file.

### 3. .claude/agents/studio-director.md
- Keep `model: fable`. In the `description:`, add that in an autonomous
  loop this agent is spawned on the mandatory triggers listed in CLAUDE.md
  ("The studio split"), and in a human-paced loop its charter is the
  resident's own.
- In the body, add a short section `## When you are invoked (autonomous
  loop)` listing the six triggers verbatim, and one line: your output for
  anything binding is a decision record in the shape of
  `templates/decision.md`, written where the next session will read it.

### 4. docs/adopting.md
- Add a procedure step (between current steps 1 and 2): **"Choose the
  variant"** — the selector question, what each answer sets (`VARIANT`
  declaration; autonomous additionally wires the escalation kit), and the
  warning that the failure mode of skipping this is a director that exists
  and is never called.
- In the component table, add a row: `escalation kit (agent-log hook,
  director_cadence, dailies)` | "if the project has its own, keep it" |
  "REQUIRED for autonomous, not copied for human-paced".
- Extend step 5 (both-ways tests): the cadence gate must ACCEPT a commit
  with a fresh director row and BLOCK one with >threshold changed lines
  and a stale log — both cases actually run, per rule 5b.

### 5. .claude/hooks/agent-log.sh (new)
- SubagentStart hook appending `ISO-timestamp<TAB>agent-name<TAB>model` to
  `.claude/agent-log.tsv` (tracked file; create with a header row). Wire
  into `.claude/settings.json`. Add its accepting and rejecting cases to
  `selftest.sh` (log line appended; malformed input does not corrupt the
  tsv).

### 6. tools/ verify skeleton
- New pluggable check `director_cadence`: reads the `VARIANT` declaration
  (grep CLAUDE.md's studio-split fill mark, or a `.claude/studio.conf` —
  builder picks one and documents it in the check's header).
  - Undeclared → RED with the message "studio variant not declared —
    choose in CLAUDE.md 'The studio split'". This is what forces the
    choice at adoption.
  - human-paced → PASS, printing the words "cadence: not enforced
    (human-paced variant)" — never a bare pass (rule 3b: a skip must be
    legible as a skip, not an absence).
  - autonomous → count changed lines under the code tree since the newest
    `studio-director` row in `.claude/agent-log.tsv`; RED over the
    threshold (default 100, marked unvalidated). Print the count and the
    row's age even when green — the denominator ships with every zero.
- Selftest per rule 5b, accepting case first: green with fresh row; red
  with stale log; red with undeclared variant; green human-paced prints
  its skip line.
- The watchdog dailies force-spawn cannot ship as portable code (trigger
  systems differ per environment); document it in CLAUDE.md's autonomous
  variant (item 2) as required wiring, citing LEDGER's hourly watchdog as
  the precedent implementation.

### Out of scope for the builder
- No changes to tier-2/tier-3 agent files, skills, or rules — the split
  below the direction role is untouched by this decision.
- No new coordinator agent file (stated above; repeated because it is the
  likeliest wrong inference).

---

## Post-implementation record — studio-director, 2026-08-24

**Review verdict on the builder batch: COMMIT WITH the named fixes below.**
The implementation matches this spec item for item; the forcing mechanism
was verified in the code, not the report (undeclared → RED naming the fix;
human-paced → the literal words "cadence: not enforced (human-paced
variant)"; the un-instantiated template is a legible skip that arms when
`{{PROJECT_NAME}}` is filled — a state this spec did not anticipate and the
builder was right to add, or the template's own verify would be permanently
red). Thresholds shipped marked `inherited-unvalidated` in the check, in
CLAUDE.md, and in the RED message itself, with `--series` as the
instruction. The builder's live-instantiation find (`git status
--porcelain` collapsing a new untracked directory to one path, so a
300-line new module counted as 0 changed lines) is rule-5b discipline done
properly — fixtures passed, the live accepting case found the hole, the
hole became a fixture — and it raises confidence in the rest of the
validation record accordingly.

**Named fix 1 — the threshold has two homes and nothing ties them.**
CLAUDE.md presents `{{100}}` and `{{12h}}` as fill marks; the enforced
number is `MAX_UNREVIEWED_LINES = 100` in
`tools/verify.d/director_cadence.py`. An adopter who fills the prose mark
with their measured number changes nothing — the gate keeps enforcing 100,
silently except for the threshold printed in verify output. One idea, two
implementations (rule 1, third corollary). Fix: CLAUDE.md's enforcement
bullet states where the number LIVES (the constant, by name and path) and
that the prose mirrors it; do not make the check parse prose.

**Named fix 2 — decision on referred question 2 (skills vs triggers).**
A trigger-declaration-and-routing mechanism for skills is over-engineering
for a four-skill template and is REJECTED. But the hole is real and the
batch's own central claim ("spawned MANDATORILY... mechanical, not
discretionary") is falsified at ship time by sibling files: in the
autonomous variant, `/close` step 2 performs trigger 5 (the quality-ladder
question) and `/land` step 4 performs trigger 3 (a landing that changes a
conclusion) with no director spawn. The fix is three one-liners, no
machinery:
- CLAUDE.md, autonomous variant, one sentence: *the triggers bind
  regardless of the doorway — a skill step that performs a trigger act is
  a director spawn in the autonomous variant, not an exemption from one.*
- `.claude/skills/close/SKILL.md`, step 2, one line: in the autonomous
  variant this question is the director's call (trigger 5) — spawn
  `studio-director`; human-paced, the resident holds the charter.
- `.claude/skills/land/SKILL.md`, step 4, one line: where a finding
  changes a conclusion, that is trigger 3 in the autonomous variant —
  the routing decision is the director's.
(`/start` runs with the owner present — human-paced by construction — and
`/dispatch` performs no direction act; neither needs a line.)

**Decision on referred question 1:** this file's condition ("implemented
and the both-ways tests have run") is met; status flipped to LOG above.
The dailies force-spawn shipping as documented wiring rather than portable
code is what this spec itself ordered, and the unvalidated thresholds are
unvalidated BY DESIGN, for the adopter's series to settle — neither keeps
this SPEC.

**Known looseness, recorded not fixed:** "fresh" is `director row newer
than HEAD`, so a director spawned after HEAD for an unrelated trigger
(e.g. a queue reorder) lets a subsequent builder batch pass without its
own review until the next commit advances HEAD. Acceptable for a template
default — the census printed on every green run makes it visible — and the
log gives any adopter the series to tighten it from if it ever bites.
