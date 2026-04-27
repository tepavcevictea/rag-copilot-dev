# Internal Knowledge Copilot - Beginner-to-Production Textbook

This guide is written for a first-time builder who wants to understand every major concept used in a production-style RAG application.

You will use this document as your "course book" while we implement.

---

## 1) What We Are Building

You are building an **Internal Knowledge Copilot**.

In plain words:
- A user uploads internal documents.
- The system reads and indexes them.
- The user asks a question.
- The system retrieves relevant passages and generates an answer.
- The answer includes citations so the user can verify where it came from.

This is called **RAG** (Retrieval-Augmented Generation).

### Why this project is strong for interviews
- It solves a real business problem (knowledge access).
- It demonstrates backend engineering, AI integration, and cloud deployment.
- It allows you to discuss quality, reliability, cost control, and security.

---

## 2) High-Level Architecture

Main components:
- **Web App (Frontend)**: user interface for uploads and chat.
- **Backend API (FastAPI)**: business logic, ingestion, retrieval, generation.
- **Vector Store (Chroma)**: stores document embeddings for semantic search.
- **LLM API (OpenAI)**: generates final answers.
- **Object/File Storage (Local first, AWS S3 later)**: stores source documents.
- **Container Runtime (Docker)**: packages app consistently.
- **Cloud Platform (AWS)**: hosts app and operations services.

Data flow:
1. User uploads docs -> backend parses/chunks/embeds -> stores vectors in Chroma.
2. User asks question -> backend embeds query -> retrieves top relevant chunks.
3. Backend sends chunks + question to LLM -> returns grounded answer + citations.

---

## 3) Core AI Concepts You Must Know

### 3.1 LLM (Large Language Model)
An LLM is a model trained on large text corpora to predict next tokens.

What it does well:
- language generation
- summarization
- reasoning patterns (with limits)

What it does badly:
- can hallucinate facts
- cannot inherently "know" your private docs unless given context

### 3.2 Embeddings
An embedding is a numeric vector representing text meaning.

Two similar texts -> vectors close together.
This enables **semantic search** instead of keyword-only search.

### 3.3 RAG
RAG = Retrieval + Generation

Without RAG:
- model answers from its training memory (risk of stale/hallucinated outputs)

With RAG:
- system retrieves relevant source chunks first
- model answers using those chunks
- improves factual grounding and controllability

### 3.4 Chunking
Long documents are split into smaller chunks (e.g., 300-1000 tokens).

Why:
- embedding models have token limits
- retrieval quality improves when chunks are focused

Tradeoff:
- chunks too small -> lose context
- chunks too large -> noisy retrieval, higher cost

### 3.5 Top-K Retrieval
Retrieve `k` most relevant chunks (e.g., 3 to 8).

Tradeoff:
- low `k` can miss context
- high `k` increases token cost and may dilute answer quality

---

## 4) What Is an API and Why We Need It

An **API** (Application Programming Interface) is a contract for how software components communicate.

In this project:
- frontend calls backend API endpoints
- backend calls OpenAI API
- backend may call AWS APIs (for storage/logging/infra operations)

### Typical project endpoints
- `POST /ingest` -> upload and index documents
- `POST /ask` -> ask a question and get answer + citations
- `GET /health` -> health check for monitoring and load balancers

API design basics:
- JSON request/response schemas
- status codes (`200`, `400`, `500`)
- error handling and validation

---

## 5) FastAPI (Backend Framework)

**FastAPI** is a modern Python framework for APIs.

Why we use it:
- fast to build
- built-in validation via Pydantic
- async support
- auto-generated docs (`/docs`) from OpenAPI spec

Important FastAPI concepts:
- **Path operation**: endpoint function, e.g. `@app.post("/ask")`
- **Pydantic model**: request/response schema
- **Dependency injection**: clean way to inject auth/db/config
- **Middleware**: add request IDs, logging, CORS policies

Production basics:
- type hints everywhere
- clear exception handling
- request timeouts
- structured logs

---

## 6) Web App Basics (Frontend)

The web app is the user-facing interface.

Core screens/components:
- Upload panel (drag/drop or file input)
- Chat panel (question/answer)
- Citation panel (source chunks, filenames)

Why frontend matters in interviews:
- shows end-to-end ownership
- proves product thinking, not just scripts

Frontend concerns:
- state management for chat history
- handling loading/errors
- displaying citations in a trustworthy way
- basic UX quality (clear, clean, responsive)

---

## 7) Chroma (Vector Database)

**Chroma** is a vector database optimized for embedding storage and similarity search.

What it stores:
- vector embeddings
- chunk text
- metadata (source filename, page, timestamp, tags)

Main operations:
- add documents (with embeddings)
- query nearest neighbors by vector similarity
- filter by metadata (optional)

Why Chroma for this project:
- easy local setup
- fast prototyping
- good for interview demo and architecture explanations

Limitations vs managed vector DBs:
- less enterprise scaling/HA story than Pinecone/Weaviate/Qdrant Cloud

---

## 8) OpenAI API Integration

