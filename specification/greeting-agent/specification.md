# Specification: greeting-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [x] Read the project input (`product-requirements-document.md`, `intent.md`)
- [x] Bootstrap agent code in `assets/greeting-agent/` using instructions from the sap-agent-bootstrap section
- [x] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

No runtime skills needed — the greeting logic is simple, no branching workflows or reference material required.

---

## Project-Specific Tasks

## Core Greeting Logic

- [x] Implement a `get_greeting` tool in `assets/greeting-agent/app/tools.py`
- [x] Wire the `get_greeting` tool into the agent's tool list in `agent_executor.py`
- [x] Update the system prompt (via `@prompt_section`) with greeting instructions

## Agent Configuration

- [x] Verify `@agent_model` decorators reference the correct LLM model names (primary + fallback)
- [x] Verify `@agent_config` decorators are set for temperature and agent memory TTL
- [x] Verify `@prompt_section` decorator is present with the greeting instructions

---

## Business Instrumentation

- [x] Implement business step instrumentation for all 4 milestones (M1-M4)
- [x] Add OpenTelemetry custom spans using context manager form in `_run_agent()`
- [x] Verify `auto_instrument()` is called at top of `main.py` before any AI framework imports

---

## MCP Tool Integration

No SAP API integrations required — skipped all MCP-related tasks.

---

## Testing

- [x] Install test dependencies
- [x] Write unit tests for `get_greeting` tool (all 4 time ranges + fallback)
- [x] Write integration tests (3 end-to-end tests)
- [x] Run `pytest` — coverage at 70% ✓
- [x] Verify exactly 5 decorated functions in `app/agent.py` ✓
- [x] Run final `pytest` to generate `test_report.json`
- [x] Verify `test_report.json` exists ✓
