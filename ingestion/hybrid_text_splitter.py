import pymupdf4llm
from langchain_core.documents import Document 
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter
)
from pathlib import Path

def split_text(
    file_path:str,
    chunk_size:int=1000,
    chunk_overlap:int=100,
)->list[Document]:
    
    """Here this performs hybrid chunking. Markdown header based spitting + reccurssive text splitting"""
    
    pdf_path=Path(file_path)
    
    if not pdf_path.is_file() or pdf_path.suffix.lower()!="pdf":
        raise ValueError(f"Invalid document type. File is not a PDF at {pdf_path}")
    
    if chunk_size<=0 or not 0<=chunk_overlap<chunk_size:
        raise ValueError("chunk_size must be positive and overlap must be smaller")
    
    
    #Extract pdf content as markdown (like in proper heading format labelling)
    markdown_text=pymupdf4llm.to_markdown(str(pdf_path))
    
    if not markdown_text.strip():
        return []
    
    
    #All 6 levels of headings 
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#" * level, f"heading_{level}")
            for level in range(1, 7)
        ],
        strip_headers=False, #Markdown headings should NOT be removed from the resulting chunk's content.
    )
    
    #Finally split the document markdown wise 
    sections=header_splitter.split_text(markdown_text)
    
    
    #Add meta data
    
    document_metadata={
        "source":str(pdf_path),
        "filename":pdf_path.name,
    }
    
    for section in sections:
        section.metadata.update(document_metadata)
        
        
    #Recurssive splitting 
    recurrsive_text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    chunks=recurrsive_text_splitter.split_text(sections)
    
    for ind,chunk in enumerate(chunks):
        chunk.metadata["chunk_index"]=ind
    
    
    return chunks
    
    