from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Task(BaseModel):
    id: str
    idempotency_key: Optional[str] = None
    model: str
    param: dict[str, str]
    inputs: dict[str, str]
    status: str
    result_url: Optional[str] = None
    error: Optional[str] = None
    callback_url: Optional[str] = None
    api_key_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class CreateTask(BaseModel):
    model: str
    param: dict[str, str]
    inputs: dict[str, str]
    callback_url: Optional[str] = None
