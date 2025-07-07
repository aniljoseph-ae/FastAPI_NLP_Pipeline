import uuid 
from openai import AsyncOpenAI
import redis.asyncio as redis

from app.core.config import settings
from app.utils.embedding import generate_embedding
from app.utils.reranker import reranker_result
from app.services.webhook_service import notify_webhook

class NLPService:
    def __init__(self):
        
        self.client = AsyncOpenAI(
            api_key=settings.API_KEY,
            base_url=settings.ULTRASAFE_API_URL,
        )

        self.redis = redis.from_url(settings.REDIS_URL)
        self.model = settings.MODEL_NAME

    def generate_task_id(self):
        return str(uuid.uuid4())
    
    async def process_text(self, text: str, task_type: str) -> dict:
        cache_key = f"{task_type}: {text}"
        cached_result = await self.redis.get(cache_key)
        if cached_result:
            return cached_result.decode("utf-8")
        
    # define prompt based on task

        prompts = {
            "classify": "Classify the sentiment of this text as positive, negative, or neutral: {text}",
            "extract": "Extract named entities (person, organization, location) from this text: {text}",
            "summarize": "Summarize this text in 50 words or less: {text}",
            "sentiment": "Analyze the sentiment of this text and provide a score from -1 to 1: {text}",
        }
        prompt = prompts[task_type].format(text=text)

        # call ultrasafe ai API
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user", 
                    "content":[{"text": "text", "text": prompt}]
                }
            ]
        )
        result = response.choices[0].message.content

        # cache result
        await self.redis.setex(cache_key, 3600, result)
        return result
    
    async def process_batch(self, texts: list, task_type: str) -> list:
        return [await self.process_text(text, task_type) for text in texts]