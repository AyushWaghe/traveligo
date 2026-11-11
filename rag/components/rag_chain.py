from formatter import format_documents
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def create_rag_chain(
    retriever,llm
):
    
    return (
        {
            "context":retriever | format_documents,
            "query":RunnablePassthrough()
        }
        
        | RAG_PROMPT | llm | StrOutputParser()
    )
    
    