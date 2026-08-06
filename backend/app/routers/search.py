from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.models.user import User

from app.services.search import search_documents


router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get("/")
def search(
    q: str,
    current_user: User = Depends(get_current_user)
):

    results = search_documents(q)


    documents = []


    for doc in results["documents"][0]:

        documents.append({
            "content": doc
        })


    return {
        "query": q,
        "results": documents
    }