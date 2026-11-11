from langchain_community.retrievers import BM25Retriever

def create_bm25_retriever(chunks,k=5):
    
    return BM25Retriever.from_documents(chunks).k  #Retriver top k matching docs 

    #Note that here we are not passing the query here in this function we are simply creating the bm25 retriver
    #Only when we invoke it through the rag chain then the query is passed to it 



    