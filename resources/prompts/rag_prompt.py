from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT = ChatPromptTemplate.from_template(
    """
You are a helpful assistant.

Answer the question only using the provided context.

If the answer is not available in the context,
say:

"I don't know based on the provided document."

Context:
{context}

Question:
{question}

Answer:
"""
)