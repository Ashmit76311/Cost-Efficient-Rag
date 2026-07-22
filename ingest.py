import os
import hashlib
import argparse
from pathlib import Path

import chromadb
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

import config

client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
collection = client.get_or_create_collection(
    name=config.COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)

embedder = SentenceTransformer(config.EMBEDDING_MODEL)


def read_pdf(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def read_html(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    return soup.get_text()


def read_md(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def read_file(filepath):
    ext = Path(filepath).suffix.lower()
    if ext == ".pdf":
        return read_pdf(filepath)
    elif ext in [".html", ".htm"]:
        return read_html(filepath)
    elif ext in [".md", ".txt"]:
        return read_md(filepath)
    else:
        print(f"Skipping unsupported file: {filepath}")
        return None


def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        length_function=len,
    )
    return splitter.split_text(text)


def make_chunk_id(source, chunk_index, content):
    # deterministic ID so re-ingesting the same file doesn't create duplicates
    raw = f"{source}:{chunk_index}:{content}"
    h = hashlib.md5(raw.encode()).hexdigest()[:10]
    return f"{Path(source).stem}_chunk{chunk_index}_{h}"


def ingest_file(filepath):
    text = read_file(filepath)
    if not text:
        return 0

    chunks = chunk_text(text)
    source = Path(filepath).name
    filetype = Path(filepath).suffix.lower().lstrip(".")

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        ids.append(make_chunk_id(source, i, chunk))
        documents.append(chunk)
        metadatas.append({
            "source": source,
            "chunk_index": i,
            "filetype": filetype,
            "total_chunks": len(chunks),
        })

    embeddings = embedder.encode(documents).tolist()

    # upsert = insert or update, so re-running is idempotent
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print(f"  {source}: {len(chunks)} chunks (model={config.EMBEDDING_MODEL}, dim={config.EMBEDDING_DIM})")
    return len(chunks)


def ingest_source(source_path):
    path = Path(source_path)
    total = 0

    if path.is_file():
        total = ingest_file(str(path))
    elif path.is_dir():
        for f in sorted(path.iterdir()):
            if f.is_file() and f.suffix.lower() in [".pdf", ".html", ".htm", ".md", ".txt"]:
                total += ingest_file(str(f))
    else:
        print(f"Path not found: {source_path}")

    print(f"\nDone. Total chunks: {total}")
    print(f"Collection size: {collection.count()}")
    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest documents into ChromaDB")
    parser.add_argument("--source", required=True, help="Path to a file or directory to ingest")
    parser.add_argument("--chunk-size", type=int, default=None, help=f"Chunk size in chars (default: {config.CHUNK_SIZE})")
    parser.add_argument("--chunk-overlap", type=int, default=None, help=f"Chunk overlap in chars (default: {config.CHUNK_OVERLAP})")
    args = parser.parse_args()

    if args.chunk_size:
        config.CHUNK_SIZE = args.chunk_size
    if args.chunk_overlap:
        config.CHUNK_OVERLAP = args.chunk_overlap

    print(f"Ingesting from: {args.source}")
    print(f"Chunk size: {config.CHUNK_SIZE}, Overlap: {config.CHUNK_OVERLAP}\n")
    ingest_source(args.source)
