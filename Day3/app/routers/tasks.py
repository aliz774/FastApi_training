from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from fastapi import Response



# Request Schema
class TaskCreate(BaseModel):
    title: str
    discription: str
    completed: bool = False

class TaskReplace(BaseModel):
    title: str
    discription: str
    completed: bool 

class TaskUpdate(BaseModel):
    title: str | None = None
    discription: str | None = None
    completed: bool | None = None



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

    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


#PUT
@router.put("/{tasK_id}")
def replace_task(task_id: int, payload:TaskReplace):

    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    updated_task = {
        "id": task_id,
        **payload.model_dump()
    }

    tasks[task_id] = updated_task

    return updated_task

@router.patch("/{task_id}")
def update_task(task_id: int, payload:TaskUpdate):

    if task_id not in tasks:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

    updates = payload.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    if "title" in updates and updates["title"] is None:
        raise HTTPException(
            status_code=422,
            detail="Title cannot be null"
        )

    if "discription" in updates and updates["discription"] is None:
            raise HTTPException(
                status_code=422,
                detail="discription cannot be null"
            )

    if "completed" in updates and updates["completed"] is None:
            raise HTTPException(
                status_code=422,
                detail="completed cannot be null"
            )

    tasks[task_id].update(updates)

    return tasks[task_id]


@router.delete("{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int):

     if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

     del tasks[task_id]

     return Response(status_code=status.HTTP_204_NO_CONTENT)