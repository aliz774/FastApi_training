from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel




# Request Schema
class TaskCreate(BaseModel):
    title: str
    discription: str
    completed: bool = False

router = APIRouter(prefix="/tasks", tags=["Tasks"])



# Temporary storage
tasks = {}
next_id = 1




# APIs

@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    global next_id

    task = {
        "id" : next_id,
        **payload.model_dump()
    }


    tasks[next_id] = task
    next_id += 1

    return task

'''
{
"id": 2
"title":xyz,
"desc":abc,
"completed":True
}
'''

@router.get("")
def list_tasks():
    return list(tasks.values())


@router.get("/{task_id}")
def get_task(task_id: int):

    task = tasks.get(task_id)

    if not task:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,details="Task not found"
        )

    return task