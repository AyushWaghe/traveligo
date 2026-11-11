from langchain_classic.retrievers import EnsembleRetriever

def create_hybrid_retriever(
    vector_retriever,
    bm25_retriever
):
    
    return EnsembleRetriever(
        retrievers=[
            vector_retriever,
            bm25_retriever
        ],
        weights=[
            0.5,0.5
        ]
    )
    

    