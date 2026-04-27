import { FormEvent, useEffect, useState } from "react";

import {
  AskResponse,
  MeResponse,
  RetrievedChunk,
  getMe,
  askQuestion,
  ingestText,
  login,
} from "./api/client";

type ChatTurn = {
  question: string;
  response: AskResponse;
};

function App() {
  const [token, setToken] = useState<string>(
    () => localStorage.getItem("rag_token") ?? "",
  );
  const [me, setMe] = useState<MeResponse | null>(null);
  const [authError, setAuthError] = useState("");
  const [authLoading, setAuthLoading] = useState(false);
  const [loginUsername, setLoginUsername] = useState("employee_demo");
  const [loginPassword, setLoginPassword] = useState("employee123");

  const [question, setQuestion] = useState("");
  const [topK, setTopK] = useState(8);
  const [mode, setMode] = useState<"rag" | "agent">("agent");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showChunks, setShowChunks] = useState(false);
  const [history, setHistory] = useState<ChatTurn[]>([]);

  const [sourceName, setSourceName] = useState("manual_note.md");
  const [sourceText, setSourceText] = useState("");
  const [ingestStatus, setIngestStatus] = useState("");
  const [showIngest, setShowIngest] = useState(false);

  const starterQuestions = [
    "What is the refund request time window?",
    "When is KYC required?",
    "How fast must we escalate a P1 incident?",
    "What is the default attribution window?",
  ];

  const hydrateMe = async (jwt: string) => {
    try {
      const profile = await getMe(jwt);
      setMe(profile);
    } catch {
      localStorage.removeItem("rag_token");
      setToken("");
      setMe(null);
    }
  };

  useEffect(() => {
    if (!token || me) {
      return;
    }
    setAuthLoading(true);
    hydrateMe(token).finally(() => setAuthLoading(false));
  }, [token, me]);

  const onLogin = async (event: FormEvent) => {
    event.preventDefault();
    setAuthError("");
    setAuthLoading(true);
    try {
      const response = await login(loginUsername, loginPassword);
      setToken(response.access_token);
      localStorage.setItem("rag_token", response.access_token);
      await hydrateMe(response.access_token);
    } catch (err) {
      setAuthError(err instanceof Error ? err.message : "Login failed.");
    } finally {
      setAuthLoading(false);
    }
  };

  const onLogout = () => {
    localStorage.removeItem("rag_token");
    setToken("");
    setMe(null);
    setHistory([]);
  };

  const onAsk = async (event: FormEvent) => {
    event.preventDefault();
    const trimmed = question.trim();
    if (!trimmed) {
      return;
    }
    setLoading(true);
    setError("");
    try {
      if (!token) {
        throw new Error("Login required.");
      }
      const response = await askQuestion(token, trimmed, topK, mode);
      setHistory((prev) => [{ question: trimmed, response }, ...prev]);
      setQuestion("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  const onIngest = async (event: FormEvent) => {
    event.preventDefault();
    if (!sourceName.trim() || !sourceText.trim()) {
      setIngestStatus("Source name and source text are required.");
      return;
    }
    setIngestStatus("Ingesting...");
    try {
      if (!token) {
        throw new Error("Login required.");
      }
      const response = await ingestText(
        token,
        sourceName.trim(),
        sourceText.trim(),
      );
      setIngestStatus(
        `Indexed ${response.chunks_indexed} chunk(s) from ${response.source}.`,
      );
    } catch (err) {
      setIngestStatus(err instanceof Error ? err.message : "Ingest failed.");
    }
  };

  if (!token || !me) {
    return (
      <main className="app-shell">
        <section className="panel">
          <h1>RAG Copilot Login</h1>
          <p className="muted">
            Use demo accounts: <code>employee_demo / employee123</code> or{" "}
            <code>admin_demo / admin123</code>.
          </p>
          <form className="stack" onSubmit={onLogin}>
            <label>
              Username
              <input
                value={loginUsername}
                onChange={(event) => setLoginUsername(event.target.value)}
              />
            </label>
            <label>
              Password
              <input
                type="password"
                value={loginPassword}
                onChange={(event) => setLoginPassword(event.target.value)}
              />
            </label>
            <button type="submit" disabled={authLoading}>
              {authLoading ? "Signing in..." : "Sign in"}
            </button>
          </form>
          {authError ? <p className="error">{authError}</p> : null}
        </section>
      </main>
    );
  }

  return (
    <main className="app-shell">
      <header className="app-header">
        <h1>RAG Copilot</h1>
        <p>
          Ask policy, runbook, support, and product questions. Every answer is
          grounded with citations.
        </p>
        <div className="row between">
          <p className="muted">
            Signed in as <strong>{me.username}</strong> ({me.role})
          </p>
          <button type="button" className="ghost" onClick={onLogout}>
            Logout
          </button>
        </div>
      </header>

      <section className="panel">
        <h2>Ask a Question</h2>
        <p className="muted">
          Type a business question, then click <strong>Ask Question</strong>.
          The assistant will answer from indexed internal documents and show
          citations.
        </p>
        <div className="chips">
          {starterQuestions.map((starter) => (
            <button
              key={starter}
              type="button"
              className="chip"
              onClick={() => setQuestion(starter)}
            >
              {starter}
            </button>
          ))}
        </div>
        <form className="stack" onSubmit={onAsk}>
          <label>
            Question
            <textarea
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              rows={3}
              placeholder="Example: Can we refund a dispute after 45 days if fraud review is active?"
            />
          </label>
          <div className="row">
            <button type="submit" disabled={loading}>
              {loading ? "Asking..." : "Ask Question"}
            </button>
            <label>
              Mode
              <select
                value={mode}
                onChange={(event) => setMode(event.target.value as "rag" | "agent")}
              >
                <option value="agent">Agent</option>
                <option value="rag">RAG</option>
              </select>
            </label>
          </div>
          <details className="advanced">
            <summary>Advanced options</summary>
            <div className="advanced-grid">
              <label>
                Retrieval depth (Top K)
                <input
                  type="number"
                  min={1}
                  max={15}
                  value={topK}
                  onChange={(event) => setTopK(Number(event.target.value))}
                />
              </label>
              <label className="inline">
                <input
                  type="checkbox"
                  checked={showChunks}
                  onChange={(event) => setShowChunks(event.target.checked)}
                />
                Show retrieved chunks for debugging
              </label>
            </div>
          </details>
        </form>
        {error ? <p className="error">{error}</p> : null}
      </section>

      <section className="panel">
        <h2>Chat History</h2>
        {history.length === 0 ? (
          <p className="muted">No queries yet.</p>
        ) : (
          history.map((turn, index) => (
            <article key={index} className="turn">
              <h3>Q: {turn.question}</h3>
              <p>{turn.response.answer}</p>
              <div>
                <strong>Citations:</strong>
                <ul>
                  {turn.response.citations.map((citation) => (
                    <li key={citation.chunk_id}>
                      {citation.source} ({citation.chunk_id.slice(0, 8)}...)
                    </li>
                  ))}
                </ul>
              </div>
              {showChunks ? (
                <div>
                  <strong>Retrieved chunks:</strong>
                  <ul>
                    {turn.response.retrieved_chunks.map(
                      (chunk: RetrievedChunk) => (
                        <li key={chunk.id}>
                          <p>
                            <strong>{chunk.source}</strong> | section=
                            {chunk.section ?? "general"} | score=
                            {chunk.score.toFixed(3)}
                          </p>
                          <p className="chunk-text">{chunk.text}</p>
                        </li>
                      ),
                    )}
                  </ul>
                </div>
              ) : null}
            </article>
          ))
        )}
      </section>

      {me.role === "admin" ? (
        <section className="panel">
        <div className="row between">
          <h2>Document Import (Admin)</h2>
          <button
            type="button"
            className="ghost"
            onClick={() => setShowIngest((prev) => !prev)}
          >
            {showIngest ? "Hide" : "Show"}
          </button>
        </div>
        <p className="muted">
          Use this only when you want to add a new text document into the
          knowledge base.
        </p>
        {showIngest ? (
          <form className="stack" onSubmit={onIngest}>
            <label>
              Document name
              <input
                value={sourceName}
                onChange={(event) => setSourceName(event.target.value)}
                placeholder="policy_new_rule.md"
              />
            </label>
            <label>
              Document content
              <textarea
                value={sourceText}
                onChange={(event) => setSourceText(event.target.value)}
                rows={6}
                placeholder="Paste the document text you want indexed."
              />
            </label>
            <button type="submit">Import Document</button>
          </form>
        ) : null}
        {ingestStatus ? <p className="status">{ingestStatus}</p> : null}
      </section>
      ) : null}
    </main>
  );
}

export default App;
