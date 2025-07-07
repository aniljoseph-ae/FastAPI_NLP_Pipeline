from setuptools import setup, find_packages

setup(
    name="nlp_pipeline",
    version="1.0.0",
    description="A FastAPI-based NLP pipeline with RAG integration",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.103.0",
        "uvicorn==0.23.2",
        "pydantic==2.4.2",
        "openai==1.3.5",
        "langchain==0.0.305",
        "weaviate-client==3.24.0",
        "sentence-transformers==2.2.2",
        "redis==5.0.0",
        "celery==5.3.4",
        "aiohttp==3.8.5",
        "mlflow==2.7.1",
        "python-dotenv==1.0.0",
        "pytest==7.4.2",
        "PyPDF2==3.0.1",
        "langgraph==0.2.5",  # Added for RAGService
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)