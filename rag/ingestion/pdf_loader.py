from pypdf import PdfReader
from langchain_core.documents import Document

def load_pdf(file_path):
    pdf_reader=PdfReader(file_path)
    
    documents=[]
    
    for page_num,page in enumerate(pdf_reader.pages):
        
        page_text=page.extract_text()
        
        if page_text:
            documents.append(
                Document(
                    page_content=page_text,
                    metadata={
                        "source":file_path,
                        "page_num":page_num+1
                    }
                )
            )
    
    
    return documents
    