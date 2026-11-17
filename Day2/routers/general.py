from fastapi import APIRouter

router = APIRouter(tags=["user"])


@router.get("/health")
def health():
    return {"status":"ok"} 


@router.get("/about")
def about():
    return {"User":"Good morning"}


@router.get("/home")
def home():
    return {"Welcome home"}

    