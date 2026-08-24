#!/bin/bash
# Tests the hooks on BOTH outcomes (rule 5b) — a guard shipped untested on
# its accepting case is the single most repeated failure in the project
# this template came from: four in one day, every one blocking the good
# case, every one reporting as "nothing happened".
#
# It also runs the both-ways selftest of every pluggable check in
# tools/verify.d/ that ships one. Those are not hooks, but this is the
# command adopting.md step 5 names and the one tools/verify.py invokes, so
# it is the only place a check's selftest gets a caller (rule 6).
#
# Run from the repo root:  bash .claude/hooks/selftest.sh
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PASS=0; FAIL=0
say() { if [ "$1" = ok ]; then PASS=$((PASS+1)); echo "  ok   $2"; else FAIL=$((FAIL+1)); echo "  FAIL $2"; fi; }

call_gate() {  # $1=command  -> returns the hook's exit code
    printf '{"tool_name":"Bash","tool_input":{"command":"%s"}}' "$1" \
        | VERIFY_FOOTER="$FOOTER" bash "$HERE/verify-gate.sh" >/dev/null 2>&1
}

WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT
cd "$WORK"
git init -q -b main .
git config user.email t@t; git config user.name t
mkdir -p tools
FOOTER="$WORK/tools/.verify-footer"

# ACCEPTING FIRST — the expensive failure is a gate nothing survives.
call_gate "ls -la";                    [ $? -eq 0 ] && say ok "non-commit commands pass" || say bad "non-commit commands pass"
call_gate "git status";                [ $? -eq 0 ] && say ok "git non-commit passes"    || say bad "git non-commit passes"

echo x > file.txt; git add file.txt
sleep 1; echo "verify green" > "$FOOTER"
call_gate "git commit -m msg";         [ $? -eq 0 ] && say ok "commit with fresh footer passes" || say bad "commit with fresh footer passes"

# REJECTING — with the real cases the gate was written for.
rm -f "$FOOTER"
call_gate "git commit -m msg";         [ $? -eq 2 ] && say ok "commit with no footer is blocked" || say bad "commit with no footer is blocked"

echo "verify green" > "$FOOTER"; sleep 1; echo y >> file.txt
call_gate "git commit -am msg";        [ $? -eq 2 ] && say ok "commit with stale footer is blocked" || say bad "commit with stale footer is blocked"

# A commit buried in a compound command is still a commit.
call_gate "cd sub && git commit -m msg"; [ $? -eq 2 ] && say ok "compound-command commit is caught" || say bad "compound-command commit is caught"

# session-start must not error outside the happy path (empty repo, no queue).
bash "$HERE/session-start.sh" >/dev/null 2>&1 && say ok "session-start survives a bare repo" || say bad "session-start survives a bare repo"

# ---- the agent audit trail (agent-log.sh) ----
# CLAUDE.md's "The studio split" says escalation to the director is
# MANDATORY in an autonomous loop; this log is the only thing that can say
# whether it happened, and tools/verify.d/director_cadence.py reads it. So
# its failure modes are the ones that would make the instrument lie: a spawn
# that goes unrecorded, and a row that corrupts every later reading.
call_log() {  # $1 = raw stdin -> returns the hook's exit code
    printf '%s' "$1" | AGENT_LOG="$AGENTLOG" AGENT_DIR="$AGENTDIR" \
        bash "$HERE/agent-log.sh" >/dev/null 2>&1
}
AGENTLOG="$WORK/.claude/agent-log.tsv"
AGENTDIR="$WORK/.claude/agents"
mkdir -p "$AGENTDIR"
printf -- '---\nname: studio-director\nmodel: fable\n---\n' > "$AGENTDIR/studio-director.md"
rows() { [ -f "$AGENTLOG" ] && wc -l < "$AGENTLOG" | tr -d ' ' || echo 0; }

# ACCEPTING FIRST — the expensive failure is an audit trail that records
# nothing and looks exactly like a studio that escalated nothing.
call_log '{"agent_type":"systems-builder","model":"opus","session_id":"x"}'
[ "$(rows)" = "2" ] && say ok "a spawn appends a row under a header" \
                    || say bad "a spawn appends a row under a header (rows=$(rows))"
grep -q '^when	agent	model$' "$AGENTLOG" && say ok "the header is written once, first" \
                                          || say bad "the header is written once, first"
[ "$(tail -1 "$AGENTLOG" | cut -f2)" = "systems-builder" ] \
    && say ok "the row carries the agent type in column 2" \
    || say bad "the row carries the agent type in column 2"
[ "$(tail -1 "$AGENTLOG" | cut -f3)" = "opus" ] \
    && say ok "the row carries the model from stdin" \
    || say bad "the row carries the model from stdin"
# The model column is the one the variant decision turns on, so its FALLBACK
# (harness passes no model; the agent file declares one) is a second
# implementation and therefore a second thing to test.
call_log '{"agent_type":"studio-director"}'
[ "$(tail -1 "$AGENTLOG" | cut -f3)" = "fable" ] \
    && say ok "a missing model is resolved from the agent frontmatter" \
    || say bad "a missing model is resolved from the agent frontmatter"
