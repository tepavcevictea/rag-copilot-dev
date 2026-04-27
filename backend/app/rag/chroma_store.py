from typing import TypedDict

import chromadb
from chromadb.api.models.Collection import Collection

from app.core.config import settings


class ChunkRecord(TypedDict):
    id: str
    source: str
    section: str
    text: str
    score: float


class ChromaStore:
    def __init__(self) -> None:
        client = chromadb.PersistentClient(path=settings.chroma_path)
        self._collection: Collection = client.get_or_create_collection(
            name=settings.chroma_collection
        )

    def add_chunks(self, chunks: list[dict], embeddings: list[list[float]]) -> None:
        ids = [chunk["id"] for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [
            {
                "source": chunk["source"],
                "chunk_id": chunk["id"],
                "section": chunk.get("section", "general"),
            }
            for chunk in chunks
        ]
        self._collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def similarity_search(
        self, query_embedding: list[float], top_k: int = 3
    ) -> list[ChunkRecord]:
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        retrieved: list[ChunkRecord] = []
        for document, metadata, distance in zip(documents, metadatas, distances):
            chunk_id = str(metadata.get("chunk_id", ""))
            source = str(metadata.get("source", "unknown"))
            section = str(metadata.get("section", "general"))
            retrieved.append(
                {
                    "id": chunk_id,
                    "source": source,
                    "section": section,
                    "text": document,
                    "score": float(distance),
                }
            )
        return retrieved
