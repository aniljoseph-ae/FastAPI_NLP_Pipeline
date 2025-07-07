from openai import OpenAI
from app.core.config import Settings

def generate_embedding(text: str) -> str:
    client = OpenAI(
        api_key=Settings.API_KEY,
        base_url=Settings.ULTRASAFE_API_URL
    )

    response = client.embeddings.create(
        input=text,
        model=Settings.EMBEDDING_MODEL
    )

    return response.data[0].embedding