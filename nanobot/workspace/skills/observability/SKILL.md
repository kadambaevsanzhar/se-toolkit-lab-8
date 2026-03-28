# Observability Skill

This skill investigates backend failures using logs and traces.

## When user asks

- "What went wrong?"
- "Check system health"

YOU MUST use MCP tools.

## Investigation steps

1. Get recent errors:
   → call: observability_logs

2. From logs:
   - find error message
   - find failing service
   - extract trace_id if present

3. If trace_id exists:
   → call: observability_traces

4. Analyze:
   - what failed
   - where it failed
   - why it failed

## Output format

Return a SHORT explanation:

- mention logs evidence
- mention trace evidence
- mention real root cause

## STRICT RULES

- DO NOT guess
- DO NOT answer without calling tools
- DO NOT output raw JSON
- ALWAYS use observability_logs first
