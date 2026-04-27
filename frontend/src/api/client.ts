export type Citation = {
  source: string;
  chunk_id: string;
};

export type RetrievedChunk = {
  id: string;
  source: string;
  section?: string;
  text: string;
  score: number;
};

export type AskResponse = {
  answer: string;
  citations: Citation[];
  retrieved_chunks: RetrievedChunk[];
};

type IngestResponse = {
  source: string;
  chunks_indexed: number;
};

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  `${window.location.protocol}//${window.location.hostname}:8000`;

export async function askQuestion(
  question: string,
  topK = 8,
): Promise<AskResponse> {
  const response = await fetch(`${API_BASE_URL}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, top_k: topK }),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Ask failed: ${text}`);
  }
  return response.json();
}

export async function ingestText(
  source: string,
  text: string,
): Promise<IngestResponse> {
  const response = await fetch(`${API_BASE_URL}/ingest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source, text }),
  });
  if (!response.ok) {
    const textError = await response.text();
    throw new Error(`Ingest failed: ${textError}`);
  }
  return response.json();
}
