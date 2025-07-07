import aiohttp
import logging
from app.api.v1.schemas import WebhookInput

logger = logging.getLogger("nlp_pipeline")

async def notify_webhook(webhook_url: str, payload: dict):
    """Send webhook notification with validated payload."""
    try:
        webhook_input = WebhookInput(**payload)
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=webhook_input.dict()) as response:
                if response.status != 200:
                    logger.error(f"Webhook notification failed: {response.status}")
                else:
                    logger.info(f"Webhook notification sent to {webhook_url}")
    except Exception as e:
        logger.error(f"Webhook notification error: {str(e)}")