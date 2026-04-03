# Observability Skill

This skill investigates backend failures using logs and traces.

## When user asks

- "What went wrong?"
- "Check system health"

YOU MUST use MCP tools. Follow this order every time (one-shot investigation).

## Investigation steps

1. **Logs first** — call `observability_logs` and focus on the most recent ERROR (or failing `request_completed` with 5xx). Note timestamps, path, and any `trace_id` / `traceId` in the log line or structured fields.

2. **Trace ID** — if any log line mentions a trace identifier, copy it exactly. If logs are inconclusive, still try the latest error-related trace if your tools allow listing by time window.

3. **Trace** — if you have a trace ID, call `observability_traces` for that id before you conclude.

4. **Synthesize** — in plain language:
   - what failed (service / route / operation)
   - what the logs show (one or two concrete facts: status, event, message)
   - what the trace confirms (spans / failure point), or say that trace data was missing

## Output format

Return a **short** coherent summary (a few sentences or a tight bullet list):

- one line on **log evidence** (what you saw in logs)
- one line on **trace evidence** (what the trace showed, or “no trace fetched”)
- one line on **likely root cause** (tied to the above, not generic advice)

## STRICT RULES

- DO NOT guess
- DO NOT answer without calling tools
- DO NOT paste raw JSON or full log dumps — quote only the minimum needed
- ALWAYS call `observability_logs` before `observability_traces`
