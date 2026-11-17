from fastapi import FastAPI
from routers import general, tasks
from config import settings

app = FastAPI()

app.include_router(general.router)
app.include_router(tasks.router)


@app.get("/")
def demo():
    return {"Fastapi is running."}




@app.get("/config")
def config_info():
    return {
        "app_name": settings.app_name,
        "token_expiry": settings.access_token_expire_minutes
    }
