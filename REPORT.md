# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

Q: What is the agentic loop?
A: The agentic loop is the core iterative cycle that autonomous AI agents follow to accomplish tasks. It consists of four stages: perceive, think, act, and reflect.

Q: What labs are available in our LMS?
A: The agent attempted to answer by exploring the local workspace and listing lab files, but it does not use any LMS tools or backend integration.

## Task 1B — Agent with LMS tools

<!-- Paste the agent's response to "What labs are available?" and "Describe the architecture of the LMS system" -->

## Task 1C — Skill prompt

<!-- Paste the agent's response to "Show me the scores" (without specifying a lab) -->

## Task 2A — Deployed agent

Using config: /app/nanobot/config.resolved.json
WebChat channel enabled
✓ Channels enabled: webchat
MCP server 'lms': connected, 9 tools registered
MCP server 'webchat': connected, 1 tools registered
Agent loop started

## Task 2B — Web client

The WebChat endpoint was successfully exposed via Caddy at `/ws/chat`.

The Flutter web client was served at `/flutter` and allowed authentication using the configured access key.

After logging in, the agent responded to user queries through the WebSocket connection.

Example prompts tested:
- What can you do in this system?
- How is the backend doing?
- What labs are available?

The agent successfully returned responses, confirming:
- WebSocket connectivity
- LLM integration via OpenRouter
- MCP tool registration and usage

The backend was reported as healthy, though no lab data was present in the database.

## Task 3A — Structured logging

Happy-path log excerpt:
2026-03-28 17:59:55,744 ... request_started
2026-03-28 17:59:55,756 ... auth_success
2026-03-28 17:59:55,756 ... db_query
2026-03-28 17:59:55,882 ... request_completed
INFO: ... "GET /items/ HTTP/1.1" 200 OK

Error-path log excerpt:
2026-03-28 18:19:30,569 ... request_started
2026-03-28 18:19:30,571 ... auth_success
2026-03-28 18:19:30,582 ... db_query
2026-03-28 18:19:30,736 ERROR ... db_query
2026-03-28 18:19:30,740 ... request_completed
INFO: ... "GET /items/ HTTP/1.1" 404 Not Found

## Task 3B — Traces

Healthy trace:
- trace_id: 2e673167866b2ce6145f400f17dd8cb8

Error trace:
- trace_id: 3ef729f4041dac083af1ba86691a8e55

## Task 3C — Metrics

Metrics UI was accessed at /utils/metrics.

No metrics are displayed because OTEL_METRICS_EXPORTER is disabled (set to "none") and no metrics storage (VictoriaMetrics) is configured in the system.

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
Task 4A completed - observability skill created and tested
