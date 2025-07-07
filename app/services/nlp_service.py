import uuid
from openai import AsyncOpenAI
import redis.asyncio as redis
from app.core.config import settings
from app.services.webhook_service import notify_webhook
import logging

logger = logging.getLogger("nlp_pipeline")

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

    async def process_text(self, text: str, task_type: str) -> str:  # Fixed return type
        cache_key = f"{task_type}:{text}"
        cached_result = await self.redis.get(cache_key)
        if cached_result:
            logger.info(f"Cache hit for {cache_key}")
            return cached_result.decode("utf-8")

        prompts = {
            "classify": "Classify the sentiment of this text as positive, negative, or neutral: {text}",
            "extract": "Extract named entities (person, organization, location) from this text: {text}",
            "summarize": "Summarize this text in 50 words or less: {text}",
            "sentiment": "Analyze the sentiment of this text and provide a score from -1 to 1: {text}",
        }
        prompt = prompts[task_type].format(text=text)

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}]  # Fixed syntax
                    }
                ]
            )
            result = response.choices[0].message.content
            await self.redis.setex(cache_key, 3600, result)  # Cache for 1 hour
            logger.info(f"Processed {task_type} task for text: {text[:50]}...")
            return result
        except Exception as e:
            logger.error(f"Error processing {task_type} task: {str(e)}")
            raise

    async def process_batch(self, texts: list, task_type: str) -> list:
        return [await self.process_text(text, task_type) for text in texts]