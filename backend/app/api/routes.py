from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import BaseModel, Field

from app.agent.orchestrator import agent_ask
from app.agent.policy_editor import (
    approve_change_request,
    create_change_request,
    list_change_requests,
    reject_change_request,
)
from app.auth.security import (
    create_access_token,
    get_current_user,
    require_admin,
    require_employee_or_admin,
)
from app.auth.users import authenticate_user
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


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class MeResponse(BaseModel):
    username: str
    role: str


class PolicyChangeRequestIn(BaseModel):
    instruction: str = Field(
        ...,
        description="Natural language policy change request.",
    )


class PolicyChangeApproveIn(BaseModel):
    change_request_id: str


class PolicyChangeRejectIn(BaseModel):
    change_request_id: str


class PolicyChangeResponse(BaseModel):
    id: str
    status: str
    requested_by: str
    approved_by: str | None = None
    instruction: str
    source: str
    rationale: str
    diff: str
    created_at: str
    approved_at: str | None = None


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/auth/login", response_model=LoginResponse)
def login(request: LoginRequest) -> LoginResponse:
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    token = create_access_token(subject=user["username"], role=user["role"])
    return LoginResponse(access_token=token, role=user["role"])


@router.get("/auth/me", response_model=MeResponse)
def me(user=Depends(get_current_user)) -> MeResponse:
    return MeResponse(username=user["sub"], role=user["role"])


@router.post("/ingest", response_model=IngestResponse)
def ingest(
    request: IngestRequest, _user=Depends(require_admin)
) -> IngestResponse:
    try:
        chunks_indexed = ingest_document(text=request.text, source=request.source)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return IngestResponse(source=request.source, chunks_indexed=chunks_indexed)


@router.post("/ask", response_model=AskResponse)
def ask(
    request: AskRequest, _user=Depends(require_employee_or_admin)
) -> AskResponse:
    try:
        result = answer_question(question=request.question, top_k=request.top_k)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return AskResponse(**result)


@router.post("/agent/ask", response_model=AgentAskResponse)
def agent_endpoint(
    request: AgentAskRequest, _user=Depends(require_employee_or_admin)
) -> AgentAskResponse:
    try:
        result = agent_ask(question=request.question, top_k=request.top_k)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return AgentAskResponse(**result)


@router.post("/policy/change-request", response_model=PolicyChangeResponse)
def policy_change_request(
    request: PolicyChangeRequestIn, user=Depends(require_employee_or_admin)
) -> PolicyChangeResponse:
    try:
        result = create_change_request(
            instruction=request.instruction,
            requested_by=user["sub"],
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return PolicyChangeResponse(**result.model_dump())


@router.post("/policy/change-approve", response_model=PolicyChangeResponse)
def policy_change_approve(
    request: PolicyChangeApproveIn, user=Depends(require_admin)
) -> PolicyChangeResponse:
    try:
        result = approve_change_request(
            change_request_id=request.change_request_id,
            approved_by=user["sub"],
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return PolicyChangeResponse(**result.model_dump())


@router.post("/policy/change-reject", response_model=PolicyChangeResponse)
def policy_change_reject(
    request: PolicyChangeRejectIn, user=Depends(require_admin)
) -> PolicyChangeResponse:
    try:
        result = reject_change_request(
            change_request_id=request.change_request_id,
            approved_by=user["sub"],
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return PolicyChangeResponse(**result.model_dump())


@router.get("/policy/change-requests", response_model=list[PolicyChangeResponse])
def policy_change_requests(_user=Depends(require_employee_or_admin)) -> list[PolicyChangeResponse]:
    try:
        requests = list_change_requests()
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return [PolicyChangeResponse(**item.model_dump()) for item in requests]
