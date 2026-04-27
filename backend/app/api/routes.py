from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel, Field

from app.agent.orchestrator import agent_ask
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


class AgentAskRequest(BaseModel):
    question: str
    top_k: int = 8


class AgentAskResponse(BaseModel):
    mode: str
    answer: str
    citations: list[Citation]
    retrieved_chunks: list[dict]


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/ingest", response_model=IngestResponse)
def ingest(request: IngestRequest) -> IngestResponse:
    try:
        chunks_indexed = ingest_document(text=request.text, source=request.source)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return IngestResponse(source=request.source, chunks_indexed=chunks_indexed)


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    try:
        result = answer_question(question=request.question, top_k=request.top_k)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return AskResponse(**result)


@router.post("/agent/ask", response_model=AgentAskResponse)
def agent_endpoint(request: AgentAskRequest) -> AgentAskResponse:
    try:
        result = agent_ask(question=request.question, top_k=request.top_k)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return AgentAskResponse(**result)
