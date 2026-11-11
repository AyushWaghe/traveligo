import json
import asyncio
from pathlib import Path
from rag.ingestion.hybrid_text_splitter import split_text
from rag.ingestion.qdrant_service import get_qdrant_vector_store

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_PATH = BASE_DIR / "config" / "docs_to_upload.json"

async def ingest_documents():
    
    # Read configuration/docs_to_upload json 
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = json.load(file)

    document_paths = config.get("documents", [])
    
    if not document_paths:
        print("No documents to be ingested.Skipping ingestion...")
        return
    
    #Get qdrant 
    vector_store=get_qdrant_vector_store()
    
    for doc_path in document_paths:
        
        pdf_path=BASE_DIR/doc_path
        
        if not pdf_path.is_file():
            print(f"File not found {pdf_path}")
            continue
        
        #Extract and chunk the pdf 
        chunks=split_text(str(pdf_path))
        
        if not chunks: continue
        
        await vector_store.aadd_documents(
            documents=chunks
        )
        
        print(f"Document {pdf_path} uploaded to Qdrant.")
        
if __name__ == "__main__":
    asyncio.run(ingest_documents())
    
    
    