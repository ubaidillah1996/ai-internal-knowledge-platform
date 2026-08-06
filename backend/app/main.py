from fastapi import FastAPI
from app.routers import auth
from app.routers import users
from app.routers import documents
from app.routers import search
from app.routers import ask
from app.routers import conversations


app = FastAPI(
    title="AI Internal Knowledge Platform"
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(documents.router)
app.include_router(search.router)
app.include_router(
    ask.router
)
app.include_router(
    conversations.router
)

@app.get("/")
def root():
    return {
        "message": "AI Knowledge Platform API Running"
    }