You will use OpenAI for:
- embeddings (for chunks and user queries)
- chat/completion generation

Key concepts:
- **model selection**: quality vs speed vs cost
- **token usage**: both prompt + output tokens are billed
- **temperature**: creativity/randomness control
- **max_tokens**: output cap, useful for cost control

Production safety:
- never hardcode API key
- use env vars / secret managers
- enforce request limits and retries

---

## 9) Docker and Docker Compose

### 9.1 Docker
Docker packages your app and dependencies into containers.

Benefits:
- "works on my machine" consistency
- reproducible local and cloud behavior

Core concepts:
- **Dockerfile**: image recipe
- **Image**: built artifact
- **Container**: running instance
- **Volume**: persistent data storage
- **Env vars**: runtime configuration

### 9.2 Docker Compose
Compose runs multiple services together (backend, frontend, optional dependencies).

Why needed:
- one command startup for local environment
- easier onboarding/demo

---

## 10) AWS Fundamentals for This Project

You want AWS from day one to learn cloud. Good idea.

Potential AWS services we may use:
- **ECR**: stores Docker images
- **ECS Fargate** (or EC2): runs containers
- **S3**: stores uploaded source docs (later stage)
- **CloudWatch**: logs and metrics
- **IAM**: permissions model
- **VPC**: network boundaries
- **Route 53/ACM** (optional): custom domain + TLS certificate

### 10.1 IAM (Permissions)
IAM controls "who can do what".

Best practices:
- least privilege
- no root account for daily ops
- separate roles for runtime workloads

### 10.2 VPC (Networking)
VPC is your private network in AWS.

Cost-sensitive note:
- NAT Gateway can generate unexpected costs.
- For early prototype, avoid architecture that requires NAT unless needed.

### 10.3 CloudWatch
CloudWatch collects logs and metrics.

Important:
- set log retention (e.g., 3-7 days in dev)
- avoid infinite retention by default

---

## 11) Cost Management (Critical)

You asked for "every button so I do not get charged unexpectedly." Here are the core controls:

### Must configure before running cloud workloads
1. AWS Budget with email alerts (low thresholds: 10, 25, 50 USD).
2. Cost Anomaly Detection monitor.
3. Resource tags (`project`, `env`, `owner`).
4. CloudWatch log retention policy.
5. Single environment only (`dev`).

### Common cost traps
- always-on compute running 24/7
- NAT Gateway hourly + data fees
- load balancers left running
- unbounded logs/snapshots/volumes
- high OpenAI token usage

### Daily checklist
- verify active compute services
- stop nonessential workloads
- check budget dashboard/anomaly alerts

### Weekly checklist
- clean unused images/volumes/snapshots
- review top spend by service
- verify no duplicate environments

---

## 12) Security and Safety Basics

### 12.1 Application Security
- input validation on all endpoints
- file type/size restrictions for uploads
- authentication/authorization (at least basic API key/JWT)

### 12.2 LLM-Specific Security
- prompt injection awareness
- do not expose secrets in prompts/logs
- source-bound answers with citations
- fallback to "I don't know" when evidence is weak

### 12.3 Data Protection
- avoid storing sensitive PII for demo unless required
- encrypt secrets and rotate keys

---

## 13) Quality and Evaluation

A production-feeling AI app needs measurable quality.

Minimum evaluation dimensions:
- retrieval relevance (are top chunks useful?)
- answer groundedness (does answer match retrieved text?)
- citation correctness (can user verify claim?)
- latency (how fast response returns?)
- cost per request

Simple evaluation process:
1. Prepare 20-30 test questions with expected sources.
2. Run queries and log retrieved chunks + outputs.
3. Manually score relevance and faithfulness.
4. Tune chunk size, overlap, top-k, and prompt.

---

## 14) RAG vs Fine-Tuning vs Prompt Engineering

### Prompt Engineering
Best first step:
- cheap, fast, no retraining

### RAG
Best for:
- private or frequently changing knowledge
- need for citations and traceability

### Fine-Tuning (LoRA/QLoRA/PEFT)
Best for:
- behavioral/style adaptation
- domain language patterns

Not best for:
- storing constantly changing factual data (RAG usually better)

Interview framing:
"I chose RAG for knowledge grounding; fine-tuning is a later optimization for behavior/domain style."

---

## 15) Logging, Monitoring, and Reliability

Production systems need observability.

Minimum:
- request ID per call
- structured logs with key fields (latency, status, model, token usage)
- health endpoint for uptime checks
- timeout and retry strategy for external APIs

Reliability patterns:
- graceful degradation on model/API failures
- clear user-facing error messages
- retries with backoff for transient failures

---

## 16) Deployment Strategy You Will Follow

1. Build locally first (functional confidence, low risk).
2. Containerize with Docker.
3. Deploy one `dev` environment to AWS.
4. Validate end-to-end demo.
5. Add cost and reliability guardrails.

This gives:
- real cloud learning
- lower billing risk
- strong interview narrative

---

## 17) Suggested Folder Structure (Target)

