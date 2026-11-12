import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY=os.environ["OPENAI_API_KEY"]

def create_llm(model:str,timeout:float=30.0,max_retries:int=1):
    return ChatOpenAI(
        model=model,
        api_key=OPENAI_API_KEY,
        timeout=30.0,
        max_retries=1,
    )
