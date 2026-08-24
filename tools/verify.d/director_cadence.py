#!/usr/bin/env python3
"""director_cadence — is the direction role actually being called upon?

A pluggable check for tools/verify.py (contract: `check() -> (bool, str)`).
It is the mechanical half of CLAUDE.md's "The studio split": in an
autonomous loop the escalation to the director is MANDATORY, and the owner's
condition on that arrangement was "no point in having a fable director if
it's never called upon." A trigger list is a rule, and this file is mostly a
list of rules that decayed without a trigger point — so the list ships with
a gate that blocks the commit when nobody escalated.

    python3 tools/verify.d/director_cadence.py            # run the check
    python3 tools/verify.d/director_cadence.py --series   # set the threshold
    python3 tools/verify.d/director_cadence.py --selftest # both ways, rule 5b

WHERE THE VARIANT IS READ, and why here rather than a .claude/studio.conf:
CLAUDE.md, the "The studio split" section, a line reading

    VARIANT: autonomous          (or: VARIANT: human-paced)

The choice is between the file every session already reads and a second
config file nobody opens. A declaration that sits beside the paragraph
explaining it can be checked against that paragraph; one in a conf file is a
claim living away from its reasoning, which is the decay this template
exists to prevent. Cost of the choice: adoption must add the section to the
PROJECT's own CLAUDE.md (adopting.md keeps the project's), which is exactly
the forcing function the RED-until-declared rule wants.

THE TWO NUMBERS BELOW ARE INHERITED, NOT MEASURED — see MAX_UNREVIEWED_LINES.
"""
import calendar
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

# INHERITED FROM THE EXTRACTED PROJECT (LEDGER), UNVALIDATED. 100 is the
# batch size at which that project's director review started catching things,
# reported by its resident and never printed as a series — so it is a
# starting point, not evidence (rule 2: never set a threshold you have not
# measured). Run `--series` on your own history, look at the distribution of
# commit sizes, and set this from it. The companion 12h dailies interval
# lives in CLAUDE.md's autonomous variant and carries the same warning.
MAX_UNREVIEWED_LINES = 100
THRESHOLD_PROVENANCE = "inherited-unvalidated"

# WHAT COUNTS AS "THE CODE TREE". Documentation is excluded because trigger 6
# ("anything touching the premise, the roadmap, or CLAUDE.md") already routes
# every doc change to the director by name — counting them here would gate
# the same change twice and let a large mechanical doc edit consume the
# budget a code batch needs. The log itself is excluded because the hook's
# own rows would inflate the number they are measured against.
DOC_SUFFIXES = (".md", ".txt", ".rst")
EXCLUDE_PATHS = (".claude/agent-log.tsv",)

DIRECTOR_AGENT = "studio-director"
LOG_REL = ".claude/agent-log.tsv"
VARIANTS = ("human-paced", "autonomous")


def _git(root, *args):
    """(rc, stdout). A git that cannot answer is a red check, never a skip —
    an instrument that could not measure must not report green (rule 3b)."""
    r = subprocess.run(["git", *args], cwd=str(root), capture_output=True,
                       text=True)
    return r.returncode, r.stdout


def read_variant(root):
    """(variant | None, note). None means undeclared; note says which of the
    two undeclared states it is, because 'no CLAUDE.md' and 'CLAUDE.md with
    the fill mark still in it' need different fixes."""
    md = root / "CLAUDE.md"
    if not md.exists():
        return None, "no CLAUDE.md at the repo root"
    body = md.read_text(encoding="utf-8", errors="replace")
    for line in body.splitlines():
        s = line.strip().lstrip("*-> ").strip()
        if not s.lower().startswith("variant:") or "{{" in s:
            continue
        val = s.split(":", 1)[1].strip().strip("`*_ ")
        if val in VARIANTS:
            return val, "declared in CLAUDE.md"
    return None, "the fill mark is still unfilled"


