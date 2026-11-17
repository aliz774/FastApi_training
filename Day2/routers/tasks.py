from fastapi import APIRouter

router = APIRouter(tags=["task"])


@router.get("/list")
def task():
    return {"task":"About task"}

