from rag.components.rag_chain import create_rag_chain
from rag.retrieval.hybrid_retrever import hybrid_search
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from llm.model import create_llm
from rag.components.formatter import format_documents
from langchain_core.tools import tool
from pydantic import Field
from typing import Annotated

load_dotenv()


@tool
def rag_tool(query=Annotated[
    str,
    Field(
        description="Query asked by the user"
    )
]):
    """
        This is the rag agent tool. Use this tool for any documentation related queries. Like to get info about travel guide 
        about any place mentioned by user or other things.
        
        Args:
            String:User query 
    
        Returns:
            A String response as the answer from the document
        """
    relevant_documents=hybrid_search(query)
    context=format_documents(relevant_documents)
    llm=create_llm("gpt-5")
    rag_chain = create_rag_chain(llm)
    
    response=rag_chain.invoke({
        "context": context,
        "question": query
    })
    
    return response.content

# if __name__ == "__main__":
#     print(rag_tool("What is the policy all about?"))