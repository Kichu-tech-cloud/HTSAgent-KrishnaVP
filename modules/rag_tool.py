import os
import sqlite3
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
import pandas as pd
import json

VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), "data/vectorstore")
DB_PATH = os.path.join(os.path.dirname(__file__), "hts_data.db")
MEMORY_FILE = "rag_memory.json"

def initialize_rag_tool():
    """Initialize the RAG tool by loading vector store or fallback database."""
    pass

def handle_rag_query(query):
    """Handle user query using LangChain or fallback to SQLite."""
    try:
        # LangChain Search
        if os.path.exists(VECTOR_STORE_PATH):
            vector_store = FAISS.load_local(VECTOR_STORE_PATH, OpenAIEmbeddings())
            results = vector_store.similarity_search(query, k=1)
            if results:
                return results[0].page_content

        # Fallback to SQLite
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM documents WHERE content LIKE ?", (f"%{query}%",))
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else "No relevant information found."
    except Exception as e:
        return f"Error while searching: {e}"

def save_to_memory(memory, file_name):
    """Save memory to a JSON file."""
    with open(file_name, "w") as file:
        json.dump(memory, file)

def load_from_memory(file_name):
    """Load memory from a JSON file."""
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return json.load(file)
    return []
