import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv


#load the env veriable 
load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_llm(question):
    return llm.invoke(question)
