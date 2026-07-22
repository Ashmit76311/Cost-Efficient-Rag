import json
import time
import os
import math
from pathlib import Path
from collections import Counter

import numpy as np

import config
import retriever


def load_questions():
    with open("eval/questions.json", "r") as f:
        return json.load(f)


# ---- helpers to figure out which chunks are relevant ----

def get_relevant_chunk_ids(question):
    """Get all chunk IDs from the collection that match the question's ground truth."""
    if not question.get("relevant_doc"):
        return []

    results = retriever.collection.get(
        where={"source": question["relevant_doc"]},
        include=["documents"],
    )

    relevant_ids = []
    keywords = question.get("relevant_keywords", [])

    for i, doc_text in enumerate(results["documents"]):
        if not keywords:
            relevant_ids.append(results["ids"][i])
        else:
            text_lower = doc_text.lower()
            if any(kw.lower() in text_lower for kw in keywords):
                relevant_ids.append(results["ids"][i])

    return relevant_ids


# ---- retrieval metrics ----

def calc_hit_rate(retrieved_ids, relevant_ids):
    if not relevant_ids:
        return 0.0
    return 1.0 if any(rid in set(relevant_ids) for rid in retrieved_ids) else 0.0


def calc_recall_at_k(retrieved_ids, relevant_ids):
    if not relevant_ids:
        return 0.0
    hits = len(set(retrieved_ids) & set(relevant_ids))
    return hits / len(relevant_ids)


def calc_mrr(retrieved_ids, relevant_ids):
    relevant_set = set(relevant_ids)
    for i, rid in enumerate(retrieved_ids):
        if rid in relevant_set:
            return 1.0 / (i + 1)
    return 0.0


def calc_ndcg_at_k(retrieved_ids, relevant_ids):
    relevant_set = set(relevant_ids)

    dcg = 0.0
    for i, rid in enumerate(retrieved_ids):
        if rid in relevant_set:
            dcg += 1.0 / math.log2(i + 2)

    ideal_hits = min(len(relevant_ids), len(retrieved_ids))
    idcg = sum(1.0 / math.log2(i + 2) for i in range(ideal_hits))

    return dcg / idcg if idcg > 0 else 0.0


def calc_context_precision(retrieved_ids, relevant_ids):
    if not retrieved_ids:
        return 0.0
    relevant_set = set(relevant_ids)
    hits = sum(1 for rid in retrieved_ids if rid in relevant_set)
    return hits / len(retrieved_ids)


# ---- answer metrics ----

def calc_exact_match(predicted, gold):
    def normalize(s):
        return " ".join(s.lower().strip().split())
    return 1.0 if normalize(predicted) == normalize(gold) else 0.0


def calc_f1(predicted, gold):
    pred_tokens = predicted.lower().split()
    gold_tokens = gold.lower().split()

    pred_counts = Counter(pred_tokens)
    gold_counts = Counter(gold_tokens)

    common = sum((pred_counts & gold_counts).values())
    if common == 0:
        return 0.0

    precision = common / len(pred_tokens)
    recall = common / len(gold_tokens)
    return 2 * precision * recall / (precision + recall)


def llm_judge(prompt):
    """Ask the LLM to rate something 0-1. Returns the float score."""
    try:
        response = retriever.llm_generate(prompt)
        score = float(response.text.strip().split()[0])
        return min(max(score, 0.0), 1.0)
    except Exception as e:
        print(f"    [judge error] {e}, defaulting to 0.5")
        return 0.5


def judge_faithfulness(answer_text, chunks):
    context = "\n---\n".join([c["text"] for c in chunks])
    prompt = f"""Rate the faithfulness of this answer to the given context.
A faithful answer only contains information supported by the context.

Context:
{context}

Answer:
{answer_text}

Score from 0.0 to 1.0 (1.0 = fully faithful, 0.0 = hallucinated).
Respond with ONLY a decimal number."""
    return llm_judge(prompt)


def judge_relevance(answer_text, question):
    prompt = f"""Rate how well this answer addresses the question.

Question: {question}

Answer: {answer_text}

Score from 0.0 to 1.0 (1.0 = perfectly answers the question, 0.0 = irrelevant).
Respond with ONLY a decimal number."""
    return llm_judge(prompt)


def judge_refusal(answer_text):
    """For out-of-scope questions: did the model correctly refuse to answer?"""
    prompt = f"""Does this response correctly indicate that it cannot answer or doesn't have enough context?
It should NOT provide a made-up answer.

Response:
{answer_text}

Score from 0.0 to 1.0 (1.0 = correctly refuses, 0.0 = hallucinates an answer).
Respond with ONLY a decimal number."""
    return llm_judge(prompt)


# ---- main evaluation loop ----