def uninstantiated_marks(root):
    """The template ships with fill marks; a project fills them. Returns the
    count of remaining `{{...}}` marks, and whether PROJECT_NAME is one.

    This is what tells the un-instantiated TEMPLATE apart from an adopting
    project that skipped the variant question — the two would otherwise both
    read as 'undeclared', and only one of them is a fault. Quickstart step 2
    fills PROJECT_NAME first, so the gate arms on the first adoption action.
    """
    md = root / "CLAUDE.md"
    if not md.exists():
        return 0, False
    body = md.read_text(encoding="utf-8", errors="replace")
    return body.count("{{"), "{{PROJECT_NAME}}" in body


def changed_code_lines(root):
    """(lines, code_files, seen_files) for the working tree against HEAD.

    Working tree, not history: this check runs inside verify.py, i.e. before
    the commit, so the batch it must judge is the uncommitted one. Untracked
    files count — a brand-new 400-line module is 400 changed lines whether or
    not it has been `git add`ed yet.

    `seen_files` is the denominator: "0 changed lines" and "the walker never
    entered a file" print identically without it (rule 3b).
    """
    rc, out = _git(root, "diff", "HEAD", "--numstat")
    if rc != 0:
        rc, out = _git(root, "diff", "--numstat")  # no HEAD yet (empty repo)
        if rc != 0:
            return None, 0, 0
    lines, code, seen = 0, 0, 0
    for row in out.splitlines():
        parts = row.split("\t")
        if len(parts) < 3:
            continue
        seen += 1
        add, dele, path = parts[0], parts[1], parts[-1]
        if not _is_code(path):
            continue
        code += 1
        # "-\t-\tpath" is git's binary marker: the file changed but has no
        # line count. Counted as a file, contributing 0 lines, and said so
        # here so a binary-only batch cannot read as "nothing changed".
        lines += sum(int(v) for v in (add, dele) if v.isdigit())
    # -uall EXPANDS UNTRACKED DIRECTORIES INTO FILES, and it is load-bearing:
    # plain --porcelain reports a brand-new directory as the single path
    # "src/", which is not a file, so a 300-line new module — the commonest
    # shape of a builder batch — measured as 0 changed lines and sailed
    # through this gate. Found by running the check on a real instantiation
    # after the fixtures (which edited a tracked file) had all passed.
    rc, out = _git(root, "status", "--porcelain", "-uall")
    if rc == 0:
        for row in out.splitlines():
            if not row.startswith("??"):
                continue
            path = row[3:]
            seen += 1
            if not _is_code(path):
                continue
            f = root / path
            if not f.is_file():
                continue
            code += 1
            try:
                lines += len(f.read_text(encoding="utf-8",
                                         errors="replace").splitlines())
            except OSError:
                pass
    return lines, code, seen


def _is_code(path):
    if path in EXCLUDE_PATHS:
        return False
    return not path.lower().endswith(DOC_SUFFIXES)


