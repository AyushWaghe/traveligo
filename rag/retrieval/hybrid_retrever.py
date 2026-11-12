from rag.ingestion.qdrant_service import get_qdrant_vector_store
from qdrant_client import models
from langchain_core.documents import Document

def hybrid_search(
    query:str,
    top_k:int=5,
    fetch_k:int=10,
    dense_vector_weight:float=5.0,
    sparse_weight:float=5.0
):
    vector_store=get_qdrant_vector_store()
    
    qdrant_client=vector_store.client
    
    #Dense embeddings of the query 
    dense_vector_query=vector_store.embeddings.embed_query(query)
    
    #Sparse embeddings of the qury 
    sparse_vector_query=vector_store.sparse_embeddings.embed_query(query)
    
    #Execute the search and store it in results
    #client.query_points() is a method provided by the Qdrant Python client that allows you to search for 
    # relevant data (points) stored in your Qdrant collection. 
    #The point in qdrant is as u know. 
    results=qdrant_client.query_points(
        collection_name=vector_store.collection_name,
        
        prefetch=[
            #Dense retrieval 
            #Prefetch bascially specifies the searches that Qdrant must execute before performing the main query.
            models.Prefetch( #Models.prefetch allows you to define a search operation that Qdrant executes before performing the main query.
                query=dense_vector_query,
                using="dense",  #This is the name which we have given to the dense vector field in the qdrant servie . py file if u see. It basically tells qdrant in which vector the search should be performed ? Dense or spase since we have stored these two in the qdrant while ingestion
                limit=fetch_k 
            ),
            
            #BM25 retrieval 
            
            models.Prefetch(
                query=models.SparseVector(
                    indices=sparse_vector_query.indices,
                    values=sparse_vector_query.values
                ),
                using="bm25",
                limit=fetch_k
            )
        ],
        
        #RRF Fusion 
        query=models.RrfQuery( #This tells Qdrant to combine the two prefetched result sets using Reciprocal Rank Fusion.
            rrf=models.Rrf(
                k=2,
                weights=[
                    dense_vector_weight,
                    sparse_weight
                ]
            )
        ),
        
        limit=top_k,
        
        with_payload=True
    )
    
    #Conver the above results to langchain documents 
    docs=[]
    
    for point in results.points:
        payload=point.payload
        
        langchain_document=Document(
            page_content=payload.get("page_content",""),
            metadata={
                **payload.get("metadata", {}),
                "score": point.score,
                "point_id": str(point.id)
            }
        )
        
        docs.append(langchain_document)
    
    
    return docs


# ---------------------------------------------------------------------------------------------


#The whole searching can be done in the below simple code but since we have to confgireu k value and all that hence we did above and also for better understandings 
# def create_hybrid_retriever():
#     vector_store = get_qdrant_vector_store()

#     return vector_store.as_retriever(
#         search_kwargs={"k": 5}
#     )
    