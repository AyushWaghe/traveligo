"""This is the RAG agent which has been exposed as a tool for the planner agent"""

from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings


def create_rag_agent():
    
    embeddings=OpenAIEmbeddings()
    
    vector_store=QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name="traveligo_docs",
        url=""
    )
    
    retriever=vector_store.as_retriever()
    