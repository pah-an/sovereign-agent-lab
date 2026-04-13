"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = [
    "check_pub_availability",
    "check_pub_availability",
    "calculate_catering_cost",
    "get_edinburgh_weather",
    "generate_event_flyer",
]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = True

TASK_A_NOTES = (
    "In Task A the model returned tool calls as JSON text strings in one AI message "
    "rather than using the proper function-calling format. The tool_calls_made list was "
    "empty as a result, but the model's intent was to call all five tools in the correct "
    "order. This is a known failure mode with Llama models on complex multi-tool prompts — "
    "the model sometimes serializes calls as text rather than invoking them through the "
    "tool-calling API."
)

# ── Task B ─────────────────────────────────────────────────────────────────

# Has generate_event_flyer been implemented (not just the stub)?
TASK_B_IMPLEMENTED = True

# The image URL returned (or the error message if still a stub).
TASK_B_IMAGE_URL_OR_ERROR = "https://pictures-storage.storage.eu-north1.nebius.cloud/text2img-7bc7f9e7-4664-40f1-95ab-1ccfc4146ae9_00001_.webp"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for Edinburgh AI Meetup, tech professionals, modern venue at The Haymarket Vaults, Edinburgh. 160 guests tonight. Warm lighting, Scottish architecture background, clean modern typography."

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
After checking The Bow Bar and getting meets_all_constraints=false (status full, capacity only
80), the agent immediately pivoted and checked The Haymarket Vaults, The Guilford Arms, and
The Albanach. It then selected The Albanach (capacity 180, vegan, available) as the fallback
venue without any human guidance.
"""

SCENARIO_1_FALLBACK_VENUE = "The Albanach"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
None of the known venues meet the capacity and dietary requirements. The Albanach, The
Haymarket Vaults, and The Guilford Arms have a capacity of 180, 160, and 200 respectively,
which is less than the required capacity of 300. The Bow Bar has a capacity of 80, which is
also less than the required capacity, and it is currently full. Therefore, none of the known
venues can accommodate 300 people with vegan options.
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False

SCENARIO_3_RESPONSE = "Your input is lacking necessary details. Please provide more information or specify the task you need help with."

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
This behaviour is not ideal for a production booking assistant. Instead of saying "your input
is lacking necessary details," the agent should clearly state that it does not have access to
train schedule information and suggest an alternative (e.g., checking National Rail or
ScotRail websites). The current response sounds dismissive and gives no useful guidance.
A well-designed agent should gracefully decline out-of-scope requests while directing the user
to appropriate resources, rather than implying the user did something wrong.
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	agent(agent)
	tools(tools)
	__end__([<p>__end__</p>]):::last
	__start__ --> agent;
	agent -.-> __end__;
	agent -.-> tools;
	tools --> agent;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/rules.yml. Min 30 words.
TASK_D_COMPARISON = """
The LangGraph graph is a single agent-tools loop: start → agent → tools → agent → end. The
model decides at every step which tool to call, in what order, and when to stop. There are no
explicit paths — all routing is implicit in the model's reasoning.

Rasa CALM flows.yml is the opposite: every possible task (confirm_booking, handle_out_of_scope)
is defined explicitly with deterministic steps. The LLM only decides which flow to enter. After
that, Rasa executes collect → collect → collect → action_validate_booking in a fixed sequence.
You can read every possible path by reading the YAML file.

LangGraph trades predictability for flexibility — the agent can handle novel situations but
might take unexpected paths. Rasa trades flexibility for auditability — every decision is
traceable, but the agent cannot improvise beyond defined flows.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
The most surprising behaviour was in Task A: the Llama model serialized all five tool calls
as JSON text strings in a single AI message instead of actually invoking them through the
function-calling API. It listed check_pub_availability (twice), calculate_catering_cost,
get_edinburgh_weather, and generate_event_flyer with correct parameters — but as literal text,
not executable calls. Yet in Tasks B and C, the same model correctly used the tool-calling
mechanism. This shows that a complex multi-step prompt can cause the model to "describe" what
it would do rather than doing it — a critical distinction for production agents where you need
actual execution, not plans.
"""
