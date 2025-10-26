from contextlib import asynccontextmanager
from typing import Union
from .models.task import Task
from datetime import datetime
import uuid

from fastapi import FastAPI

tasks: dict[str, Task] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    placeholder_task = Task(
        id=str("0"),
        idempotency_key=str(uuid.uuid4()),
        model="Placeholder model",
        param={},
        inputs={},
        status="NotStarted",
        result_url="",
        error="",
        callback_url="",
        api_key_id="",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    tasks[placeholder_task.id] = placeholder_task
    print(f"Added placeholder task with ID: {placeholder_task.id}")

    yield

    tasks.clear()
    print("Cleared tasks on shutdown")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/v1/tasks/{task_id}")
def read_item(task_id: int, q: Union[str, None] = None):
    if task_id == 0:
        return tasks[str(task_id)]
    return {"item_id": task_id, "q": q}
