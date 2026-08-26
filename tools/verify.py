#!/usr/bin/env python3
"""The one command before every commit. Green writes tools/.verify-footer;
red DELETES it — so a red run has nothing to paste into a commit message,
which is the point: the footer exists because its ancestor project pasted
unmeasured claims into commits three times, and a warning printed after the
message was written could not reach a decision already made.

    python3 tools/verify.py            # run everything
    python3 tools/verify.py --list     # show the registered checks

Add checks in tools/verify.d/*.py — each module defines
    def check() -> tuple[bool, str]
returning (green, one-line summary). Modules run in filename order, ALL of
them even after a failure (a commit should learn everything red at once,
not one thing per attempt). The summary line goes into the footer verbatim,
so make it carry numbers with denominators: "lint ok (0 errors, 214 files
walked)" — never a bare "ok", which cannot tell clean from never-ran.

The starter checks below are the floor, not the ceiling. The extracted
project's verify grew to ~40 checks; each one was added the day its absence
cost something, which is the right schedule for growing this file.
"""
import importlib.util
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
FOOTER = pathlib.Path(__file__).resolve().parent / ".verify-footer"
CHECK_DIR = pathlib.Path(__file__).resolve().parent / "verify.d"


def builtin_checks():
    """Checks every project gets before wiring anything of its own."""

    def hooks_selftest():
        st = ROOT / ".claude" / "hooks" / "selftest.sh"
        if not st.exists():
            return False, "hooks selftest MISSING (.claude/hooks/selftest.sh)"
        r = subprocess.run(["bash", str(st)], capture_output=True, text=True,
                           cwd=ROOT)
        tail = (r.stdout.strip().splitlines() or ["no output"])[-1]
        return r.returncode == 0, "hooks: " + tail

    def docs_marked():
        """Every doc in docs-dirs declares LIVE / SPEC / LOG near the top.

        A doc that does not say what it is gets read as current when it is
        history; the ancestor project audited a 1,500-line chronology by
        stamping a status banner on top, certifying the mess.
        """
        dirs = [d for d in (ROOT / "docs",) if d.exists()]
        seen, bad = 0, []
        for d in dirs:
            for f in d.rglob("*.md"):
                seen += 1
                head = f.read_text(encoding="utf-8", errors="replace")[:400]
                if not any(k in head for k in ("LIVE", "SPEC", "LOG")):
                    bad.append(str(f.relative_to(ROOT)))
        if bad:
            return False, f"docs: {len(bad)} of {seen} unmarked ({bad[0]}...)"
        return True, f"docs marked ({seen} checked)"

    def queue_startable():
        """The queue holds startable work — running thin is reported before
        it costs an idle hour, not noticed after."""
        q = ROOT / "queue.md"
        if not q.exists():
            return True, "no queue.md (fine for a library; a project wants one)"
        body = q.read_text(encoding="utf-8", errors="replace")
        now = body.split("## Now", 1)[-1].split("## Standing", 1)[0]
        items = [l for l in now.splitlines() if l.startswith("1. ")]
        ok = len(items) >= 1 and "## Standing" in body
        return ok, (f"queue: {len(items)} startable item(s), standing section "
                    f"{'present' if '## Standing' in body else 'MISSING'}")

    def studio_overhead():
        """What share of the day's agent spawns BUILT THE PRODUCT.

        READING ONLY, NEVER RED. There is no landed series to set a bound
        from, and a threshold invented here would be the move rule 2
        forbids. What this is for is a person seeing the number at all: the
        ancestor project ran 110 spawns in a day, 78 of them the project
        working on itself, and nobody could see the proportion because the
        log recorded WHICH AGENT and never WHICH KIND OF WORK.

        THE SET IS LITERAL AND LIVES IN `.claude/agent-roles`, one name per
        line, because no naming convention carries this: an agent called
        `instrument-builder` is a builder by name and overhead by purpose.
        A name in neither list counts as OVERHEAD — an unrecognised agent is
        not evidence that the product got built, and defaulting the other
        way would flatter every roster change.

        It is a COUNT over the newest UTC day PRESENT IN THE LOG, with the
        date carried in the value, so a log that went quiet yesterday cannot
        read as today's spend. Every zero ships its denominator, and a
        missing log prints the words rather than a clean-looking zero.
        """
        log = ROOT / ".claude" / "agent-log.tsv"
        roles = ROOT / ".claude" / "agent-roles"
        if not log.exists():
            return True, "studio overhead: nothing-measured (no agent log)"
        building = set()
        if roles.exists():
            building = {l.strip() for l in roles.read_text(encoding="utf-8").splitlines()
                        if l.strip() and not l.startswith("#")}
        by_day = {}
        # TWO COUNTERS, AND THEY MUST BE ABLE TO DISAGREE. The first version
        # of this incremented `rows` only AFTER the dateable test, so the
        # message read "0 dateable row(s) of 0" — a denominator describing
        # the set that survived the filter, which can never disagree with
        # the numerator and therefore measures nothing. §3b, in code written
        # for §3b, ten minutes after writing it. `offered` is every row the
        # file holds; `dateable` is what the window could actually use.
        offered = dateable = 0
        for line in log.read_text(encoding="utf-8", errors="replace").splitlines()[1:]:
            if not line.strip():
                continue
            offered += 1
            parts = line.split("\t")
            if len(parts) < 2 or "T" not in parts[0]:
                continue
            dateable += 1
            day = parts[0].split("T")[0]
            built, total = by_day.get(day, (0, 0))
            by_day[day] = (built + (1 if parts[1].strip() in building else 0), total + 1)
        if not by_day:
            return True, (f"studio overhead: nothing-measured — 0 of {offered} "
                          f"log row(s) carry a date, so no day window could be "
                          f"built (the log is there and unreadable, which is not "
                          f"the same fact as an empty log)")
        day = max(by_day)
        built, total = by_day[day]
        if not building:
            return True, (f"studio overhead: NOT MEASURED — {total} spawn(s) on "
                          f"{day}, but .claude/agent-roles is missing, so no "
                          f"agent can be counted as building the product")
        skipped = offered - dateable
        note = f", {skipped} undateable row(s) counted in no window" if skipped else ""
        return True, (f"studio overhead: gameShareDay={built}/{total}@{day} — "
                      f"COUNT of product-building spawns over all spawns on the "
                      f"newest day in the log, of {offered} row(s) read{note}; "
                      f"reading only, not gated")

    return [("hooks_selftest", hooks_selftest),
            ("docs_marked", docs_marked),
            ("queue_startable", queue_startable),
            ("studio_overhead", studio_overhead)]


def plugin_checks():
    out = []
    if not CHECK_DIR.exists():
        return out
    for f in sorted(CHECK_DIR.glob("*.py")):
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            out.append((f.stem, mod.check))
        except Exception as e:  # a broken check is a red check, never a skip
            out.append((f.stem, lambda e=e, n=f.stem: (False, f"{n}: BROKEN CHECK ({e})")))
    return out


def main():
    checks = builtin_checks() + plugin_checks()
    if "--list" in sys.argv:
        for name, _ in checks:
            print(name)
        return 0

    results, green = [], True
    for name, fn in checks:
        try:
            ok, line = fn()
        except Exception as e:
            ok, line = False, f"{name}: CRASHED ({e})"
        results.append((ok, line))
        green &= ok
        print(("  ok   " if ok else "  FAIL ") + line)

    if green:
        stamp = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())
        FOOTER.write_text(", ".join(l for _, l in results)
                          + f"\n(verified {stamp})\n", encoding="utf-8")
        print(f"\n--- footer written to {FOOTER.relative_to(ROOT)} — "
              "paste it into the commit with -F ---")
        return 0
    FOOTER.unlink(missing_ok=True)
    print("\nNOT GREEN — the footer has been deleted; there is nothing to paste.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
