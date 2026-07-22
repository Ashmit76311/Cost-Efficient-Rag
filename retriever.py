import time
import sys

import chromadb
from sentence_transformers import SentenceTransformer

import config

client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
collection = client.get_or_create_collection(
    name=config.COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)

embedder = SentenceTransformer(config.EMBEDDING_MODEL)

# Setup LLM client based on provider
if config.LLM_PROVIDER == "groq":
    from groq import Groq
    groq_client = Groq(api_key=config.GROQ_API_KEY)
else:
    from google import genai
    genai_client = genai.Client(api_key=config.GOOGLE_API_KEY)


class MockResponse:
    def __init__(self, text, pt, ct, tt):
        self.text = text
        self.usage_metadata = type('obj', (object,), {
            'prompt_token_count': pt,
            'candidates_token_count': ct,
            'total_token_count': tt
        })

def llm_generate(prompt, max_retries=5):
    """Call the configured LLM with retry + backoff for rate limits."""
    for attempt in range(max_retries):
        try:
            if config.LLM_PROVIDER == "groq":
                chat_completion = groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=config.LLM_MODEL,
                )
                text = chat_completion.choices[0].message.content
                pt = chat_completion.usage.prompt_tokens
                ct = chat_completion.usage.completion_tokens
                tt = chat_completion.usage.total_tokens
                return MockResponse(text, pt, ct, tt)
            else:
                response = genai_client.models.generate_content(
                    model=config.LLM_MODEL,
                    contents=prompt,
                )
                return response
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e) or "rate limit" in str(e).lower():
                wait = 10 * (attempt + 1)
                print(f"    [rate limited] waiting {wait}s (attempt {attempt+1}/{max_retries})...")
                time.sleep(wait)
            else:
                raise
    raise Exception("Max retries exceeded for LLM call")


def search(query, k=None, filters=None):
    k = k or config.TOP_K
    query_embedding = embedder.encode(query).tolist()

    kwargs = {
        "query_embeddings": [query_embedding],
        "n_results": k,
        "include": ["documents", "metadatas", "distances"],
    }
    if filters:
        kwargs["where"] = filters

    results = collection.query(**kwargs)

    chunks = []
    for i in range(len(results["ids"][0])):
        chunks.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })

    return chunks


def build_prompt(query, chunks):
    if not chunks:
        return (
            f"Question: {query}\n\n"
            "No relevant context was found. Respond that you don't have enough "
            "information to answer this question."
        )

    context = ""
    for i, chunk in enumerate(chunks):
        context += f"\n[Chunk {i+1}] (Source: {chunk['metadata']['source']})\n{chunk['text']}\n"

    prompt = f"""You are a helpful QA assistant. Answer the question based ONLY on the provided context chunks.
Cite the chunk numbers you used in your answer like [1], [2], etc.
If the context doesn't contain enough information to answer the question, say "I don't have enough context to answer this question." Do NOT make up information.

Context:
{context}

Question: {query}

Answer:"""
    return prompt


def answer(query, k=None, filters=None):
    start = time.time()

    chunks = search(query, k, filters)
    retrieval_time = time.time() - start

    prompt = build_prompt(query, chunks)

    llm_start = time.time()
    response = llm_generate(prompt)
    llm_time = time.time() - llm_start

    total_time = time.time() - start

    usage = response.usage_metadata
    token_info = {
        "prompt_tokens": usage.prompt_token_count,
        "completion_tokens": usage.candidates_token_count,
        "total_tokens": usage.total_token_count,
    }

    print(f"[query] latency={total_time:.2f}s | retrieval={retrieval_time:.2f}s | "
          f"chunks={len(chunks)} | tokens={token_info['total_tokens']}")

    return {
        "answer": response.text,
        "chunks": chunks,
        "metrics": {
            "retrieval_latency_ms": round(retrieval_time * 1000, 2),
            "llm_latency_ms": round(llm_time * 1000, 2),
            "total_latency_ms": round(total_time * 1000, 2),
            "chunks_used": len(chunks),
            "tokens": token_info,
        },
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python retriever.py <your question>")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    result = answer(query)
    print(f"\nAnswer: {result['answer']}")
    print(f"\nSources:")
    for c in result["chunks"]:
        print(f"  - {c['metadata']['source']} (chunk {c['metadata']['chunk_index']}), distance={c['distance']:.4f}")
