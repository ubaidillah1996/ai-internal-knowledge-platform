from app.services.llm import generate_answer



def generate_summary(history):


    prompt = f"""

Summarize this conversation briefly.

Conversation:

{history}


Summary:
"""


    summary = generate_answer(

        question="Summarize conversation",

        context=prompt,

        history=""

    )


    return summary