from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="RAG Copilot API",
    version="0.1.0",
    description="Internal Knowledge Copilot backend API.",
)

app.include_router(router)
