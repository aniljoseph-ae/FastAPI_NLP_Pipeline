from openai import OpenAI
from app.core.config import settings  # Fixed capitalization

def generate_embedding(text: str) -> list:  # Fixed return type
    client = OpenAI(
        api_key=settings.API_KEY,
        base_url=settings.ULTRASAFE_API_URL
    )
    response = client.embeddings.create(
        input=text,
        model=settings.EMBEDDING_MODEL
    )
    return response.data[0].embedding