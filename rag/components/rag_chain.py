from .formatter import format_documents
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from resources.prompts.rag_prompt import RAG_PROMPT

def create_rag_chain(
    llm
):
    
     return (
        RAG_PROMPT
        | llm
        | StrOutputParser()
    )
    
    