import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

required_vars = ("PDF_PATH", "DATABASE_URL", "PG_VECTOR_COLLECTION")
for k in required_vars:
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")

def ingest_pdf():

    current_dir = Path(__file__).parent
    pdf_path = current_dir.parent / os.getenv("PDF_PATH")

    docs = PyPDFLoader(str(pdf_path)).load()


    splits = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=150, add_start_index=False).split_documents(docs)
    
    if not splits:
        raise SystemExit(0)

    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in splits
    ]

    ids = [f"doc-{i}" for i in range(len(enriched))]

    embeddings = GoogleGenerativeAIEmbeddings(
        model=os.getenv("EMBED_MODEL", "models/embedding-001")
    )

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

    store.add_documents(documents=enriched, ids=ids)

    pass


if __name__ == "__main__":
    ingest_pdf()