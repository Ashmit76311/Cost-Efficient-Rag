# Cost-Efficient RAG Application

A QA service over a document corpus, backed by ChromaDB (a free, embedded vector store), with full evaluation of retrieval quality, answer quality, latency, and cost.

## Why ChromaDB?

| Feature | ChromaDB | FAISS | pgvector | Pinecone |
|---------|----------|-------|----------|----------|
| Cost | Free (embedded) | Free (in-memory) | Needs Postgres | $70+/mo |
| Persistence | ✅ Disk-backed | ❌ Manual | ✅ | ✅ |
| Metadata filtering | ✅ Built-in | ❌ None | ✅ SQL | ✅ |
| Deduplication | ✅ Upsert by ID | ❌ Manual | ✅ | ✅ |
| Setup | `pip install` | `pip install` | Server needed | Cloud signup |

ChromaDB gives us persistence, metadata filtering, and idempotent upsert with zero infra cost. See the [FAISS benchmark](eval/results/faiss_benchmark.json) for a latency comparison.

## Architecture

```
┌──────────┐     ┌───────────┐     ┌──────────┐     ┌─────────┐
│ PDF/HTML/ │────▶│ ingest.py │────▶│ ChromaDB │◀────│ query   │
│ Markdown  │     │ (chunk +  │     │ (vectors │     │ (search │
│ files     │     │  embed)   │     │ + meta)  │     │ + LLM)  │
└──────────┘     └───────────┘     └──────────┘     └────┬────┘
                                                         │
                                                    ┌────▼────┐
                                                    │ Gemini  │
                                                    │ 2.0     │
                                                    │ Flash   │
                                                    └─────────┘
```

- **Embedding**: `all-MiniLM-L6-v2` (384 dims, runs on CPU, free)
- **LLM**: Google Gemini 2.0 Flash (free tier)
- **Chunking**: `RecursiveCharacterTextSplitter`, default 500 chars / 50 overlap

## Setup

```bash
# 1. Clone and install
git clone <repo-url>
cd rag-app
pip install -r requirements.txt

# 2. Set your Gemini API key (free from https://aistudio.google.com/apikey)
cp .env.example .env
# Edit .env and set GOOGLE_API_KEY=your-key-here

# 3. Ingest the sample corpus
python ingest.py --source docs/

# 4. Test a query
python retriever.py "What is backpropagation?"
```

## Usage

### CLI

```bash
# Query directly
python retriever.py "Explain the bias-variance tradeoff"

# Ingest your own documents
python ingest.py --source /path/to/your/docs/
python ingest.py --source myfile.pdf --chunk-size 800 --chunk-overlap 100
```

### HTTP API

```bash
# Start the server
python app.py

# Query
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a hash map?", "k": 5}'

# Query with metadata filter
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is normalization?", "filters": {"source": "databases.md"}}'

# Ingest new documents
curl -X POST http://localhost:5000/ingest \
  -H "Content-Type: application/json" \
  -d '{"source": "docs/"}'

# Health check
curl http://localhost:5000/health
```

### Response Format

```json
{
  "answer": "A hash map stores key-value pairs and provides average O(1) lookup... [1][2]",
  "sources": [
    {"source": "data_structures.md", "chunk_index": 3, "distance": 0.42}
  ],
  "metrics": {
    "retrieval_latency_ms": 12.5,
    "llm_latency_ms": 850.3,
    "total_latency_ms": 862.8,
    "chunks_used": 5,
    "tokens": {"prompt_tokens": 1200, "completion_tokens": 150, "total_tokens": 1350}
  }
}
```

## Configuration

