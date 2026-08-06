from fastapi import FastAPI
from app.routers import auth
from app.routers import users
from app.routers import documents
from app.routers import search
from app.routers import ask
from app.routers import conversations
from app.middleware.error_handler import app_exception_handler
from app.core.exceptions import AppException
from app.core.logger import setup_logger




app = FastAPI(
    title="AI Internal Knowledge Platform"
)

logger = setup_logger()

logger.info(
    "AI Knowledge Platform started"
)

app.add_exception_handler(
    AppException,
    app_exception_handler
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