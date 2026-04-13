"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Albanach"
QUERY_1_VENUE_ADDRESS = "2 Hunter Square, Edinburgh"
QUERY_2_FINAL_ANSWER  = "No venues found matching the constraints — no venue in the database can accommodate 300 people with vegan options."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
Changed The Albanach's status from 'available' to 'full' in mcp_venue_server.py and re-ran
the client. The only file modified was mcp_venue_server.py — the client code
(exercise4_mcp_client.py) required zero changes. The client discovers tools dynamically
from the server at connection time, so when the server's data changes, the client automatically
gets the updated results. With The Albanach set to full, only The Haymarket Vaults would remain
as a valid match for Query 1 (160 guests, vegan). This demonstrates the core value of MCP:
the tool server is a single source of truth. Change the data in one place and every connected
client — LangGraph agent, Rasa action, or any other MCP consumer — sees the update immediately.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 0
LINES_OF_TOOL_CODE_EX4 = 0

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP provides dynamic tool discovery — clients don't hardcode which tools exist. Add a new
@mcp.tool() to the server and every client picks it up automatically on the next connection.
This is fundamentally different from importing Python functions, where each client must update
its import statements and tool lists manually.

Second, MCP decouples the tool runtime from the agent runtime. The server can be written in any
language, run on a different machine, or be shared across teams. The LangGraph agent and Rasa
action server connect to the same server, guaranteeing data consistency without code duplication.

Third, MCP enables protocol-level tool introspection. The client can list tools, inspect their
schemas, and validate parameters before calling — the same standardised interface regardless of
what the tool actually does underneath.
"""

# ── Week 5 architecture ────────────────────────────────────────────────────
# Describe your full sovereign agent at Week 5 scale.
# At least 5 bullet points. Each bullet must be a complete sentence
# naming a component and explaining why that component does that job.

WEEK_5_ARCHITECTURE = """
- The LangGraph research agent handles open-ended tasks (venue search, cost estimation, weather checks) because autonomous reasoning is needed when the path cannot be predetermined and the agent must pivot on failures.
- The Rasa CALM confirmation agent handles structured human interactions (booking confirmations, deposit agreements) because every word in these conversations has financial or legal implications requiring deterministic, auditable execution paths.
- The MCP tool server provides a shared tool layer that both agents connect to, ensuring data consistency and enabling new tools to be added once and discovered by all clients automatically.
- A persistent memory layer (CLAUDE.md filesystem memory + Pinecone vector store) allows the agent to remember past sessions and learn from previous bookings, avoiding repeated work and improving recommendations over time.
- LangSmith observability traces every agent step — tool calls, model reasoning, token usage, and latency — enabling cost tracking, debugging, and safety guardrails that prevent runaway loops or excessive spending in production.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
The LangGraph agent handles the research because it can autonomously check multiple venues,
pivot when The Bow Bar is full (as seen in Exercise 2 Scenario 1 — it checked all four venues
without being told which ones to try), calculate costs, and generate flyers in whatever order
makes sense. The path isn't predetermined — the agent reasons its way through.

The Rasa CALM agent handles the manager's call because the conversation must follow a strict
sequence: collect guest_count, then vegan_count, then deposit_amount_gbp, then validate against
Rod's constraints in Python. When the deposit exceeds £300, the agent escalates — always, no
exceptions, no reasoning about it. The LLM cannot negotiate these limits.

Swapping feels wrong because the LangGraph agent in Exercise 2 Scenario 3 gave a vague,
dismissive response to an out-of-scope question — "your input is lacking necessary details."
Imagine that response to a pub manager calling about a real booking. CALM's explicit
handle_out_of_scope flow ensures a professional deflection every time. Conversely, trying to
predetermine every possible research path in YAML flows would be impossibly rigid — you cannot
write a flow for "what if the first two venues are full and the weather changes the plan."
"""
