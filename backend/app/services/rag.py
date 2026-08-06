from app.services.embedding import create_embedding
from app.services.vector_store import search_embedding
from app.services.llm import generate_answer

from app.services.chat_memory import save_message

from app.services.source_formatter import format_sources

from app.services.conversation_service import (
    update_title_if_empty
)

from app.services.context_builder import build_context



def ask_question(
    db,
    question: str,
    conversation_id: int,
    user_id: int
):


    # ==============================
    # 1. Build conversation memory
    # ==============================

    conversation_context = build_context(

        db=db,

        conversation_id=conversation_id,

        user_id=user_id

    )


    enhanced_query = f"""
{conversation_context}


Current question:

{question}
"""


    print("======== ENHANCED QUERY ========")
    print(enhanced_query)



    # ==============================
    # 2. Create embedding
    # ==============================

    query_vector = create_embedding(

        enhanced_query

    )



    # ==============================
    # 3. Vector Search
    # ==============================

    results = search_embedding(

        query_vector

    )



    if not results or results[0]["distance"] > 1.2:

        return {

            "question": question,

            "answer":
            "I could not find this information in the knowledge base.",

            "sources": []

        }



    # ==============================
    # 4. Prepare context for LLM
    # ==============================

    knowledge_context = "\n\n".join(

        [

            item["content"]

            for item in results

        ]

    )



    # ==============================
    # 5. Generate answer
    # ==============================

    answer = generate_answer(

        question=question,

        context=knowledge_context,

        history=conversation_context

    )



    # ==============================
    # 6. Save conversation
    # ==============================

    save_message(

        db=db,

        conversation_id=conversation_id,

        role="user",

        content=question

    )


    save_message(

        db=db,

        conversation_id=conversation_id,

        role="assistant",

        content=answer

    )



    # ==============================
    # 7. Update title
    # ==============================

    update_title_if_empty(

        db=db,

        conversation_id=conversation_id,

        title=question[:50]

    )



    # ==============================
    # 8. Format sources
    # ==============================

    sources = format_sources(

        results

    )



    return {

        "question": question,

        "answer": answer,

        "sources": sources

    }