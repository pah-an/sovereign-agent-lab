"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  200 pounds deposit
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
"""

CONVERSATION_1_OUTCOME = "confirmed"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  calling to confirm a booking
I'm sorry, I'm not trained to help with that.
How many guests are you confirming for tonight's event?
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  500 pounds deposit
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
"""

CONVERSATION_2_OUTCOME = "escalated"
CONVERSATION_2_REASON  = "a deposit of £500 exceeds the organiser's authorised limit of £300"

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?
I'm sorry, I'm not trained to help with that.
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM recognized the parking question as out-of-scope and responded with the utter_out_of_scope
message: "I can only help with confirming tonight's venue booking. For anything else, please
contact the event organiser directly." It then asked "Would you like to continue with confirm
booking?" — offering to resume the confirm_booking flow exactly where it left off, without
losing the already-collected guest_count slot (160). The flow state was preserved.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
Rasa CALM handled the out-of-scope request gracefully: it acknowledged the request was outside
its scope with a specific, helpful redirect ("contact the event organiser directly"), then
offered to resume the booking flow without losing context. The guest_count slot was preserved.

The LangGraph agent in Exercise 2 Scenario 3 responded with a vague, unhelpful "Your input is
lacking necessary details. Please provide more information or specify the task you need help
with." It didn't acknowledge the question was out of scope, didn't suggest alternatives, and
didn't offer any way forward.

The key structural difference: CALM has an explicit handle_out_of_scope flow in flows.yml that
routes off-topic requests to a defined response. LangGraph has no such mechanism — the model
improvises its response, which in this case produced something dismissive and confusing. For
customer-facing interactions, CALM's deterministic handling is more professional and reliable.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
Uncommented the four-line cutoff guard block in ActionValidateBooking.run(). Tested it by
running a conversation after 16:45 — the guard triggered immediately after all three slots
were collected, returning: "I need to check one thing with the organiser before I can confirm.
The issue is: it is past 16:45 — insufficient time to process the confirmation before the
5 PM deadline. Can I call you back within 15 minutes?" Verified the escalation worked, then
ran the happy path with the guard temporarily disabled to confirm the rest of the logic still
works correctly.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

CALM_VS_OLD_RASA = """
The LLM now handles slot extraction that Python regex used to do. "About 50 need vegan" and
"200 pounds deposit" were parsed by the LLM via from_llm slot mappings into 50.0 and 200.0
automatically — no ValidateBookingConfirmationForm with regex patterns needed. Intent
classification is also gone — CALM reads flow descriptions instead of needing nlu.yml training
examples.

Python STILL handles the business rules: MAX_GUESTS (170), MAX_DEPOSIT_GBP (300), and
MAX_VEGAN_RATIO (0.80) are enforced deterministically in ActionValidateBooking. A deposit
of £500 is always rejected regardless of how the manager phrases it — as we saw in
Conversation 2.

The trade-off: you trust the LLM more for language understanding (which it excels at), but
you lose the explicit, testable parsing rules that regex provided. CALM's LLM extraction is
a black box — it works better for natural language ("about fifty" → 50.0), but when it fails,
debugging is harder than fixing a regex pattern.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

SETUP_COST_VALUE = """
CALM still required config.yml, domain.yml, flows.yml, endpoints.yml, a trained model, two
terminals (action server + shell), and a Rasa Pro licence. That setup cost bought something
specific: deterministic execution paths that are readable, auditable, and predictable.

The CALM agent CANNOT improvise a response outside defined flows. It cannot call a tool not
defined in flows.yml. It cannot decide to skip the deposit question if the manager sounds
trustworthy. When the parking question came in Conversation 3, it routed to handle_out_of_scope
and offered to resume — every time, guaranteed. You cannot make that guarantee with LangGraph,
where the model decides each step at runtime. For the confirmation use case — where every word
could cost money or create a legal commitment — this predictability is a feature, not a
limitation. A compliance officer can read flows.yml and verify the agent will never accept a
deposit above £300.
"""
