from celery import Celery
from app.core.config import settings
from app.services.nlp_service import NLPService
from app.services.webhook_service import notify_webhook

app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

app.conf.task_serializer = "json"
app.conf.accept_content = ["json"]  # Fixed typo
app.conf.result_serializer = "json"

@app.task
async def process_nlp_task(task_id: str, input_data: str | list, task_type: str, webhook_url: str | None):
    nlp_service = NLPService()
    result = (
        await nlp_service.process_batch(input_data, task_type)
        if task_type == "batch"
        else await nlp_service.process_text(input_data, task_type)
    )
    if webhook_url:
        await notify_webhook(webhook_url, {"task_id": task_id, "result": result})
    return result