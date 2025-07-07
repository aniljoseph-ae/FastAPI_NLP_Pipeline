from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    API_KEY : str = ""        # PASTE_API_KEY_HERE
    ULTRASAFE_API_URL : str =  "https://api.us.inc/usf/v1/hiring/chat/completions"
    WEAVIATE_URL : str = "http://weaviate:8080"
    REDIS_URL : str = "redis://redis:6379/0"
    ALLOWED_ORIGINS : List[str] = ["*"]
    MODEL_NAME : str = "usf-mini"
    EMBEDDING_MODEL : str = "text-embedding-ada-002"
    CELERY_BROCKER_URL : str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"



settings = Settings()