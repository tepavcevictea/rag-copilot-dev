from __future__ import annotations

import difflib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from uuid import uuid4

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from app.core.config import settings
from app.rag.pipeline import reindex_document

ChangeStatus = Literal["proposed", "applied", "rejected"]


class PolicyEditPlan(BaseModel):
    source: str = Field(description="Target markdown file name, for example policy_refund_rules.md")
    original_text: str = Field(description="Exact text span that currently exists in the file.")
    replacement_text: str = Field(description="Updated text with policy change applied.")
    rationale: str = Field(description="One sentence summary of the change intent.")


class PolicyChangeRequest(BaseModel):
    id: str
    status: ChangeStatus
    requested_by: str
    approved_by: str | None = None
    instruction: str
    source: str
    rationale: str
    original_text: str
    replacement_text: str
    diff: str
    created_at: str
    approved_at: str | None = None


def _repo_root() -> Path:
    # app/agent/policy_editor.py -> backend/
    return Path(__file__).resolve().parents[2]


def _kb_dir() -> Path:
    return _repo_root() / "docs" / "kb"


def _change_dir() -> Path:
    path = _repo_root() / ".policy_changes"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _load_docs() -> list[tuple[str, str]]:
    kb = _kb_dir()
    if not kb.exists():
        raise RuntimeError(f"KB directory not found: {kb}")
    docs: list[tuple[str, str]] = []
    for md_file in sorted(kb.glob("*.md")):
        docs.append((md_file.name, md_file.read_text(encoding="utf-8")))
    if not docs:
        raise RuntimeError("No policy markdown files found under docs/kb.")
    return docs


def _build_diff(source: str, original_text: str, replacement_text: str) -> str:
    diff_lines = difflib.unified_diff(
        original_text.splitlines(keepends=True),
        replacement_text.splitlines(keepends=True),
        fromfile=f"{source} (before)",
        tofile=f"{source} (after)",
    )
    return "".join(diff_lines) or "(no textual diff)"


def _model() -> ChatOpenAI:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")
    return ChatOpenAI(model=settings.openai_chat_model, temperature=0)


def _plan_from_instruction(instruction: str, docs: list[tuple[str, str]]) -> PolicyEditPlan:
    catalog = []
    for name, content in docs:
        catalog.append(f"FILE: {name}\n---\n{content}\n")
    docs_context = "\n\n".join(catalog)

    llm = _model().with_structured_output(PolicyEditPlan)
    return llm.invoke(
        [
            (
                "system",
                "You are a precise policy editor. Pick exactly one source file from the catalog. "
                "Return an exact existing span from that file in original_text, and return replacement_text "
                "in the same formal policy style. Do not invent file names.",
            ),
            (
                "human",
                f"Instruction:\n{instruction}\n\nDocument catalog:\n{docs_context}",
            ),
        ]
    )


def create_change_request(instruction: str, requested_by: str) -> PolicyChangeRequest:
    docs = _load_docs()
    plan = _plan_from_instruction(instruction=instruction, docs=docs)
    source_path = _kb_dir() / plan.source
    if not source_path.exists():
        raise RuntimeError(f"Model selected missing source file: {plan.source}")

    file_text = source_path.read_text(encoding="utf-8")
    match_count = file_text.count(plan.original_text)
    if match_count == 0:
        raise RuntimeError(
            "Could not locate the proposed original_text in the target file. "
            "Try a more specific instruction."
        )
    if match_count > 1:
        raise RuntimeError(
            "Proposed original_text is ambiguous (appears multiple times). "
            "Try a more specific instruction."
        )
    if plan.original_text.strip() == plan.replacement_text.strip():
        raise RuntimeError(
            "No-op change request: proposed replacement matches existing text."
        )

    diff = _build_diff(
        source=plan.source,
        original_text=plan.original_text,
        replacement_text=plan.replacement_text,
    )
    now = datetime.now(timezone.utc).isoformat()
    request = PolicyChangeRequest(
        id=str(uuid4()),
        status="proposed",
        requested_by=requested_by,
        instruction=instruction,
        source=plan.source,
        rationale=plan.rationale,
        original_text=plan.original_text,
        replacement_text=plan.replacement_text,
        diff=diff,
        created_at=now,
    )
    request_path = _change_dir() / f"{request.id}.json"
    request_path.write_text(request.model_dump_json(indent=2), encoding="utf-8")
    return request


def get_change_request(change_request_id: str) -> PolicyChangeRequest:
    request_path = _change_dir() / f"{change_request_id}.json"
    if not request_path.exists():
        raise RuntimeError("Change request not found.")
    payload = json.loads(request_path.read_text(encoding="utf-8"))
    return PolicyChangeRequest(**payload)


def list_change_requests() -> list[PolicyChangeRequest]:
    requests: list[PolicyChangeRequest] = []
    for request_path in sorted(_change_dir().glob("*.json")):
        payload = json.loads(request_path.read_text(encoding="utf-8"))
        requests.append(PolicyChangeRequest(**payload))
    requests.sort(key=lambda item: item.created_at, reverse=True)
    return requests


def approve_change_request(change_request_id: str, approved_by: str) -> PolicyChangeRequest:
    request = get_change_request(change_request_id=change_request_id)
    if request.status != "proposed":
        raise RuntimeError("Only proposed change requests can be approved.")

    source_path = _kb_dir() / request.source
    if not source_path.exists():
        raise RuntimeError(f"Source document missing: {request.source}")

    current_text = source_path.read_text(encoding="utf-8")
    if request.original_text not in current_text:
        raise RuntimeError(
            "Original text span is no longer present. Reject and create a new proposal."
        )
    updated_text = current_text.replace(
        request.original_text,
        request.replacement_text,
        1,
    )
    source_path.write_text(updated_text, encoding="utf-8")
    reindex_document(text=updated_text, source=request.source)

    request.status = "applied"
    request.approved_by = approved_by
    request.approved_at = datetime.now(timezone.utc).isoformat()
    request_path = _change_dir() / f"{request.id}.json"
    request_path.write_text(request.model_dump_json(indent=2), encoding="utf-8")
    return request


def reject_change_request(change_request_id: str, approved_by: str) -> PolicyChangeRequest:
    request = get_change_request(change_request_id=change_request_id)
    if request.status != "proposed":
        raise RuntimeError("Only proposed change requests can be rejected.")

    request.status = "rejected"
    request.approved_by = approved_by
    request.approved_at = datetime.now(timezone.utc).isoformat()
    request_path = _change_dir() / f"{request.id}.json"
    request_path.write_text(request.model_dump_json(indent=2), encoding="utf-8")
    return request
