from datetime import datetime, timezone
from typing import Optional, Union
import uuid
from ..auth import require_api_key
from ..models.task import CreateTask, Task, tasks
from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse

protected_router = APIRouter(
    dependencies=[Depends(require_api_key)], tags=["protected"]
)

idempotency_map: dict[str, str] = {}


@protected_router.post("/v1/tasks")
def add_task(
    task: CreateTask,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
):
    if idempotency_key and idempotency_key in idempotency_map:
        task_id = idempotency_map[idempotency_key]
        if task_id in tasks:
            response = JSONResponse(status_code=200, content={"task_id": task_id})
            response.headers["Location"] = f"/v1/tasks/{task_id}"
            return response

    now = datetime.now(timezone.utc)
    generated_id = str(uuid.uuid4())
    idem_key = idempotency_key or generated_id
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

    tasks[new_task.id] = new_task
    if idem_key:
        idempotency_map[idem_key] = new_task.id

    response = JSONResponse(status_code=201, content={"task_id": generated_id})
    response.headers["Location"] = f"/v1/tasks/{generated_id}"
    return response


@protected_router.get("/v1/tasks/{task_id}")
def get_task(task_id: str, q: Union[str, None] = None):
    return tasks[task_id]


@protected_router.get("/v1/models")
def list_models():
    return {"ChatBpd": ["0.1.0"], "Cloudsunut": ["0.2.1"]}


@protected_router.get("/readyz")
def ready_check():
    # _perform_health_checks()
    # check db, redis ping, minIO access check
    return JSONResponse(status_code=200, content={"status": "ready"})
