import ollama

from app.core.config import settings


def generate_answer(
    question: str,
    context: str,
    history: str = ""
):

    response = ollama.chat(

        model=settings.OLLAMA_MODEL,

        messages=[

            {
                "role": "system",
                "content": """
You are an internal company knowledge assistant.

Answer only based on the provided knowledge base context.

Use conversation history only to understand references.

If the answer is not available,
say:
'I could not find this information in the knowledge base.'
"""
            },

            {
                "role": "user",
                "content": f"""
Conversation History:

{history}


Knowledge Base Context:

{context}


Question:

{question}
"""
            }

        ]

    )


    return response["message"]["content"]