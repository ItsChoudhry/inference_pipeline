from contextlib import asynccontextmanager
from typing import Optional, Union

from starlette.responses import JSONResponse
from .models.task import CreateTask, Task
from datetime import datetime
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html

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


@app.post("/v1/tasks")
def add_task(task: CreateTask, idempotency_key: Optional[str] = None):
    print(task)
    print(idempotency_key)
    if idempotency_key and idempotency_key in tasks:
        return tasks[idempotency_key]

    now = datetime.now()
    generated_id = str(uuid.uuid4())
    idem_key = idempotency_key if idempotency_key else generated_id
    new_task = Task(
        id=generated_id,
        idempotency_key=idem_key,
        model=task.model,
        param=task.param,
        inputs=task.inputs,
        status="pending",
        result_url=None,
        error=None,
        callback_url=task.callback_url,
        api_key_id="",
        created_at=now,
        updated_at=now,
    )
    tasks[idem_key] = new_task
    return idem_key


@app.get("/v1/tasks/{task_id}")
def get_task(task_id: str, q: Union[str, None] = None):
    return tasks[task_id]


@app.get("/v1/models")
def list_models():
    return {"ChatBpd": ["0.1.0"], "Cloudsunut": ["0.2.1"]}


@app.get("/healthz")
def health_check():
    try:
        # _perform_health_checks()
        return JSONResponse(status_code=200, content={"status": "healthy"})
    except Exception as e:
        raise HTTPException(status_code=503, detail={"status": "unhealthy", "error": e})


@app.get("/readyz")
def ready_check():
    # _perform_health_checks()
    # check db, redis ping, minIO access check
    return JSONResponse(status_code=200, content={"status": "healthy"})


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Custom OpenAPI docs at /docs with Swagger UI."""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )
