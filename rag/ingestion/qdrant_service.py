import os
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient,models
from langchain_qdrant import (QdrantVectorStore,RetrievalMode,FastEmbedSparse)
from langchain_openai import OpenAIEmbeddings

load_dotenv()

DENSE_VECTOR_NAME = "dense"
SPARSE_VECTOR_NAME = "bm25"

QDRANT_URL=os.environ["QDRANT_URL"]
QDRANT_API_KEY=os.environ["QDRANT_API_KEY"]
COLLECTION_NAME=os.getenv(
    "QDRANT_COLLECTION",
    "traveligo_docs"
)

#Vector embeddigns  
vector_embeddings=OpenAIEmbeddings(
    model="text-embedding-3-small"
)

#BM 25 embeddings 
#FastEmbedSparse is a class provided by langchain_qdrant that helps convert text into sparse vectors, 
# which are used for keyword-based retrieval such as BM25.
sparse_embeddings=FastEmbedSparse(
    model_name="Qdrant/bm25"
)

#Connect to qdrant cloud
qdrant_client=QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

def get_qdrant_vector_store()->QdrantVectorStore:
    
    #Create collection if it does not exist 
    if not qdrant_client.collection_exists(COLLECTION_NAME):
        
        dimension = len(
            vector_embeddings.embed_query("dimension check")
        )
        
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,

            vectors_config={
                DENSE_VECTOR_NAME: models.VectorParams(
                    size=dimension,
                    distance=models.Distance.COSINE
                )
            },

            sparse_vectors_config={
                SPARSE_VECTOR_NAME: models.SparseVectorParams(
                    modifier=models.Modifier.IDF
                )
            }
        )
        
    return QdrantVectorStore(
        client=qdrant_client,
        collection_name=COLLECTION_NAME,
        embedding=vector_embeddings,
        sparse_embedding=sparse_embeddings,
        retrieval_mode=RetrievalMode.HYBRID,
        vector_name=DENSE_VECTOR_NAME,
        sparse_vector_name=SPARSE_VECTOR_NAME
    )
