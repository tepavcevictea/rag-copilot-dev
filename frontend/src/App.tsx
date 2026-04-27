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
  const [showIngest, setShowIngest] = useState(false);

  const starterQuestions = [
    "What is the refund request time window?",
    "When is KYC required?",
    "How fast must we escalate a P1 incident?",
    "What is the default attribution window?",
  ];

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
          Ask policy, runbook, support, and product questions. Every answer is
          grounded with citations.
        </p>
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
    </main>
  );
}

export default App;
