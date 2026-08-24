#!/bin/bash
# SubagentStart hook: append one row per agent spawn to .claude/agent-log.tsv.
#
# WHY THIS EXISTS. CLAUDE.md's "The studio split" says the direction role is
# spawned on MANDATORY triggers in an autonomous loop, and the owner's
# condition on that arrangement was "no point in having a fable director if
# it's never called upon." That is a claim about behaviour, and a claim
# without an instrument decays (this template's premise). This log is the
# instrument: whether the triggers actually fire becomes a one-command read
# instead of a transcript archaeology dig.
#
#     cut -f2 .claude/agent-log.tsv | sed 1d | sort | uniq -c | sort -rn
#
# It is also the input `tools/verify.d/director_cadence.py` reads, so the
# cadence gate is measuring spawns that happened rather than spawns that
# were intended.
#
# COMMITTED, NOT IGNORED. An instrument that lives only in an ephemeral
# container is one the next session cannot read (rule 12: prefer a channel
# this environment can definitely read — in a repo, that means a tracked
# file).
#
# Contract (Claude Code SubagentStart):
#   stdin:  { "agent_type": "systems-builder", "model": "opus", ... }
#   exit 0  = proceed. This hook NEVER blocks: a broken audit trail must not
#             be able to stop the work it exists only to describe.
#
# Columns: when<TAB>agent<TAB>model. The model column is there because the
# whole variant decision is about WHICH MODEL holds the direction role — a
# log that cannot distinguish a fable director from an opus builder cannot
# answer the question it was built for.
#
# Tested both ways (rule 5b) by .claude/hooks/selftest.sh, accepting first:
#   ACCEPT: JSON with agent_type appends exactly one three-column row;
#           model absent from stdin is resolved from the agent's frontmatter
#   REJECT: malformed/empty stdin exits 0 and appends nothing — the file it
#           audits cannot be corrupted by garbage arriving at it

LOG="${AGENT_LOG:-.claude/agent-log.tsv}"
AGENT_DIR="${AGENT_DIR:-$(cd "$(dirname "$0")/../agents" 2>/dev/null && pwd)}"

INPUT=$(cat)

field() {  # $1 = json key -> its string value, or empty
    if command -v jq >/dev/null 2>&1; then
        printf '%s' "$INPUT" | jq -r ".$1 // empty" 2>/dev/null
    else
        # Same fallback shape as verify-gate.sh: this hook must work on a
        # container where jq was never installed, and a silently-skipped
        # audit row is indistinguishable from a session that delegated
        # nothing. One idea, two implementations — the selftest runs both.
        printf '%s' "$INPUT" \
            | grep -oE "\"$1\"[[:space:]]*:[[:space:]]*\"([^\"\\\\]|\\\\.)*\"" \
            | head -1 | sed "s/^\"$1\"[[:space:]]*:[[:space:]]*\"//; s/\"$//"
    fi
}

AGENT=$(field agent_type)

# NOTHING PARSED, NOTHING WRITTEN. A row with an empty agent column would
# read as "an agent with no name ran", which is a finding; the truth is that
# this hook could not tell, and those must not look the same (rule 3b).
[ -n "$AGENT" ] || exit 0

MODEL=$(field model)
if [ -z "$MODEL" ] && [ -n "$AGENT_DIR" ] && [ -f "$AGENT_DIR/$AGENT.md" ]; then
    # The harness does not always pass the model; the agent file always
    # declares one, and that declaration is what actually took effect.
    MODEL=$(sed -n 's/^model:[[:space:]]*//p' "$AGENT_DIR/$AGENT.md" | head -1)
fi
# Never blank. An empty third column reads as "ran on no model", which is
# not a thing; "unknown" says the hook could not resolve it (rule 3b again).
[ -n "$MODEL" ] || MODEL=unknown

# A TAB IN A VALUE WOULD SPLIT THE ROW, the same fault as a space in a
# key=value verdict — every reader of this file splits on tabs, including
# director_cadence.py. Newlines and carriage returns likewise.
AGENT=$(printf '%s' "$AGENT" | tr '\t\n\r' '   ')
MODEL=$(printf '%s' "$MODEL" | tr '\t\n\r' '   ')

mkdir -p "$(dirname "$LOG")" 2>/dev/null
# The header is written only when the file is absent or empty, so an
# existing log is never rewritten — this file is append-only by
# construction (rule 5: scope the write to exactly what this spawn made).
[ -s "$LOG" ] || printf 'when\tagent\tmodel\n' >> "$LOG"
printf '%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$AGENT" "$MODEL" >> "$LOG"

exit 0
