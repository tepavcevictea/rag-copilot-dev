from uuid import uuid4

from openai import OpenAI

from app.core.config import settings
from app.rag.chroma_store import ChunkRecord, ChromaStore

store = ChromaStore()

DOMAIN_KEYWORDS = {
    "refund",
    "invoice",
    "campaign",
    "kyc",
    "incident",
    "sla",
    "p1",
    "p2",
    "ad",
    "support",
    "billing",
    "policy",
    "runbook",
    "retention",
    "pii",
    "attribution",
    "conversion",
}

OFF_TOPIC_KEYWORDS = {
    "weather",
    "temperature",
    "sports",
    "football",
    "movie",
    "recipe",
    "stock tips",
    "bitcoin price",
    "joke",
    "poem",
    "song",
    "write code",
    "python code",
}

SENSITIVE_KEYWORDS = {
    "api key",
    "secret",
    "password",
    "token",
    "private key",
    "ssh key",
    "bypass auth",
    "exploit",
    "sql injection",
}


def _client() -> OpenAI:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")
    return OpenAI(api_key=settings.openai_api_key)


def _chunk_by_size(content: str, max_chars: int, overlap_chars: int) -> list[str]:
    chunks: list[str] = []
    start = 0
    while start < len(content):
        end = min(start + max_chars, len(content))
        chunk = content[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(content):
            break
        start = max(0, end - overlap_chars)
    return chunks


def chunk_text(text: str, source: str) -> list[ChunkRecord]:
    # Header-aware chunking keeps meaningful section context for retrieval.
    lines = text.splitlines()
    sections: list[tuple[str, str]] = []
    current_header = "general"
    current_body: list[str] = []

    for line in lines:
        if line.startswith("#"):
            if current_body:
                sections.append((current_header, "\n".join(current_body).strip()))
                current_body = []
            current_header = line.strip("# ").strip().lower() or "general"
            continue
        current_body.append(line)

    if current_body:
        sections.append((current_header, "\n".join(current_body).strip()))

    chunk_records: list[ChunkRecord] = []
    for section, body in sections:
        if not body:
            continue
        sized_chunks = _chunk_by_size(
            body,
            max_chars=settings.chunk_max_chars,
            overlap_chars=settings.chunk_overlap_chars,
        )
        for piece in sized_chunks:
            chunk_records.append(
                {
                    "id": str(uuid4()),
                    "source": source,
                    "section": section,
                    "text": piece,
                    "score": 0.0,
                }
            )
    return chunk_records


def _enforce_question_policy(question: str) -> tuple[bool, str | None]:
    lowered = question.lower()
    if any(token in lowered for token in SENSITIVE_KEYWORDS):
        return (
            False,
            "I cannot help with sensitive security or credential-related requests.",
        )

    domain_hits = sum(1 for token in DOMAIN_KEYWORDS if token in lowered)
    off_topic_hits = sum(1 for token in OFF_TOPIC_KEYWORDS if token in lowered)

    if domain_hits == 0 and off_topic_hits > 0:
        return (
            False,
            "I only answer questions related to the internal knowledge base domain.",
        )
    if domain_hits == 0:
        return (
            False,
            "This question appears out of scope. Ask about policies, runbooks, support, or product operations.",
        )
    return True, None


def embed_texts(texts: list[str]) -> list[list[float]]:
    client = _client()
    response = client.embeddings.create(
        model=settings.openai_embedding_model,
        input=texts,
    )
    return [item.embedding for item in response.data]


def ingest_document(text: str, source: str) -> int:
    chunks = chunk_text(text=text, source=source)
    embeddings = embed_texts([chunk["text"] for chunk in chunks])
    store.add_chunks(chunks=chunks, embeddings=embeddings)
    return len(chunks)


def _token_set(text: str) -> set[str]:
    cleaned = "".join(ch if ch.isalnum() else " " for ch in text.lower())
    return {token for token in cleaned.split() if len(token) > 2}


def _rerank_chunks(question: str, retrieved: list[ChunkRecord]) -> list[ChunkRecord]:
    query_tokens = _token_set(question)
    scored: list[tuple[float, ChunkRecord]] = []
    for chunk in retrieved:
        chunk_tokens = _token_set(chunk["text"])
        overlap = len(query_tokens.intersection(chunk_tokens))
        lexical_score = overlap / max(len(query_tokens), 1)
        distance_score = max(0.0, 1.0 - (chunk["score"] / 2.0))
        combined = (0.7 * lexical_score) + (0.3 * distance_score)
        scored.append((combined, chunk))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in scored]


def answer_question(question: str, top_k: int = 3) -> dict:
    allowed, policy_message = _enforce_question_policy(question)
    if not allowed:
        return {"answer": policy_message, "citations": [], "retrieved_chunks": []}

    query_embedding = embed_texts([question])[0]
    retrieval_k = max(top_k, settings.retrieval_top_k)
    retrieved = store.similarity_search(query_embedding=query_embedding, top_k=retrieval_k)
    retrieved = [
        chunk
        for chunk in retrieved
        if chunk["score"] <= settings.retrieval_max_distance
    ]
    if retrieved:
        retrieved = _rerank_chunks(question=question, retrieved=retrieved)
        retrieved = retrieved[: settings.final_context_k]

    if not retrieved:
        return {
            "answer": "I do not know based on the indexed documents yet.",
            "citations": [],
            "retrieved_chunks": [],
        }

    context = "\n\n".join(
        f"[source={chunk['source']}] {chunk['text']}" for chunk in retrieved
    )
    prompt = (
        "You are an internal knowledge copilot. Answer the question using only the "
        "provided context. If context is missing, say you do not know. "
        "Do not provide coding help, personal advice, or non-domain content.\n\n"
        f"Question: {question}\n\nContext:\n{context}"
    )
    client = _client()
    completion = client.chat.completions.create(
        model=settings.openai_chat_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    answer = completion.choices[0].message.content or "No answer generated."
    citations = [
        {"source": chunk["source"], "chunk_id": chunk["id"]} for chunk in retrieved
    ]
    return {"answer": answer, "citations": citations, "retrieved_chunks": retrieved}
