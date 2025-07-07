import json
import os
from PyPDF2 import PdfReader
from app.utils.vector_store import VectorStore
from typing import List, Dict
import logging

logger = logging.getLogger("nlp_pipeline")

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        logger.error(f"Error reading PDF {file_path}: {str(e)}")
        return ""

def process_input_data(file_path: str) -> List[Dict]:
    """Process input data from JSON or PDF files."""
    documents = []
    
    if file_path.endswith(".json"):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    documents = [
                        {"content": item["content"], "metadata": item.get("metadata", {"source": file_path})}
                        for item in data
                    ]
                else:
                    documents.append({"content": data["content"], "metadata": data.get("metadata", {"source": file_path})})
        except Exception as e:
            logger.error(f"Error processing JSON {file_path}: {str(e)}")
            raise
    elif file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
        if text:
            documents.append({"content": text, "metadata": {"source": file_path}})
    else:
        raise ValueError("Unsupported file format. Use JSON or PDF.")

    return documents

def ingest_data(file_path: str):
    """Ingest data into the vector store."""
    try:
        vector_store = VectorStore()
        documents = process_input_data(file_path)
        texts = [doc["content"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]
        vector_store.add_documents(texts, metadatas)
        logger.info(f"Successfully ingested {len(documents)} documents from {file_path}.")
    except Exception as e:
        logger.error(f"Data ingestion failed for {file_path}: {str(e)}")
        raise

if __name__ == "__main__":
    # Example usage: ingest JSON or PDF
    input_file = "sample_data.json"  # or "sample_document.pdf"
    ingest_data(input_file)