from pydantic import BaseModel
from typing import List, Optional

class TextInput(BaseModel):
    text: str
    webhook_url: Optional[str] = None

class BatchTextInput(BaseModel):
    texts: List[str]
    webhook_url: Optional[str] = None

class TaskResponse(BaseModel):
    task_id: str
    status: str

class WebhookInput(BaseModel):
    task_id: str
    result: str | List[str]