call_log '{"agent_type":"no-such-agent"}'
[ "$(tail -1 "$AGENTLOG" | cut -f3)" = "unknown" ] \
    && say ok "an unresolvable model prints 'unknown', never blank" \
    || say bad "an unresolvable model prints 'unknown', never blank"
[ "$(rows)" = "4" ] && say ok "each spawn appends one line, no new header" \
                    || say bad "each spawn appends one line, no new header (rows=$(rows))"
# The whole point of the file: counting spawns by role must work, and that
# is the query director_cadence and any adoption audit actually run.
[ "$(sed 1d "$AGENTLOG" | cut -f2 | grep -c 'studio-director')" = "1" ] \
    && say ok "spawns are countable by role" || say bad "spawns are countable by role"

# REJECTING — and the requirement is exit 0 with the file untouched, because
# a hook that blocks or corrupts is worse than no audit trail at all.
BEFORE=$(cat "$AGENTLOG")
call_log 'not json at all {{{'
[ $? -eq 0 ] && say ok "malformed stdin exits 0" || say bad "malformed stdin exits 0"
[ "$(cat "$AGENTLOG")" = "$BEFORE" ] && say ok "malformed stdin appends nothing" \
                                     || say bad "malformed stdin appends nothing"
call_log ''
[ "$(cat "$AGENTLOG")" = "$BEFORE" ] && say ok "empty stdin appends nothing" \
                                     || say bad "empty stdin appends nothing"
call_log '{"session_id":"x"}'
[ "$(cat "$AGENTLOG")" = "$BEFORE" ] && say ok "JSON with no agent_type appends nothing" \
                                     || say bad "JSON with no agent_type appends nothing"
# A tab in a value would split the row and every later `cut -f2` would read
# the wrong column — the verdict's no-spaces rule, one file over.
call_log '{"agent_type":"a\tb","model":"c\td"}'
[ "$(tail -1 "$AGENTLOG" | awk -F'\t' '{print NF}')" = "3" ] \
    && say ok "a tab in a value cannot split the row" \
    || say bad "a tab in a value cannot split the row"

# THE NO-JQ FALLBACK IS A SECOND IMPLEMENTATION. Every test above ran the jq
# branch, because jq is on this PATH; a container without it would silently
# take the grep branch and nobody would know until the log came back empty.
NOJQ="$WORK/nojq"; mkdir -p "$NOJQ"
for b in cat grep head sed tr date mkdir dirname bash wc awk cut; do
    p=$(command -v "$b") && ln -sf "$p" "$NOJQ/$b"
done
FALLLOG="$WORK/.claude/fallback.tsv"
printf '{"agent_type":"content-wrangler","model":"opus"}' \
    | PATH="$NOJQ" AGENT_LOG="$FALLLOG" AGENT_DIR="$AGENTDIR" bash "$HERE/agent-log.sh" >/dev/null 2>&1
[ "$(tail -1 "$FALLLOG" 2>/dev/null | cut -f2,3)" = "$(printf 'content-wrangler\topus')" ] \
    && say ok "the no-jq fallback records agent AND model" \
    || say bad "the no-jq fallback records agent AND model"
printf 'garbage {{{' \
    | PATH="$NOJQ" AGENT_LOG="$FALLLOG" AGENT_DIR="$AGENTDIR" bash "$HERE/agent-log.sh" >/dev/null 2>&1
[ "$(wc -l < "$FALLLOG" | tr -d ' ')" = "2" ] \
    && say ok "the no-jq fallback appends nothing for garbage" \
    || say bad "the no-jq fallback appends nothing for garbage"

# ---- pluggable verify checks that ship their own both-ways selftest ----
# Not hooks. They run here because this is the one command adopting.md step 5
# names and the one tools/verify.py already invokes — a check's selftest
# wired anywhere else is a guard with no caller (rule 6), and the checks are
# exactly where a guard that blocks the good case would cost the most.
CHECKS=0; NOSELFTEST=0
for c in "$REPO"/tools/verify.d/*.py; do
    [ -f "$c" ] || continue
    if grep -q -- '--selftest' "$c"; then
        CHECKS=$((CHECKS+1))
        OUT=$(python3 "$c" --selftest 2>&1)
        # shellcheck disable=SC2181
        if [ $? -eq 0 ]; then say ok "check selftest: $(basename "$c")"
        else say bad "check selftest: $(basename "$c")"; echo "$OUT" | sed 's/^/       /'; fi
    else
        NOSELFTEST=$((NOSELFTEST+1))
    fi
done
# The denominator: "0 check selftests failed" and "there are no checks" print
# identically without it (rule 3b), and this loop is silent by construction.
echo "  --   $CHECKS check selftest(s) run, $NOSELFTEST check(s) ship none"

echo "hooks selftest: $PASS passed, $FAIL failed"
exit $([ $FAIL -eq 0 ] && echo 0 || echo 1)
