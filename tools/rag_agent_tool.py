from rag.components.rag_chain import create_rag_chain
from rag.retrieval.hybrid_retrever import hybrid_search
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from llm.model import create_llm
from rag.components.formatter import format_documents

load_dotenv()


def rag_tool(query:str):
    relevant_documents=hybrid_search(query)
    context=format_documents(relevant_documents)
    llm=create_llm("gpt-5")
    rag_chain = create_rag_chain(llm)
    
    return rag_chain.invoke({
        "context": context,
        "question": query
    })

if __name__ == "__main__":
    print(rag_tool("What is the policy all about?"))