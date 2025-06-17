import sqlite3
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd


def ingest_csv_to_db(csv_file_path, db_file_path):
    """Load CSV data into SQLite database."""
    conn = sqlite3.connect(db_file_path)
    try:
        data = pd.read_csv(csv_file_path)
        data.to_sql("documents", conn, if_exists="replace", index=False)
        print(f"CSV data from {csv_file_path} successfully loaded into {db_file_path}.")
    except Exception as e:
        print(f"Error ingesting CSV data: {e}")
    finally:
        conn.close()


def ingest_pdf_to_langchain(pdf_path):
    """Load PDF data into LangChain vector store."""
    loader = PyPDFLoader(pdf_path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    documents = loader.load_and_split(splitter)
    vector_store = FAISS.from_documents(documents)
    vector_store.save_local("data/vectorstore")
    print(f"PDF data from {pdf_path} successfully ingested into LangChain vector store.")