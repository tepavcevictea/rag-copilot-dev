from uuid import uuid4

from app.rag.chroma_store import ChunkRecord, InMemoryChromaStore

store = InMemoryChromaStore()


def chunk_text(text: str, source: str) -> list[ChunkRecord]:
    # Step-1: simple paragraph chunking for fast iteration.
    raw_chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    return [
        {"id": str(uuid4()), "source": source, "text": chunk}
        for chunk in raw_chunks
    ]


def ingest_document(text: str, source: str) -> int:
    chunks = chunk_text(text=text, source=source)
    store.add_chunks(chunks)
    return len(chunks)


def answer_question(question: str, top_k: int = 3) -> dict:
    retrieved = store.similarity_search(question, top_k=top_k)
    if not retrieved:
        return {
            "answer": "I do not know based on the indexed documents yet.",
            "citations": [],
            "retrieved_chunks": [],
        }

    answer = " ".join(chunk["text"] for chunk in retrieved[:2])
    citations = [
        {"source": chunk["source"], "chunk_id": chunk["id"]} for chunk in retrieved
    ]
    return {"answer": answer, "citations": citations, "retrieved_chunks": retrieved}
