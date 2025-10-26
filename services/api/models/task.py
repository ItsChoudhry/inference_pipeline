from pydantic import BaseModel
from datetime import datetime


class Task(BaseModel):
    id: str
    idempotency_key: str
    model: str
    param: dict[str, str]
    inputs: dict[str, str]
    status: str
    result_url: str
    error: str
    callback_url: str
    api_key_id: str
    created_at: datetime
    updated_at: datetime
