"""
Bonus: benchmark FAISS vs ChromaDB retrieval latency.
Loads all embeddings from the existing ChromaDB collection,
builds a FAISS index, and compares query latency.
"""
import time
import json
import os

import numpy as np
import faiss
import chromadb
from sentence_transformers import SentenceTransformer

import config

client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
collection = client.get_or_create_collection(
    name=config.COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)
embedder = SentenceTransformer(config.EMBEDDING_MODEL)


def load_questions():
    with open("eval/questions.json", "r") as f:
        return json.load(f)


def benchmark():
    # grab all vectors from chromadb
    all_data = collection.get(include=["embeddings", "documents", "metadatas"])
    if not all_data["embeddings"]:
        print("No embeddings found. Run ingest.py first.")
        return

    embeddings = np.array(all_data["embeddings"], dtype=np.float32)
    n_vectors, dim = embeddings.shape
    print(f"Loaded {n_vectors} vectors of dimension {dim} from ChromaDB\n")

    # normalize for cosine similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings_norm = embeddings / norms

    # build FAISS index (flat inner product = cosine on normalized vectors)
    faiss_index = faiss.IndexFlatIP(dim)
    faiss_index.add(embeddings_norm)
    print(f"Built FAISS IndexFlatIP with {faiss_index.ntotal} vectors\n")

    questions = load_questions()
    # only use in-scope questions
    test_queries = [q for q in questions if q["type"] == "in_scope"]

    k = config.TOP_K
    chroma_latencies = []
    faiss_latencies = []

    for q in test_queries:
        query_emb = embedder.encode(q["question"])
        query_emb_np = np.array([query_emb], dtype=np.float32)

        # normalize query
        query_norm = query_emb_np / np.linalg.norm(query_emb_np)

        # benchmark chromadb
        start = time.time()
        collection.query(query_embeddings=query_emb.tolist(), n_results=k)
        chroma_time = (time.time() - start) * 1000
        chroma_latencies.append(chroma_time)

        # benchmark faiss
        start = time.time()
        faiss_index.search(query_norm, k)
        faiss_time = (time.time() - start) * 1000
        faiss_latencies.append(faiss_time)

    # results
    print("=" * 50)
    print(f"LATENCY COMPARISON (k={k}, {len(test_queries)} queries)")
    print("=" * 50)

    for name, lats in [("ChromaDB", chroma_latencies), ("FAISS", faiss_latencies)]:
        p50 = np.percentile(lats, 50)
        p95 = np.percentile(lats, 95)
        mean = np.mean(lats)
        print(f"\n{name}:")
        print(f"  p50:  {p50:.2f} ms")
        print(f"  p95:  {p95:.2f} ms")
        print(f"  mean: {mean:.2f} ms")

    print(f"\nFAISS speedup (p50): {np.percentile(chroma_latencies, 50) / max(np.percentile(faiss_latencies, 50), 0.001):.1f}x")

    # save results
    os.makedirs("eval/results", exist_ok=True)
    results = {
        "n_vectors": n_vectors,
        "dimension": dim,
        "k": k,
        "n_queries": len(test_queries),
        "chromadb": {
            "p50_ms": round(np.percentile(chroma_latencies, 50), 2),
            "p95_ms": round(np.percentile(chroma_latencies, 95), 2),
            "mean_ms": round(np.mean(chroma_latencies), 2),
        },
        "faiss": {
            "p50_ms": round(np.percentile(faiss_latencies, 50), 2),
            "p95_ms": round(np.percentile(faiss_latencies, 95), 2),
            "mean_ms": round(np.mean(faiss_latencies), 2),
        },
        "note": "FAISS uses IndexFlatIP (exact search) on normalized vectors for cosine similarity. "
                "ChromaDB uses HNSW (approximate) internally.",
    }

    with open("eval/results/faiss_benchmark.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to eval/results/faiss_benchmark.json")


if __name__ == "__main__":
    benchmark()
