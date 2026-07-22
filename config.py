import os
from dotenv import load_dotenv

load_dotenv()

# LLM provider: "groq" or "gemini"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/chromadb")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 output dimension

# groq uses llama, gemini uses gemini-2.0-flash
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile" if LLM_PROVIDER == "groq" else "gemini-2.0-flash")

# chunking defaults
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

TOP_K = int(os.getenv("TOP_K", "5"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "documents")
