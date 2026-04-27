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
  mode?: string;
  answer: string;
  citations: Citation[];
  retrieved_chunks: RetrievedChunk[];
};

export type LoginResponse = {
  access_token: string;
  token_type: string;
  role: "employee" | "admin";
};

export type MeResponse = {
  username: string;
  role: "employee" | "admin";
};

type IngestResponse = {
  source: string;
  chunks_indexed: number;
};

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  `${window.location.protocol}//${window.location.hostname}:8000`;

function authHeaders(token: string) {
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
}

export async function login(
  username: string,
  password: string,
): Promise<LoginResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Login failed: ${text}`);
  }
  return response.json();
}

export async function getMe(token: string): Promise<MeResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/me`, {
    method: "GET",
    headers: authHeaders(token),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Auth check failed: ${text}`);
  }
  return response.json();
}

export async function askQuestion(
  token: string,
  question: string,
  topK = 8,
  mode: "rag" | "agent" = "rag",
): Promise<AskResponse> {
  const endpoint = mode === "agent" ? "/agent/ask" : "/ask";
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify({ question, top_k: topK }),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Ask failed: ${text}`);
  }
  return response.json();
}

export async function ingestText(
  token: string,
  source: string,
  text: string,
): Promise<IngestResponse> {
  const response = await fetch(`${API_BASE_URL}/ingest`, {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify({ source, text }),
  });
  if (!response.ok) {
    const textError = await response.text();
    throw new Error(`Ingest failed: ${textError}`);
  }
  return response.json();
}
