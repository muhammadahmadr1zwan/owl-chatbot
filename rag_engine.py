"""
RAG Engine for Purdue OWL Chatbot
Handles text ingestion, vector storage, and retrieval using LangChain + ChromaDB
"""

import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Configuration
DATA_DIR = "data"
CHROMA_DIR = "chromadb"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def load_documents(data_dir: str = DATA_DIR) -> list:
    """
    Load all .txt files from the data directory.
    
    Args:
        data_dir: Path to directory containing text files
        
    Returns:
        List of Document objects
    """
    loader = DirectoryLoader(
        data_dir,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()
    print(f"Loaded {len(documents)} document(s) from {data_dir}")
    return documents


def split_documents(documents: list) -> list:
    """
    Split documents into smaller chunks for better retrieval.
    
    Args:
        documents: List of Document objects
        
    Returns:
        List of chunked Document objects
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks


def create_database(data_dir: str = DATA_DIR, persist_dir: str = CHROMA_DIR) -> Chroma:
    """
    Main function: Load documents, split them, create embeddings, and store in ChromaDB.
    
    Args:
        data_dir: Path to directory containing text files
        persist_dir: Path to store the ChromaDB database
        
    Returns:
        Chroma vector store instance
    """
    # Load and split documents
    documents = load_documents(data_dir)
    chunks = split_documents(documents)
    
    # Create embeddings using HuggingFace (free, runs locally)
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )
    
    # Create and persist the vector store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    
    print(f"Database created and saved to {persist_dir}")
    return vectorstore


def load_database(persist_dir: str = CHROMA_DIR) -> Chroma:
    """
    Load an existing ChromaDB database.
    
    Args:
        persist_dir: Path to the ChromaDB database
        
    Returns:
        Chroma vector store instance
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )
    
    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )
    
    print(f"Database loaded from {persist_dir}")
    return vectorstore


def search(query: str, vectorstore: Chroma, k: int = 3) -> list:
    """
    Search the vector store for relevant documents.
    
    Args:
        query: User's question
        vectorstore: Chroma vector store instance
        k: Number of results to return
        
    Returns:
        List of relevant document chunks
    """
    results = vectorstore.similarity_search(query, k=k)
    return results


# Run this script directly to build the database
if __name__ == "__main__":
    print("Building Purdue OWL knowledge base...")
    print("-" * 40)
    
    if not os.path.exists(DATA_DIR):
        print(f"Error: {DATA_DIR} directory not found!")
        print("Please add .txt files to the data folder first.")
    else:
        db = create_database()
        print("-" * 40)
        print("Done! You can now use the chatbot.")
