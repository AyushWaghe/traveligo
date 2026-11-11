
def create_vector_retriver(vector_store,k=5):
    
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )
    
    
#Note that in this vector retriver funtion we are not passing the query embeddings since the query is converted to the 
#Embedding internally by the qdrant. As observe that we had mentioned the embedding model while making the qdrant vector store 