
import ollama

from app.core.config import settings
from app.core.logger import logger


def generate_answer(
    question: str,
    context: str,
    search_query: str = ""
):

    logger.info(
        "LLM generation started"
    )

    logger.info(
        f"Using model: {settings.OLLAMA_MODEL}"
    )

    logger.info(
        f"Context length: {len(context)} characters"
    )

    logger.info(
        f"Search query length: {len(search_query)} characters"
    )

    try:

        response = ollama.chat(

            model=settings.OLLAMA_MODEL,

            options={
                "temperature": 0
            },

            messages=[

                {
                    "role": "system",

                    "content": """
You are an internal company knowledge assistant.

Answer the user's question using ONLY the Knowledge Base Context.

Rules:

1. The Knowledge Base Context is the only source of facts.

2. Do not use general knowledge.

3. Do not invent information.

4. The Standalone Search Query is only used to understand
   what the user's question refers to.

5. If the context contains an action performed by a person
   or role, that action can be used to answer questions
   about that person's role in that specific action.

6. The exact word "role" does NOT need to appear in the context.

Example:

Context:
"Leave applications must be approved by managers."

Question:
"What is the role of managers in approving annual leave?"

Answer:
"Managers approve annual leave applications."

7. Do not add responsibilities that are not stated in the context.

8. If the context does not contain information that can
   answer the question, reply exactly:

"I could not find this information in the knowledge base."

9. Keep the answer short and direct.

10. Return ONLY the answer.
"""
                },

                {
                    "role": "user",

                    "content": f"""
Knowledge Base Context:

{context}

Original User Question:

{question}

Standalone Search Query:

{search_query}

Answer the question using ONLY the Knowledge Base Context.
"""
                }

            ]

        )

    except Exception as e:

        logger.error(
            f"LLM generation failed: {e}"
        )

        raise


    answer = (
        response["message"]["content"]
        .strip()
    )


    logger.info(
        "LLM response generated successfully"
    )

    logger.info(
        f"Answer length: {len(answer)} characters"
    )

    return answer

