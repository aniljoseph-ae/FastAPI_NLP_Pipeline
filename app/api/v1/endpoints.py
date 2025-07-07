from fastapi import APIRouter, Depends, BackgroundTasks
from app.api.v1.schemas import TextInput, BatchTextInput, TaskResponse
from app.services.nlp_service import NLPService
from app.services.rag_service import RAGService
from app.tasks.celery_tasks import process_nlp_task
from app.core.dependencies import get_nlp_service, get_rag_service
import asyncio

router = APIRouter()

async def run_nlp_task(task_id: str, input_data: str | list, task_type: str, webhook_url: str | None):
    await process_nlp_task(task_id, input_data, task_type, webhook_url)

@router.post("/classify", response_model=TaskResponse)
async def classify_text(
    input: TextInput,
    background_tasks: BackgroundTasks,
    nlp_service: NLPService = Depends(get_nlp_service),
):
    task_id = nlp_service.generate_task_id()
    background_tasks.add_task(run_nlp_task, task_id, input.text, "classify", input.webhook_url)
    return TaskResponse(task_id=task_id, status="queued")

@router.post("/extract", response_model=TaskResponse)
async def extract_entities(
    input: TextInput,
    background_tasks: BackgroundTasks,
    nlp_service: NLPService = Depends(get_nlp_service),
):
    task_id = nlp_service.generate_task_id()
    background_tasks.add_task(run_nlp_task, task_id, input.text, "extract", input.webhook_url)
    return TaskResponse(task_id=task_id, status="queued")

@router.post("/summarize", response_model=TaskResponse)
async def summarize_text(
    input: TextInput,
    background_tasks: BackgroundTasks,
    nlp_service: NLPService = Depends(get_nlp_service),
):
    task_id = nlp_service.generate_task_id()
    background_tasks.add_task(run_nlp_task, task_id, input.text, "summarize", input.webhook_url)
    return TaskResponse(task_id=task_id, status="queued")

@router.post("/sentiment", response_model=TaskResponse)
async def analyze_sentiment(
    input: TextInput,
    background_tasks: BackgroundTasks,
    nlp_service: NLPService = Depends(get_nlp_service),
):
    task_id = nlp_service.generate_task_id()
    background_tasks.add_task(run_nlp_task, task_id, input.text, "sentiment", input.webhook_url)
    return TaskResponse(task_id=task_id, status="queued")

@router.post("/batch", response_model=TaskResponse)
async def batch_process(
    input: BatchTextInput,
    background_tasks: BackgroundTasks,
    nlp_service: NLPService = Depends(get_nlp_service),
):
    task_id = nlp_service.generate_task_id()
    background_tasks.add_task(run_nlp_task, task_id, input.texts, "batch", input.webhook_url)
    return TaskResponse(task_id=task_id, status="queued")

@router.post("/retrieve", response_model=dict)
async def retrieve_similar(
    input: TextInput,
    rag_service: RAGService = Depends(get_rag_service),
):
    results = await rag_service.retrieve_similar(input.text, top_k=5)
    return {"results": results}