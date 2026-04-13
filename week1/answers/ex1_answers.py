"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_A_XML_ANSWER      = "The Albanach"
PART_A_SANDWICH_ANSWER = "The Albanach"

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT    = True
PART_A_XML_CORRECT      = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
All three presentation formats produced correct answers with the 70B model on the
baseline dataset. The PLAIN condition returned The Haymarket Vaults, while XML and
SANDWICH both returned The Albanach. This suggests that the structured XML format
shifted the model's attention toward the first matching venue (The Albanach appears
first in the list), while plain text processing led to The Haymarket Vaults. The
signal-to-noise ratio was high enough for the strong model to handle all formats
correctly — the dataset was too clean to expose structural sensitivity.
"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_B_XML_ANSWER      = "The Albanach"
PART_B_SANDWICH_ANSWER = "The Albanach"

PART_B_PLAIN_CORRECT    = True
PART_B_XML_CORRECT      = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = False

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
The Holyrood Arms is the most dangerous distractor because it satisfies two of
the three constraints (capacity=160 and vegan=yes), failing only on status=full.
A model that skims rather than evaluating all three constraints simultaneously
would likely select it. The New Town Vault is less dangerous because it fails on
vegan=no, which is a more salient feature to check.
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True

PART_C_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_C_XML_ANSWER      = "The Haymarket Vaults"
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults"

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
Even the smaller 8B model (Meta-Llama-3.1-8B-Instruct) answered correctly across
all three conditions with near-miss distractors. The 8B model consistently chose
The Haymarket Vaults regardless of format, unlike the 70B model which preferred
The Albanach in structured formats. This shows that even a smaller model can
handle this particular constraint-checking task when the dataset is small enough
(9 venues). The structural effect described in the Liu et al. research likely
requires longer contexts to manifest — our venue list is short enough that both
models can attend to all items effectively.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when the signal-to-noise ratio is low — that is,
when there are many items to evaluate, near-miss distractors are present, and the
correct answer is buried in the middle of a long context. On short, clean datasets
like this one, even a small 8B model extracts the right answer regardless of format.
But as agents scale to real-world data — hundreds of venues, noisy web search results,
multi-document contexts — structured formatting (XML tags, sandwich pattern) becomes
critical for reliable extraction. The effect is model-size dependent: smaller models
hit the formatting sensitivity threshold sooner as context grows.
"""