def run_evaluation(k=None):
    k = k or config.TOP_K
    questions = load_questions()

    print(f"Running evaluation with k={k} on {len(questions)} questions...\n")

    retrieval_results = []
    answer_results = []
    latencies = []

    for q in questions:
        print(f"  Q{q['id']}: {q['question'][:60]}...")

        filters = q.get("filters")
        result = retriever.answer(q["question"], k=k, filters=filters)
        latencies.append(result["metrics"]["retrieval_latency_ms"])

        retrieved_ids = [c["id"] for c in result["chunks"]]

        # --- retrieval metrics (skip for out-of-scope) ---
        if q["type"] != "out_of_scope":
            relevant_ids = get_relevant_chunk_ids(q)

            ret_metrics = {
                "question_id": q["id"],
                "type": q["type"],
                "hit_rate": calc_hit_rate(retrieved_ids, relevant_ids),
                "recall_at_k": calc_recall_at_k(retrieved_ids, relevant_ids),
                "mrr": calc_mrr(retrieved_ids, relevant_ids),
                "ndcg_at_k": calc_ndcg_at_k(retrieved_ids, relevant_ids),
                "context_precision": calc_context_precision(retrieved_ids, relevant_ids),
                "relevant_total": len(relevant_ids),
                "retrieved_relevant": len(set(retrieved_ids) & set(relevant_ids)),
            }
            retrieval_results.append(ret_metrics)

        # --- answer metrics ---
        ans_metrics = {
            "question_id": q["id"],
            "type": q["type"],
            "answer": result["answer"],
            "latency_ms": result["metrics"]["total_latency_ms"],
            "tokens": result["metrics"]["tokens"],
        }

        if q["type"] == "out_of_scope":
            ans_metrics["refusal_score"] = judge_refusal(result["answer"])
            ans_metrics["faithfulness"] = ans_metrics["refusal_score"]
            ans_metrics["relevance"] = ans_metrics["refusal_score"]
        else:
            ans_metrics["faithfulness"] = judge_faithfulness(result["answer"], result["chunks"])
            ans_metrics["relevance"] = judge_relevance(result["answer"], q["question"])

            if q.get("gold_answer"):
                ans_metrics["exact_match"] = calc_exact_match(result["answer"], q["gold_answer"])
                ans_metrics["f1"] = calc_f1(result["answer"], q["gold_answer"])

        answer_results.append(ans_metrics)

        # be nice to the free tier rate limits
        time.sleep(4)

    summary = compute_summary(retrieval_results, answer_results, latencies, k)
    save_results(retrieval_results, answer_results, summary)

    return summary


def compute_summary(retrieval_results, answer_results, latencies, k):
    ret_agg = {}
    if retrieval_results:
        for metric in ["hit_rate", "recall_at_k", "mrr", "ndcg_at_k", "context_precision"]:
            values = [r[metric] for r in retrieval_results]
            ret_agg[metric] = round(np.mean(values), 4)

    ans_agg = {}
    faithfulness_scores = [a["faithfulness"] for a in answer_results if "faithfulness" in a]
    relevance_scores = [a["relevance"] for a in answer_results if "relevance" in a]
    em_scores = [a["exact_match"] for a in answer_results if "exact_match" in a]
    f1_scores = [a["f1"] for a in answer_results if "f1" in a]

    if faithfulness_scores:
        ans_agg["avg_faithfulness"] = round(np.mean(faithfulness_scores), 4)
    if relevance_scores:
        ans_agg["avg_relevance"] = round(np.mean(relevance_scores), 4)
    if em_scores:
        ans_agg["avg_exact_match"] = round(np.mean(em_scores), 4)
    if f1_scores:
        ans_agg["avg_f1"] = round(np.mean(f1_scores), 4)

    refusal_scores = [a["refusal_score"] for a in answer_results if "refusal_score" in a]
    if refusal_scores:
        ans_agg["avg_refusal_score"] = round(np.mean(refusal_scores), 4)

    latency_agg = {}
    if latencies:
        latency_agg["p50_retrieval_ms"] = round(np.percentile(latencies, 50), 2)
        latency_agg["p95_retrieval_ms"] = round(np.percentile(latencies, 95), 2)
        latency_agg["mean_retrieval_ms"] = round(np.mean(latencies), 2)

    total_tokens = sum(a["tokens"]["total_tokens"] for a in answer_results if "tokens" in a)

    summary = {
        "k": k,
        "total_questions": len(answer_results),
        "in_scope_questions": len(retrieval_results),
        "out_of_scope_questions": len(answer_results) - len(retrieval_results),
        "retrieval_metrics": ret_agg,
        "answer_metrics": ans_agg,
        "latency": latency_agg,
        "total_tokens_used": total_tokens,
        "embedding_model": config.EMBEDDING_MODEL,
        "embedding_dim": config.EMBEDDING_DIM,
        "llm_model": config.LLM_MODEL,
    }

    return summary


def save_results(retrieval_results, answer_results, summary):
    os.makedirs("eval/results", exist_ok=True)

    with open("eval/results/retrieval_metrics.json", "w") as f:
        json.dump(retrieval_results, f, indent=2)

    answer_summary = []
    for a in answer_results:
        entry = {k: v for k, v in a.items() if k != "answer"}
        entry["answer_preview"] = a["answer"][:200] + "..." if len(a["answer"]) > 200 else a["answer"]
        answer_summary.append(entry)

    with open("eval/results/answer_metrics.json", "w") as f:
        json.dump(answer_summary, f, indent=2)

    with open("eval/results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    print(f"\nRetrieval Metrics (k={summary['k']}):")
    for k_name, v in summary["retrieval_metrics"].items():
        print(f"  {k_name}: {v}")

    print(f"\nAnswer Metrics:")
    for k_name, v in summary["answer_metrics"].items():
        print(f"  {k_name}: {v}")

    print(f"\nLatency:")
    for k_name, v in summary["latency"].items():
        print(f"  {k_name}: {v}")

    print(f"\nTotal tokens used: {summary['total_tokens_used']}")
    print("=" * 60)

    print(f"\nResults saved to eval/results/")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run RAG evaluation harness")
    parser.add_argument("--k", type=int, default=None, help=f"Top-k for retrieval (default: {config.TOP_K})")
    args = parser.parse_args()

    run_evaluation(k=args.k)
