from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "dev"
    openai_api_key: str | None = None
    openai_chat_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    chroma_path: str = "./.chroma"
    chroma_collection: str = "rag_copilot_kb"
    retrieval_top_k: int = 8
    final_context_k: int = 4
    chunk_max_chars: int = 900
    chunk_overlap_chars: int = 120
    retrieval_max_distance: float = 1.35

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
