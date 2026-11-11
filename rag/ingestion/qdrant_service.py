import os
from pathlib import Path

from dotenv import load_dotenv

from qdrant_client import QdrantClient,models
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings

load_dotenv()

QDRANT_URL=os.environ["QDRANT_URL"]
QDRANT_API_KEY=os.environ["QDRANT_API_KEY"]
COLLECTION_NAME=os.getenv(
    "QDRANT_COLLECTION",
    "traveligo_docs"
)

#Embedding model 
embeddings=OpenAIEmbeddings(
    model="text-embedding-3-small"
)

#Connect to qdrant cloud
qdrant_client=QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

def get_qdrant_vector_store()->QdrantVectorStore:
    
    #Create collection if it does not exist 
    if not qdrant_client.collection_exists(COLLECTION_NAME):
        
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=1536,
                distance=models.Distance.COSINE
            )
        )
        
    return QdrantVectorStore(
        client=qdrant_client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )
