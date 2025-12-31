import os
from langchain_openai import OpenAIEmbeddings

# Initialize the model using the standard OpenAI class (best for local servers)
embed_model = OpenAIEmbeddings(
    model="text-embedding-nomic-embed-text-v1.5",
    openai_api_base="http://127.0.0.1:1234/v1",
    openai_api_key="not-needed",
    check_embedding_ctx_length=False
)

def embed_for_storage(text):
    """Adds the required prefix for saving documents."""
    return f"search_document: {text}"

def embed_for_query(text):
    """Adds the required prefix for user questions."""
    return f"search_query: {text}"