"""This function formats the retrieved langchain docs together in simple string format to be passed to the llm"""


def format_documents(docs):
    pieces = []

    for doc in docs:
        piece = f"""
File name: {doc.metadata.get("filename")}
Chunk index:{doc.metadata.get("chunk_index")}

{doc.page_content}
"""
        pieces.append(piece)

    return "\n\n".join(pieces)  
