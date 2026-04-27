from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.rag.pipeline import answer_question, ingest_document

router = APIRouter()


class IngestRequest(BaseModel):
    source: str = Field(..., description="Document name or path")
    text: str = Field(..., description="Document raw text")


class IngestResponse(BaseModel):
    source: str
    chunks_indexed: int


class AskRequest(BaseModel):
    question: str
    top_k: int = 3


class Citation(BaseModel):
    source: str
    chunk_id: str


class AskResponse(BaseModel):
    answer: str
    citations: list[Citation]
    retrieved_chunks: list[dict]


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/ingest", response_model=IngestResponse)
def ingest(request: IngestRequest) -> IngestResponse:
    chunks_indexed = ingest_document(text=request.text, source=request.source)
    return IngestResponse(source=request.source, chunks_indexed=chunks_indexed)


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    result = answer_question(question=request.question, top_k=request.top_k)
    return AskResponse(**result)
