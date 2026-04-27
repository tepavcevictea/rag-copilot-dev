from typing import Literal, TypedDict

from app.rag.pipeline import answer_question


class AgentResult(TypedDict):
    mode: Literal["refusal", "tool_rag_lookup", "tool_policy_summary"]
    answer: str
    citations: list[dict]
    retrieved_chunks: list[dict]


def _intent_route(question: str) -> Literal["rag_lookup", "policy_summary"]:
    lowered = question.lower()
    summary_signals = ("summarize", "summary", "give me overview", "brief")
    if any(signal in lowered for signal in summary_signals):
        return "policy_summary"
    return "rag_lookup"


def _policy_summary(question: str, top_k: int) -> AgentResult:
    rag_result = answer_question(question=question, top_k=top_k)
    summary_prefix = "Policy summary:\n"
    return {
        "mode": "tool_policy_summary",
        "answer": f"{summary_prefix}{rag_result['answer']}",
        "citations": rag_result["citations"],
        "retrieved_chunks": rag_result["retrieved_chunks"],
    }


def agent_ask(question: str, top_k: int = 8) -> AgentResult:
    """
    Minimal tool-using agent.

    - Routes intent.
    - Uses RAG as a tool.
    - Preserves safety behavior from the RAG pipeline.
    """
    route = _intent_route(question)
    if route == "policy_summary":
        return _policy_summary(question=question, top_k=top_k)

    rag_result = answer_question(question=question, top_k=top_k)
    refusal_markers = (
        "I cannot help with sensitive security",
        "I only answer questions related",
        "This question appears out of scope",
    )
    is_refusal = any(marker in rag_result["answer"] for marker in refusal_markers)

    return {
        "mode": "refusal" if is_refusal else "tool_rag_lookup",
        "answer": rag_result["answer"],
        "citations": rag_result["citations"],
        "retrieved_chunks": rag_result["retrieved_chunks"],
    }
