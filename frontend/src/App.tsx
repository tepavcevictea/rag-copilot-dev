import { FormEvent, useState } from "react";

import {
  AskResponse,
  RetrievedChunk,
  askQuestion,
  ingestText,
} from "./api/client";

type ChatTurn = {
  question: string;
  response: AskResponse;
};

function App() {
  const [question, setQuestion] = useState("");
  const [topK, setTopK] = useState(8);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showChunks, setShowChunks] = useState(false);
  const [history, setHistory] = useState<ChatTurn[]>([]);

  const [sourceName, setSourceName] = useState("manual_note.md");
  const [sourceText, setSourceText] = useState("");
  const [ingestStatus, setIngestStatus] = useState("");

  const onAsk = async (event: FormEvent) => {
    event.preventDefault();
    const trimmed = question.trim();
    if (!trimmed) {
      return;
    }
    setLoading(true);
    setError("");
    try {
      const response = await askQuestion(trimmed, topK);
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
      const response = await ingestText(sourceName.trim(), sourceText.trim());
      setIngestStatus(
        `Indexed ${response.chunks_indexed} chunk(s) from ${response.source}.`,
      );
    } catch (err) {
      setIngestStatus(err instanceof Error ? err.message : "Ingest failed.");
    }
  };

  return (
    <main className="app-shell">
      <header className="app-header">
        <h1>RAG Copilot</h1>
        <p>
          Grounded internal knowledge assistant with citations and retrieval
          transparency.
        </p>
      </header>

      <section className="panel">
        <h2>Quick Ingest</h2>
        <form className="stack" onSubmit={onIngest}>
          <label>
            Source name
            <input
              value={sourceName}
              onChange={(event) => setSourceName(event.target.value)}
              placeholder="policy_note.md"
            />
          </label>
          <label>
            Source text
            <textarea
              value={sourceText}
              onChange={(event) => setSourceText(event.target.value)}
              rows={5}
              placeholder="Paste document text to index into Chroma."
            />
          </label>
          <button type="submit">Ingest Text</button>
        </form>
        {ingestStatus ? <p className="status">{ingestStatus}</p> : null}
      </section>

      <section className="panel">
        <h2>Ask</h2>
        <form className="stack" onSubmit={onAsk}>
          <label>
            Question
            <textarea
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              rows={3}
              placeholder="Ask about policy, runbook, support, or product behavior."
            />
          </label>
          <label>
            Top K
            <input
              type="number"
              min={1}
              max={15}
              value={topK}
              onChange={(event) => setTopK(Number(event.target.value))}
            />
          </label>
          <div className="row">
            <button type="submit" disabled={loading}>
              {loading ? "Asking..." : "Ask Question"}
            </button>
            <label className="inline">
              <input
                type="checkbox"
                checked={showChunks}
                onChange={(event) => setShowChunks(event.target.checked)}
              />
              Show retrieved chunks
            </label>
          </div>
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
    </main>
  );
}

export default App;
