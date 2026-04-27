from uuid import uuid4

from openai import OpenAI

from app.core.config import settings
from app.rag.chroma_store import ChunkRecord, ChromaStore

store = ChromaStore()


def _client() -> OpenAI:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")
    return OpenAI(api_key=settings.openai_api_key)


def chunk_text(text: str, source: str) -> list[ChunkRecord]:
    # Step-1: simple paragraph chunking for fast iteration.
    raw_chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    return [
        {"id": str(uuid4()), "source": source, "text": chunk, "score": 0.0}
        for chunk in raw_chunks
    ]


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


def answer_question(question: str, top_k: int = 3) -> dict:
    query_embedding = embed_texts([question])[0]
    retrieved = store.similarity_search(query_embedding=query_embedding, top_k=top_k)
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
        "provided context. If context is missing, say you do not know.\n\n"
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
