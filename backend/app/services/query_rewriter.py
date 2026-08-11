
import re
import ollama

from app.core.config import settings
from app.core.logger import logger


QUESTION_TYPES = [
    "who",
    "what",
    "when",
    "where",
    "why",
    "how",
]


def get_question_type(question: str):
    question = question.strip().lower()

    for qtype in QUESTION_TYPES:
        if question.startswith(qtype):
            return qtype

    return None

def normalize_question_type(question: str):
    question = question.strip()

    question_type = get_question_type(question)

    if not question_type:
        return question

    return (
        question_type.capitalize()
        + question[len(question_type):]
    )

def repair_rewrite(
    question: str,
    history: str,
    bad_result: str
):
    """
    Repair a failed query rewrite while preserving
    the original question type and intent.
    """

    original_type = get_question_type(question)

    prompt = f"""
You are repairing a failed query rewrite.

Original Question:

{question}

Conversation History:

{history}

Incorrect Rewrite:

{bad_result}

Your task:

1. Preserve the original question type.
2. Resolve ONLY conversational references.
3. Do not change the user's intent.
4. Do not answer the question.
5. Do not add new information.
6. Return exactly ONE standalone search question.

CRITICAL:

The rewritten question MUST start with the same
question type as the original question.

Original question type:

{original_type}

Therefore:

WHO must remain WHO.
WHAT must remain WHAT.
WHEN must remain WHEN.
WHERE must remain WHERE.
WHY must remain WHY.
HOW must remain HOW.

Example:

Original:

Who approves it?

History:

user: Who approves annual leave?
assistant: Managers approve annual leave applications.

Incorrect Rewrite:

What is the role of managers in approving annual leave?

Correct Rewrite:

Who approves annual leave?

The only task is to resolve the reference "it".

Do not change WHO into WHAT.

Do not change WHAT into WHO.

Do not answer the question.

Do not add responsibilities or assumptions.

Return ONLY the repaired standalone question.
"""

    try:

        response = ollama.chat(
            model=settings.OLLAMA_MODEL,
            options={
                "temperature": 0
            },
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You repair query rewrites. "
                        "Preserve the original question type "
                        "and resolve references only. "
                        "Return exactly one standalone "
                        "search question."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

    except Exception as e:

        logger.error(
            f"Rewrite repair failed: {e}"
        )

        return question

    repaired = (
        response["message"]["content"]
        .strip()
    )

    repaired = normalize_question_type(repaired)

    logger.info(
        f"Repaired rewrite result: {repaired}"
    )

    if not repaired:

        logger.warning(
            "Repair result empty. "
            "Fallback to original question."
        )

        return question

    if len(repaired.split()) <= 2:

        logger.warning(
            "Repair result too short. "
            "Fallback to original question."
        )

        return question

    repaired_type = get_question_type(repaired)

    if (
        original_type
        and repaired_type
        and original_type != repaired_type
    ):
        logger.warning(
            "Repair still changed question type: "
            f"{original_type} -> {repaired_type}"
        )

        return question


    # ==========================================
    # Detect unresolved references
    # ==========================================

    reference_words = [
        "it",
        "its",
        "they",
        "their",
        "them",
        "this",
        "that",
        "those",
        "these",
    ]

    repaired_tokens = re.findall(
        r"\b\w+\b",
        repaired.lower()
    )

    unresolved_reference = any(
        word in repaired_tokens
        for word in reference_words
    )


    if unresolved_reference:

        logger.warning(
            "Repair still contains unresolved "
            "reference: %s",
            repaired
        )

        history_lines = [
            line.strip()
            for line in history.splitlines()
            if line.strip()
        ]

        previous_user_questions = [
            line[5:].strip()
            for line in history_lines
            if line.lower().startswith("user:")
        ]

        if previous_user_questions:

            previous_question = (
                previous_user_questions[-1]
            )

            previous_type = get_question_type(
                previous_question
            )

            if (
                previous_type
                and previous_type == original_type
            ):

                fallback = normalize_question_type(
                    previous_question
                )

                logger.info(
                    "Using previous user question "
                    "as deterministic fallback: %s",
                    fallback
                )

                return fallback

        return question


    return repaired


    # ==========================================
    # Validate reference resolution
    # ==========================================

    reference_words = [
        "it",
        "its",
        "they",
        "their",
        "them",
        "this",
        "that",
        "those",
        "these",
    ]

    question_tokens = re.findall(
        r"\b\w+\b",
        question.lower()
    )

    repaired_lower = repaired.lower()

    unresolved_reference = any(
        word in repaired_lower.split()
        for word in reference_words
    )

    if unresolved_reference:

        logger.warning(
            "Repair still contains unresolved reference. "
            "Falling back to original question."
        )

        # Try one final deterministic repair using the
        # most recent user question from history.
        history_lines = [
            line.strip()
            for line in history.splitlines()
            if line.strip()
        ]

        previous_user_questions = [
            line[5:].strip()
            for line in history_lines
            if line.lower().startswith("user:")
        ]

        if previous_user_questions:

            previous_question = previous_user_questions[-1]

            previous_type = get_question_type(
                previous_question
            )

            if (
                previous_type
                and previous_type == original_type
            ):

                return normalize_question_type(
                    previous_question
                )

        return question


    return repaired

def rewrite_query(
    question: str,
    history: str
):

    # ==============================
    # Check whether rewrite is needed
    # ==============================

    reference_words = [
        "it",
        "its",
        "they",
        "their",
        "them",
        "this",
        "that",
        "those",
        "these",
        "above",
        "previous",
        "earlier",
        "mentioned",
    ]

    tokens = re.findall(
        r"\b\w+\b",
        question.lower()
    )

    needs_rewrite = any(
        word in tokens
        for word in reference_words
    )

    if not needs_rewrite:

        logger.info(
            "No reference detected. "
            "Skipping query rewrite."
        )

        return question

    # ==============================
    # Rewrite prompt
    # ==============================

    prompt = f"""
You are a query rewriting system for a company knowledge search engine.

Your ONLY task is to rewrite the current question into a standalone
search query.

When resolving a reference, preserve the minimum relevant context
from Conversation History required to make the rewritten question
independently searchable.

If the current question refers to a person, action, object,
process, or topic from the previous conversation, include that
context when necessary.

Do not add new information.

Do not broaden the question.

Do not narrow the question.

Only carry forward context that is explicitly present
in Conversation History.

Resolve pronouns and references using Conversation History.

Preserve the original meaning of the question.

Replace references such as:

it
its
they
their
them
this
that
those
these
above
previous
earlier
mentioned

Use ONLY information available in Conversation History
to resolve references.

Do NOT answer the question.

Do NOT invent information.

Do NOT add responsibilities, explanations, assumptions,
reasons, procedures, or details that are not required
to resolve the reference.

Do NOT change the user's intent.

IMPORTANT:

ONLY resolve references and preserve the minimum
conversation context required for standalone retrieval.

Do NOT rewrite the user's intent.

Keep words such as:

role
responsibility
process
requirement
policy
approval

unchanged if they already appear in the question.

CRITICAL OUTPUT RULE:

The first word of the rewritten question MUST match
the question type of the original question.

WHO -> WHO
WHAT -> WHAT
WHEN -> WHEN
WHERE -> WHERE
WHY -> WHY
HOW -> HOW

The grammatical question type is part of the user's intent.

If the original question asks WHO,
the rewritten question MUST ask WHO.

If the original question asks WHAT,
the rewritten question MUST ask WHAT.

If the original question asks WHEN,
the rewritten question MUST ask WHEN.

If the original question asks WHERE,
the rewritten question MUST ask WHERE.

If the original question asks WHY,
the rewritten question MUST ask WHY.

If the original question asks HOW,
the rewritten question MUST ask HOW.

Example:

Conversation History:

user: Who approves annual leave?
assistant: Managers approve annual leave applications.

Current Question:

Who approves it?

Correct rewrite:

Who approves annual leave?

Incorrect rewrite:

What is the role of managers in approving annual leave?

Incorrect rewrite:

Who is responsible for approving annual leave?

The only task is to resolve "it".

Another example:

Conversation History:

user: Who approves annual leave?
assistant: Managers approve annual leave applications.

Current Question:

What about their role?

Correct rewrite:

What is the role of managers in approving annual leave?

Incorrect rewrite:

Who is responsible for approving annual leave?

Another example:

Conversation History:

user: How many annual leave days do employees receive?
assistant: Employees receive 25 days annual leave.

user: Who approves it?
assistant: Managers approve annual leave applications.

Current Question:

What about their role?

Correct rewrite:

What is the role of managers in approving annual leave?

Do not change the question type.

Do not answer the question.

Do not add new information.

Return exactly ONE standalone search question.

Conversation History:

{history}

Current Question:

{question}

Standalone Search Query:
"""

    # ==============================
    # Call LLM
    # ==============================

    try:

        response = ollama.chat(
            model=settings.OLLAMA_MODEL,
            options={
                "temperature": 0
            },
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You resolve references in questions "
                        "for knowledge base retrieval. "
                        "Return only one standalone "
                        "search question."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

    except Exception as e:

        logger.error(
            f"Query rewrite failed: {e}"
        )

        return question

    result = (
        response["message"]["content"]
        .strip()
    )

    logger.info(
        f"Raw rewrite result: {result}"
    )

    # ==============================
    # Basic validation
    # ==============================

    if not result:

        logger.warning(
            "Rewrite result empty. "
            "Fallback to original question."
        )

        return question

    if len(result.split()) <= 2:

        logger.warning(
            "Rewrite result too short. "
            "Fallback to original question."
        )

        return question

    # ==============================
    # Question type validation
    # ==============================

    original_type = get_question_type(question)
    rewritten_type = get_question_type(result)

    if (
        original_type
        and rewritten_type
        and original_type != rewritten_type
    ):

        logger.warning(
            "Question type changed during rewrite: "
            f"{original_type} -> {rewritten_type}"
        )

        result = repair_rewrite(
            question=question,
            history=history,
            bad_result=result
        )

    # ==============================
    # Validate repaired result
    # ==============================

    if not result:

        logger.warning(
            "Final rewrite result empty. "
            "Fallback to original question."
        )

        return question

    if len(result.split()) <= 2:

        logger.warning(
            "Final rewrite result too short. "
            "Fallback to original question."
        )

        return question

    # ==============================
    # Final question type validation
    # ==============================

    final_type = get_question_type(result)

    if (
        original_type
        and final_type
        and original_type != final_type
    ):

        logger.warning(
            "Final rewrite still changed question type: "
            f"{original_type} -> {final_type}"
        )

        return question

    # ==============================
    # Intent preservation validation
    # ==============================

    intent_words = [
        "role",
        "responsibility",
        "process",
        "requirement",
        "policy",
        "approval",
    ]

    question_lower = question.lower()
    result_lower = result.lower()

    for word in intent_words:

        if word in question_lower:

            if word not in result_lower:

                logger.warning(
                    f"Intent changed during rewrite: {word}"
                )

                return question

    result = normalize_question_type(result)

    return result

