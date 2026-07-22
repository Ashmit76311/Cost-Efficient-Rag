from flask import Flask, request, jsonify

import retriever
import ingest

app = Flask(__name__)


@app.route("/query", methods=["POST"])
def query():
    data = request.json
    question = data.get("question")
    if not question:
        return jsonify({"error": "question is required"}), 400

    k = data.get("k")
    filters = data.get("filters")

    result = retriever.answer(question, k=k, filters=filters)

    sources = []
    for c in result["chunks"]:
        sources.append({
            "source": c["metadata"]["source"],
            "chunk_index": c["metadata"]["chunk_index"],
            "distance": c["distance"],
        })

    return jsonify({
        "answer": result["answer"],
        "sources": sources,
        "metrics": result["metrics"],
    })


@app.route("/ingest", methods=["POST"])
def ingest_endpoint():
    data = request.json
    source = data.get("source")
    if not source:
        return jsonify({"error": "source path is required"}), 400

    total = ingest.ingest_source(source)
    return jsonify({
        "chunks_ingested": total,
        "collection_size": ingest.collection.count(),
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "collection_size": retriever.collection.count(),
        "embedding_model": retriever.config.EMBEDDING_MODEL,
        "llm_model": retriever.config.LLM_MODEL,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
