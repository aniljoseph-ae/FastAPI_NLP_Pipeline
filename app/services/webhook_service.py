import aiohttp
import json
import logging

async def notify_webhook(webhook_url: str, payload: dict):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(webhook_url, json=payload) as response:
                if response.status != 200:
                    logging.error(f"Webhook notification failed: {response.status}")
        except Exception as e:
            logging.error(f"Webhook notification error: {str(e)}")