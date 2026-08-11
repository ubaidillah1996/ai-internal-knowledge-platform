from app.services.embedding import create_embedding
from app.services.vector_store import search_embedding
from app.services.llm import generate_answer

from app.services.chat_memory import (
    save_message,
    get_history,
    format_history
)

from app.services.source_formatter import format_sources

from app.services.conversation_service import (
    update_title_if_empty
)

from app.services.context_builder import build_context

from app.services.query_rewriter import rewrite_query

from app.services.conversation_summarizer import (
    generate_summary,
    save_summary
)
from app.services.reranker import rerank

import logging

logger = logging.getLogger("ai-platform")



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


    logger.info(
        "Conversation context: %s",
        conversation_context
    )



    # ==============================
    # 2. Rewrite query for retrieval
    # ==============================

    search_query = rewrite_query(

        question=question,

        history=conversation_context

    )

    
    logger.info(
        "Original question: %s",
        question
    )

   
    logger.info(
        "Search query: %s",
        search_query
    )


    print("================ SEARCH QUERY ================")
    print(search_query)



    # ==============================
    # 3. Create embedding
    # ==============================

    query_vector = create_embedding(

        search_query

    )



    # ==============================
    # 4. Vector Search
    # ==============================

    results = search_embedding(

        query_vector

    )

    # ==============================
    # 4.5 Rerank search results
    # ==============================

    if results:

        results = rerank(
            question=question,
            documents=results,
            top_k=3
        )

        for index, item in enumerate(results, start=1):

            logger.info(
                "Rerank #%s | score=%.4f | file=%s",
                index,
                item["rerank_score"],
                item["metadata"].get(
                    "filename",
                    "Unknown"
                )
            )

        logger.info(
            "Reranked results: %s",
            len(results)
        )


    logger.info(
        "Retrieved results: %s",
        len(results)
    )



    if not results or results[0]["distance"] > 1.5:

        return {

            "question": question,

            "answer":
            "I could not find this information in the knowledge base.",

            "sources": []

        }



    # ==============================
    # 5. Prepare context for LLM
    # ==============================

    knowledge_context = "\n\n".join(

        [

            item["content"]

            for item in results

        ]

    )


    logger.info(
        "Knowledge context length: %s",
        len(knowledge_context)
    )



    # ==============================
    # 6. Generate answer
    # ==============================

    answer = generate_answer(

        question=question,

        context=knowledge_context,

        search_query=search_query

    )



    # ==============================
    # 7. Save conversation
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
    # 8. Conversation summarization
    # ==============================


    history_messages = get_history(

        db=db,

        conversation_id=conversation_id,

        user_id=user_id,

        limit=100
    )


    if history_messages and len(history_messages) >= 10:

        history_text = format_history(
            history_messages
        )

        summary = generate_summary(
            history_text
        )

        save_summary(

            db=db,

            conversation_id=conversation_id,

            summary=summary,

            message_count=len(history_messages)

        )


    # ==============================
    # 9. Update title
    # ==============================

    update_title_if_empty(

        db=db,

        conversation_id=conversation_id,

        title=question[:50]

    )



    # ==============================
    # 9. Format sources
    # ==============================

    sources = format_sources(

        results

    )



    return {

        "question": question,

        "answer": answer,

        "sources": sources

    }