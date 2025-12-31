import os
# from langchain_chroma import Chroma
# from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
# import embedding # Your embedding logic
from dotenv import load_dotenv
load_dotenv()


llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("groq_api_key"),
    temperature=0.1 # Low temperature for factual accuracy
)

prompt = input("Enter your prompt: ")
response = llm.invoke(prompt)
print(response.content)