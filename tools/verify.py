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
        """Every document declares LIVE / SPEC / LOG near the top.

        A doc that does not say what it is gets read as current when it is
        history; the ancestor project audited a 1,500-line chronology by
        stamping a status banner on top, certifying the mess.

        WALK THE WHOLE REPO, AND PRINT BOTH NUMBERS. The ancestor's first
        version globbed one directory level and had never looked at fifteen
        files; this one's first version scanned only `docs/` and reported
        "2 checked" in a repo shipping twenty markdown files. Both failures
        are the same one: a denominator that does not move when a document
        is added somewhere new. So the walk is a repo-wide rglob and the
        SKIPS are a named list below rather than a directory list above —
        an exclusion nobody is told about is indistinguishable from a file
        nobody looked at, which is rule 3b wearing a filter's clothes.

        The summary therefore carries three counts: examined, excluded by
        DECISION (with the reason and the per-reason count), and not walked
        at all. Adding a `design/` or `notes/` directory moves the first
        number without anyone editing this function.
        """
        # EXCLUDED FROM THE MARKER REQUIREMENT — each entry is a decision
        # with its reason, and the reason prints. Add to this list rather
        # than narrowing the walk, so the exclusion stays visible.
        skip = {
            "templates": "skeletons: instantiated, not read — a LIVE/SPEC/"
                         "LOG line on a {{PLACEHOLDER}} would be meaningless",
            ".claude": "agent, rule and skill definitions: configured by "
                       "YAML frontmatter, not by a status line",
        }
        # NOT WALKED AT ALL: version control and third-party trees. A
        # vendored CHANGELOG is somebody else's claim, not this project's,
        # and walking node_modules would make this check a stopwatch.
        vendor = {".git", "node_modules", "vendor", "venv", ".venv",
                  "build", "dist", "target", "__pycache__", ".mypy_cache"}
        seen, bad, unwalked = 0, [], 0
        excluded = {k: 0 for k in skip}
        excluded["repo root"] = 0
        for f in sorted(ROOT.rglob("*.md")):
            parts = f.relative_to(ROOT).parts
            if any(part in vendor for part in parts):
                unwalked += 1
                continue
            if len(parts) == 1:
                # CLAUDE.md and README.md are the operating rules and the
                # front door — always current by construction, and neither
                # is a dated document a reader could mistake for history.
                excluded["repo root"] += 1
                continue
            if parts[0] in skip:
                excluded[parts[0]] += 1
                continue
            seen += 1
            head = f.read_text(encoding="utf-8", errors="replace")[:400]
            if not any(k in head for k in ("LIVE", "SPEC", "LOG")):
                bad.append(str(f.relative_to(ROOT)))
        why = "; ".join(f"{k}/ {v} ({skip[k]})" if k in skip
                        else f"{k} {v}"
                        for k, v in excluded.items() if v)
        tail = (f"{sum(excluded.values())} excluded by decision"
                + (f" [{why}]" if why else "")
                + f", {unwalked} not walked (vendor/VCS)")
        if bad:
            return False, (f"docs: {len(bad)} of {seen} unmarked "
                           f"({', '.join(bad[:3])}"
                           + (f", +{len(bad) - 3} more not shown" if len(bad) > 3
                              else "") + f"); {tail}")
        if seen == 0:
            return True, f"docs: nothing measured — 0 documents examined; {tail}"
        return True, f"docs marked ({seen} checked); {tail}"

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

    return [("hooks_selftest", hooks_selftest),
            ("docs_marked", docs_marked),
            ("queue_startable", queue_startable)]


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