def newest_director_row(root):
    """(epoch | None, director_rows, total_rows). The denominator is the
    total row count so "no director was spawned" cannot be confused with
    "the hook never wrote anything" — the second is an instrument fault and
    the first is the thing this check exists to catch."""
    log = root / LOG_REL
    if not log.exists():
        return None, 0, 0
    newest, director, total = None, 0, 0
    for row in log.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = row.split("\t")
        if len(parts) < 2 or parts[0] == "when":
            continue
        total += 1
        if parts[1].strip() != DIRECTOR_AGENT:
            continue
        director += 1
        try:
            t = time.strptime(parts[0].strip(), "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            continue  # a row this check cannot read is not a review it saw
        epoch = calendar.timegm(t)
        newest = epoch if newest is None else max(newest, epoch)
    return newest, director, total


def head_epoch(root):
    rc, out = _git(root, "log", "-1", "--format=%ct")
    if rc != 0 or not out.strip().isdigit():
        return None
    return int(out.strip())


def _age(seconds):
    if seconds is None:
        return "never"
    h, m = divmod(max(0, int(seconds)) // 60, 60)
    return f"{h}h{m:02d}m"


def _n(count, word):
    return f"{count} {word}" + ("" if count == 1 else "s")


def check(root=ROOT):
    root = pathlib.Path(root)
    variant, note = read_variant(root)

    marks, has_project_name = uninstantiated_marks(root)
    if variant is None and has_project_name:
        # Not a project yet — the un-instantiated template itself. Legible as
        # a skip rather than as a pass (rule 3b), and it names the exact edit
        # that arms the gate.
        return True, (f"cadence: not armed — template not instantiated "
                      f"({marks} unfilled {{{{...}}}} marks incl. PROJECT_NAME); "
                      f"the gate arms when CLAUDE.md is filled in")

    if variant is None:
        return False, ("studio variant not declared — choose in CLAUDE.md "
                       f"'The studio split' ({note}; expected a line "
                       f"'VARIANT: {' | '.join(VARIANTS)}')")

    if variant == "human-paced":
        return True, ("cadence: not enforced (human-paced variant) — the "
                      "human paces the loop and enforces the trigger list; "
                      "0 of 0 batches gated, by design")

    lines, code_files, seen = changed_code_lines(root)
    if lines is None:
        return False, ("director_cadence: cannot read the diff (not a git "
                       "checkout?) — an instrument that cannot measure does "
                       "not get to report green")

    newest, director_rows, total_rows = newest_director_row(root)
    head = head_epoch(root)
    now = int(time.time())
    fresh = (newest is not None and head is not None and newest > head)
    head_age = _age(None if head is None else now - head)
    row_age = ("no such row ever" if newest is None
               else f"newest {_age(now - newest)} old")
    census = (f"{director_rows} of {total_rows} log rows are "
              f"{DIRECTOR_AGENT} ({row_age}), HEAD {head_age} old")

    if lines > MAX_UNREVIEWED_LINES and not fresh:
        return False, (f"director_cadence RED: {lines} changed lines in "
                       f"{_n(code_files, 'code file')} ({seen} paths seen) "
                       f"with no {DIRECTOR_AGENT} row newer than HEAD — "
                       f"{census}; "
                       f"threshold {MAX_UNREVIEWED_LINES} "
                       f"({THRESHOLD_PROVENANCE}). Spawn the director for the "
                       f"batch review, or run --series and set the threshold "
                       f"from your own evidence")

    why = "reviewed" if fresh else f"under threshold {MAX_UNREVIEWED_LINES}"
    return True, (f"cadence ok ({why}): {lines} changed lines in "
                  f"{_n(code_files, 'code file')} ({seen} paths seen), "
                  f"threshold {MAX_UNREVIEWED_LINES} ({THRESHOLD_PROVENANCE}); "
                  f"{census}")


# ---------------------------------------------------------------- series ---

def series(root=ROOT, count=50):
    """Print the per-commit changed-line series, newest first, then the
    summaries — the raw row ABOVE both, on purpose: a human sees a regime
    change in the row in one second and no aggregate can see it at all.

    IT IS A PROXY, AND SAY SO WHEN YOU USE IT. The gate measures UNCOMMITTED
    lines since the last director row; this measures LANDED commit sizes.
    They coincide when each reviewed batch lands as one commit, which is the
    flow the gate assumes. If your project commits in fragments, the series
    reads low and the threshold set from it will be tight.
    """
    root = pathlib.Path(root)
    rc, out = _git(root, "log", f"-{count}", "--numstat",
                   "--format=%x01%H %ct")
    if rc != 0:
        print("no git history to read — nothing measured")
        return 1
    vals, cur = [], None
    for row in out.splitlines():
        if row.startswith("\x01"):
            if cur is not None:
                vals.append(cur)
            cur = 0
            continue
        parts = row.split("\t")
        if len(parts) < 3 or cur is None:
            continue
        if not _is_code(parts[-1]):
            continue
        cur += sum(int(v) for v in parts[:2] if v.isdigit())
    if cur is not None:
        vals.append(cur)
    if not vals:
        print(f"director_cadence --series: 0 commits examined "
              f"(asked for {count}) — nothing measured")
        return 1
    print(f"changed code lines per commit, newest first ({len(vals)} of "
          f"{count} requested commits had history):")
    print("  " + " ".join(str(v) for v in vals))
    s = sorted(vals)
    med = s[len(s) // 2] if len(s) % 2 else (s[len(s) // 2 - 1]
                                             + s[len(s) // 2]) / 2
    over = sum(1 for v in vals if v > MAX_UNREVIEWED_LINES)
    print(f"  median {med}  peak {s[-1]}  min {s[0]}  n={len(vals)}")
    print(f"  over the current threshold {MAX_UNREVIEWED_LINES} "
          f"({THRESHOLD_PROVENANCE}): {over} of {len(vals)} commits")
    print("  a median answers 'is this normal', the peak answers 'did it "
          "ever' — set the bound from the row, not from either summary")
    return 0


# -------------------------------------------------------------- selftest ---

def _fixture(tmp, variant_line, changed_lines, row_age_hours,
             director_rows=True, project_name="Toy"):
    """Build a throwaway repo. HEAD is committed two hours in the past so a
    'fresh' row (now) and a 'stale' row (5h ago) sit either side of it
    unambiguously — a fixture whose fresh case is only fresh by a second
    tests the clock, not the check."""
    import os
    tmp.mkdir(parents=True, exist_ok=True)
    (tmp / ".claude").mkdir(exist_ok=True)
    (tmp / "src").mkdir(exist_ok=True)
    (tmp / "CLAUDE.md").write_text(
        f"# CLAUDE.md — how to work on {project_name}\n\n"
        "## The studio split — choose the variant\n\n"
        f"{variant_line}\n", encoding="utf-8")
    (tmp / "src" / "mod.py").write_text("# base\n", encoding="utf-8")
    env = dict(os.environ)
    past = time.strftime("%Y-%m-%dT%H:%M:%S+0000",
                         time.gmtime(time.time() - 2 * 3600))
    env.update(GIT_AUTHOR_DATE=past, GIT_COMMITTER_DATE=past,
               GIT_AUTHOR_NAME="t", GIT_COMMITTER_NAME="t",
               GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_EMAIL="t@t")
    for args in (["init", "-q", "-b", "main"], ["add", "-A"],
                 ["commit", "-q", "-m", "base"]):
        subprocess.run(["git", *args], cwd=str(tmp), env=env,
                       capture_output=True, text=True)
    if director_rows is not None:
        rows = "when\tagent\tmodel\n"
        if director_rows:
            when = time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                 time.gmtime(time.time() - row_age_hours * 3600))
            rows += f"{when}\tstudio-director\tfable\n"
        rows += "2000-01-01T00:00:00Z\tsystems-builder\topus\n"
        (tmp / ".claude" / "agent-log.tsv").write_text(rows, encoding="utf-8")
    if changed_lines:
        (tmp / "src" / "mod.py").write_text(
            "\n".join(f"x = {i}" for i in range(changed_lines)) + "\n",
            encoding="utf-8")
    return tmp


def selftest():
    """Rule 5b: a guard has two outcomes and shipping it means having watched
    BOTH — accepting case FIRST, because the expensive failure is a validator
    nothing survives and it reports as 'nothing happened'."""
    import tempfile
    passed = failed = 0
    # The fixture rewrites a 1-line base file with BIG lines, and git's
    # numstat counts the deleted base line as well as the additions — so the
    # number the check prints is BIG+1. Written out rather than pasted as a
    # literal, because a magic 401 in an assertion is the kind of constant
    # that gets "fixed" to match a future fixture instead of understood.
    BIG = 400
    BIG_DIFF = BIG + 1

    def say(ok, what, detail=""):
        nonlocal passed, failed
        if ok:
            passed += 1
            print(f"  ok   {what}")
        else:
            failed += 1
            print(f"  FAIL {what} :: {detail}")

    base = pathlib.Path(tempfile.mkdtemp())
    try:
        # --- ACCEPTING CASES FIRST -------------------------------------
        r = _fixture(base / "a", "VARIANT: autonomous", BIG, 0)
        ok, msg = check(r)
        say(ok, "big batch WITH a fresh director row is accepted", msg)
        say(f"{BIG_DIFF} changed lines" in msg and "newest 0h" in msg,
            "the accepting message prints the count and the row age", msg)

        r = _fixture(base / "b", "VARIANT: autonomous", 0, 5)
        ok, msg = check(r)
        say(ok, "small batch with a stale log is accepted (not a ratchet)",
            msg)
        say("0 changed lines" in msg and "log rows" in msg,
            "a zero ships its denominator", msg)

        r = _fixture(base / "c", "VARIANT: human-paced", BIG, 5)
        ok, msg = check(r)
        say(ok and "cadence: not enforced (human-paced variant)" in msg,
            "human-paced passes and says it is a SKIP, not a bare green", msg)

        r = _fixture(base / "d", "{{VARIANT: human-paced | autonomous}}",
                     BIG, 5, project_name="{{PROJECT_NAME}}")
        ok, msg = check(r)
        say(ok and "PROJECT_NAME" in msg,
            "the un-instantiated template is a legible skip, not a failure",
            msg)

        # --- REJECTING CASES -------------------------------------------
        r = _fixture(base / "e", "VARIANT: autonomous", BIG, 5)
        ok, msg = check(r)
        say(not ok and f"{BIG_DIFF} changed lines" in msg,
            "big batch with a STALE log is blocked, naming the count", msg)

        # A NEW UNTRACKED DIRECTORY, which every case above missed: `git
        # status --porcelain` collapses one to a single non-file path, and
        # this shape — a whole new module dropped in by a builder — read as
        # 0 changed lines until it was run against a real instantiation.
        r = _fixture(base / "i", "VARIANT: autonomous", 0, 5)
        (r / "newmod").mkdir()
        (r / "newmod" / "a.py").write_text(
            "\n".join(f"y = {i}" for i in range(BIG)) + "\n", encoding="utf-8")
        ok, msg = check(r)
        say(not ok and f"{BIG} changed lines" in msg,
            "a brand-new untracked DIRECTORY is counted, not skipped", msg)

        r = _fixture(base / "f", "{{VARIANT: human-paced | autonomous}}",
                     BIG, 5)
        ok, msg = check(r)
        say(not ok and "studio variant not declared" in msg,
            "an instantiated project with no variant is blocked", msg)

        r = _fixture(base / "g", "VARIANT: autonomous", BIG, 5,
                     director_rows=None)
        ok, msg = check(r)
        say(not ok and "0 of 0 log rows" in msg,
            "no agent log at all is blocked and says 0 of 0", msg)

        r = _fixture(base / "h", "VARIANT: autonomous", BIG, 5)
        (r / "CLAUDE.md").unlink()
        ok, msg = check(r)
        say(not ok and "no CLAUDE.md" in msg,
            "a missing CLAUDE.md is blocked, not skipped", msg)
    finally:
        subprocess.run(["rm", "-rf", str(base)], capture_output=True)

    print(f"director_cadence selftest: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--series" in sys.argv:
        n = [a for a in sys.argv[1:] if a.isdigit()]
        sys.exit(series(count=int(n[0]) if n else 50))
    green, line = check()
    print(("  ok   " if green else "  FAIL ") + line)
    sys.exit(0 if green else 1)
