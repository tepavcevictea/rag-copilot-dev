from typing import TypedDict


class ChunkRecord(TypedDict):
    id: str
    source: str
    text: str


class InMemoryChromaStore:
    """
    Step-1 stand-in for Chroma.

    We keep this interface intentionally small so we can swap in a real
    Chroma client next without changing API route logic.
    """

    def __init__(self) -> None:
        self._chunks: list[ChunkRecord] = []

    def add_chunks(self, chunks: list[ChunkRecord]) -> None:
        self._chunks.extend(chunks)

    def similarity_search(self, query: str, top_k: int = 3) -> list[ChunkRecord]:
        query_terms = {term.strip().lower() for term in query.split() if term.strip()}
        scored: list[tuple[int, ChunkRecord]] = []
        for chunk in self._chunks:
            text_terms = set(chunk["text"].lower().split())
            score = len(query_terms.intersection(text_terms))
            scored.append((score, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [record for score, record in scored[:top_k] if score > 0]
