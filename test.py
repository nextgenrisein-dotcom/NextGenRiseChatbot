import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


api_key = os.getenv("GROQ_API_KEY")


if not api_key:
    raise ValueError("GROQ_API_KEY not found")


print("Groq API Key loaded successfully")


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=api_key
)


response = llm.invoke(
    "Introduce yourself in one sentence."
)


print(response.content)