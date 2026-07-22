# Cost Analysis: ChromaDB vs Managed Vector Databases

## Assumptions

- **Embedding dimension**: 384 (all-MiniLM-L6-v2)
- **Storage per vector**: ~1.6 KB (384 dims × 4 bytes + metadata overhead)
- **Queries per month**: 10,000 (light usage)
- **Compute**: single-core VM or local machine for ChromaDB/FAISS
- **Managed DB pricing**: based on publicly listed prices (as of 2024)

## Monthly Cost Comparison

| Scale | ChromaDB (self-hosted) | FAISS (self-hosted) | Pinecone (Starter→Standard) | Weaviate Cloud |
|-------|----------------------|--------------------|-----------------------------|----------------|
| **100K vectors** | ~$5/mo (small VM) | ~$5/mo (small VM) | $0 (free tier) → $70/mo | ~$25/mo |
| **1M vectors** | ~$10/mo (2GB RAM VM) | ~$10/mo (2GB RAM VM) | ~$70/mo (s1 pod) | ~$100/mo |
| **10M vectors** | ~$40/mo (16GB RAM VM) | ~$25/mo (6GB RAM, in-memory) | ~$350/mo (multiple pods) | ~$400/mo |

### How we calculated this

**ChromaDB self-hosted:**
- Stores data on disk (SQLite + parquet). RAM usage is mostly for the HNSW index.
- 100K vectors × 1.6KB ≈ 160MB on disk. HNSW index ~300MB in RAM.
- 1M vectors ≈ 1.6GB disk, ~2GB RAM for index.
- 10M vectors ≈ 16GB disk, ~12GB RAM for index.
- VM costs: $5/mo (1GB RAM, e.g. DigitalOcean droplet) to $40/mo (16GB RAM).
- No per-query costs.

**FAISS self-hosted:**
- Pure in-memory with IndexFlatIP. All vectors must fit in RAM.
- 100K × 384 × 4 bytes ≈ 150MB RAM.
- 1M ≈ 1.5GB RAM.
- 10M ≈ 15GB RAM. But with IVF index, can compress to ~6GB.
- Same VM costs. Slightly cheaper than ChromaDB at scale because no HNSW overhead.
- No metadata filtering — you'd need a side database for that.

**Pinecone (managed):**
- Free tier: 100K vectors on 1 pod (limited).
- Standard: starts at ~$70/mo for s1.x1 pod (1M vectors capacity).
- Scaling: each additional pod ~$70/mo. 10M vectors needs ~5 pods.
- Includes: managed infra, monitoring, backups, SLA.

**Weaviate Cloud:**
- Sandbox: free but limited.
- Standard: starts ~$25/mo for small clusters.
- Scales roughly linearly with data size.

## Trade-offs We Accept with ChromaDB

| Trade-off | Impact | Mitigation |
|-----------|--------|------------|
| No built-in replication | Single point of failure | Regular backups, can restore from embeddings |
| No SLA or managed monitoring | Must self-manage uptime | Simple health check endpoint, systemd service |
| HNSW index lives in RAM | Memory grows with vectors | At 10M+ vectors, consider IVF or disk-based ANN |
| No horizontal scaling | Single machine limit | Shard by metadata/topic if needed |
| Query latency slightly higher than FAISS | ~2-10ms vs <1ms (see benchmark) | Still sub-100ms total, fine for most apps |

## When to Switch to Managed

1. **>10M vectors** with low-latency requirements → HNSW RAM costs become significant, managed DBs handle sharding automatically.
2. **Multi-region deployment** → replication and geo-distribution is hard to DIY.
3. **Team size > 3-4 engineers** → managed DB reduces operational burden, the cost is justified by engineering time saved.
4. **SLA requirements** → if you need 99.9%+ uptime guarantees, pay for managed.
5. **Rapid scaling** → if vector count is growing 10x in months, managed auto-scaling is worth it.

## Bottom Line

For a lightly-queried corpus under 1M vectors, ChromaDB on a small VM costs **$5-10/mo** vs **$70-100/mo** for managed alternatives. That's a **7-10x cost reduction**. The main trade-off is operational responsibility — you manage your own backups, uptime, and scaling. For a startup MVP, internal tool, or academic project, this is a no-brainer. For production systems with SLA requirements and a growing team, the managed tax starts to make sense.