```text
backend/
  app/
    main.py
    api/
      routes.py
    rag/
      pipeline.py
      chroma_store.py
    core/
      config.py
frontend/
  src/
    App.tsx
    api/client.ts
infra/
  aws/
    README.md
    cost-guardrails.md
docker-compose.yml
.env.example
```

---

## 18) Terminology Quick Glossary

- **RAG**: retrieve evidence before generating answer
- **Embedding**: numeric semantic representation of text
- **Vector DB**: database optimized for nearest-neighbor search in embedding space
- **Chunk**: small piece of document used for retrieval
- **Top-k**: number of retrieved chunks
- **Latency**: response time
- **Grounded answer**: answer supported by provided sources
- **Hallucination**: plausible but unsupported model output
- **Container**: packaged application runtime
- **Infra as Code**: codified cloud resources and configuration

---

## 19) What "Production-Style" Means for This Project

At this stage, "production-style" means:
- modular architecture
- reproducible deployment
- cost governance
- observability
- security basics
- explainable AI outputs (citations)

It does **not** require:
- massive scale
- enterprise SOC2 setup
- multi-region disaster recovery

This scope is perfect for interview readiness.

---

## 20) Your Learning Path (Order)

Study in this sequence:
1. RAG fundamentals (Sections 3-4)
2. FastAPI and API design (Sections 5 and 4)
3. Chroma internals (Section 7)
4. Docker/Compose (Section 9)
5. AWS fundamentals and cost controls (Sections 10-11)
6. Security + evaluation + reliability (Sections 12-15)

Then build and map each code file to these concepts.

---

## 21) Final Note

This textbook is your conceptual base.
As we implement, we will create:
- a practical step-by-step lab guide,
- architecture diagrams,
- and a demo script for interviews.

If you want, next I will generate **Part 2**:
**"Button-by-button AWS setup manual"** with exact console paths, menu names, and safe defaults for each screen.

---

## 22) Retrieval Tuning We Added

This project now includes a more production-like retrieval layer:

- **Header-aware chunking:** Instead of splitting only by blank lines, the pipeline uses markdown headers (`#`, `##`, `###`) as section boundaries.
- **Chunk size policy:** Chunks are limited by character size with overlap. This reduces context loss while avoiding very long noisy chunks.
- **Larger candidate retrieval:** Initial retrieval uses a larger candidate pool (`retrieval_top_k`) than the final context window.
- **Distance filtering:** Retrieved chunks with weak similarity (distance above threshold) are dropped.
- **Heuristic reranking:** Remaining chunks are reranked with a hybrid score:
  - lexical overlap with the user question
  - vector distance quality
- **Final context reduction:** Only top reranked chunks are sent to generation.

Why this matters:
- Better recall from vector search.
- Better precision before generation.
- Fewer irrelevant chunks in prompt.

---

## 23) Prompt and Abuse Guardrails

RAG systems can be abused if they answer anything outside business scope.
We added policy checks before generation:

- **Out-of-domain refusal:** If a question is not related to internal KB topics, the assistant refuses.
- **Sensitive request refusal:** If prompts ask for secrets, credentials, bypasses, or exploit instructions, the assistant refuses.
- **Prompt grounding rule:** Generation prompt enforces "answer only from provided context."
- **Unknown fallback:** If evidence quality is low, return "I do not know" instead of guessing.

Examples of blocked requests:
- "What is the weather today?"
- "Write me Python code for web scraping."
- "Give me your API key."
- "How can I bypass authentication?"

This is a core production requirement for enterprise AI systems.

---

## 24) Why Retrieval Problems Happened and How We Fixed Them

Observed issue:
- Some questions (for example P1 escalation timing) failed despite data being present.

Why:
- Repeated generic sections across many docs produced semantically similar vectors.
- Retriever returned generic "decision points" chunks instead of specific SLA lines.

Fixes applied:
- section-aware chunking
- wider candidate retrieval
- distance threshold filtering
- reranking and smaller final context

Expected impact:
- Higher chance of retrieving precise numeric or procedural facts.
- Fewer "I do not know" responses when evidence exists.

---

## 25) Configuration Knobs for Bigger Projects

The following settings are now tunable through environment variables:

- `RETRIEVAL_TOP_K`: first-pass candidate count from vector DB
- `FINAL_CONTEXT_K`: final chunk count passed to LLM
- `CHUNK_MAX_CHARS`: max chunk size
- `CHUNK_OVERLAP_CHARS`: overlap between adjacent chunks
- `RETRIEVAL_MAX_DISTANCE`: threshold for filtering weak matches

For larger projects, tune these with a fixed evaluation set and track:
- answer accuracy
- citation correctness
- groundedness
- latency
- token cost

---

## 26) Practical Next Steps

1. Rebuild and redeploy backend with new retrieval pipeline.
2. Re-ingest corpus (old vectors were produced with older chunking logic).
3. Re-run benchmark questions, especially previous failures.
4. Build frontend chat UI for presentable interview demo.
5. Add Redis session memory and request logging.