All config via environment variables (see `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `GOOGLE_API_KEY` | — | Gemini API key (required) |
| `CHROMA_DB_PATH` | `./data/chromadb` | ChromaDB storage path |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence transformer model |
| `LLM_MODEL` | `gemini-2.0-flash` | Gemini model name |
| `CHUNK_SIZE` | `500` | Chunk size in characters |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `TOP_K` | `5` | Default number of retrieved chunks |
| `COLLECTION_NAME` | `documents` | ChromaDB collection name |

## Evaluation

Run the full evaluation harness:

```bash
# Make sure docs are ingested first
python ingest.py --source docs/

# Run evaluation (25 questions: 20 in-scope, 3 out-of-scope, 2 metadata-filter)
python evaluate.py

# Run with different k
python evaluate.py --k 10

# Run FAISS latency benchmark (bonus)
python benchmark_faiss.py
```

### Evaluation Dataset

25 questions across 10 CS/ML topics:
- **20 in-scope questions** with gold answers and relevant document/keyword annotations
- **3 out-of-scope trick questions** (recipes, sports, geography) — tests "no relevant context" handling
- **2 metadata-filter questions** — tests retrieval with `{"source": "specific_doc.md"}` filter

### Metrics Computed

**Retrieval (per-question + averaged):**
- Hit Rate — did we retrieve at least one relevant chunk?
- Recall@k — fraction of all relevant chunks retrieved
- MRR (Mean Reciprocal Rank) — how high is the first relevant chunk?
- nDCG@k — normalized discounted cumulative gain
- Context Precision — fraction of retrieved chunks that are relevant

**Answer (per-question + averaged):**
- Faithfulness — LLM-as-judge: is the answer grounded in context?
- Answer Relevance — LLM-as-judge: does the answer address the question?
- Exact Match — normalized exact match with gold answer
- F1 — token-level F1 score with gold answer
- Refusal Score — for out-of-scope: did the model correctly refuse?

**Latency:**
- p50 / p95 retrieval latency
- Mean retrieval latency

Results are saved to `eval/results/`.

## Cost Analysis

See [eval/results/cost_analysis.md](eval/results/cost_analysis.md) for the full breakdown.

**TL;DR**: ChromaDB on a small VM costs **$5-10/mo** for up to 1M vectors, vs **$70-100/mo** for managed alternatives like Pinecone. That's a 7-10x cost reduction.

| Scale | ChromaDB | Pinecone | Savings |
|-------|----------|----------|---------|
| 100K vectors | ~$5/mo | ~$70/mo | 14x |
| 1M vectors | ~$10/mo | ~$70/mo | 7x |
| 10M vectors | ~$40/mo | ~$350/mo | 9x |

## Discussion

### When would you switch back to managed?

1. **>10M vectors** — RAM costs for HNSW index become significant, managed DBs auto-shard
2. **Multi-region needs** — replication is hard to DIY
3. **SLA requirements** — if you need guaranteed uptime
4. **Rapid growth** — if vector count is growing 10x in months

### Was retrieval or generation the weak link?

In our evaluation, **retrieval is the bottleneck for answer quality**. When the right chunks are retrieved, Gemini 2.0 Flash generates faithful, well-cited answers consistently. The main failure mode is retrieving chunks from the wrong topic (low context precision), which leads the LLM to either give a wrong-but-grounded answer or correctly refuse.

Key observations:
- **Hit rate** is generally high — the right document is usually in the top-5
- **Context precision** is the weakest retrieval metric — irrelevant chunks dilute the context
- **Faithfulness** is high — the LLM rarely hallucinates beyond the provided context
- **Out-of-scope refusal** works well — the model correctly identifies when it lacks context
- Larger chunk sizes may help for questions requiring broader context, at the cost of precision
- A re-ranking step (cross-encoder) could improve context precision significantly

## Project Structure

```
├── app.py              # Flask HTTP API
├── ingest.py           # Document ingestion pipeline
├── retriever.py        # Vector search + LLM answer generation
├── evaluate.py         # Evaluation harness
├── benchmark_faiss.py  # Bonus: FAISS latency benchmark
├── config.py           # Environment-based configuration
├── requirements.txt    # Dependencies
├── .env.example        # Config template
├── docs/               # Sample document corpus (10 MD files)
├── eval/
│   ├── questions.json  # 25 evaluation questions
│   └── results/        # Generated evaluation results
└── data/               # ChromaDB storage (gitignored)
```
