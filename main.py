from db.main import init_db

from routes.auth import auth_router
from routes.summarize import summ_router

from errors import register_all_errors

from fastapi import FastAPI
from settings import config

app = FastAPI()

register_all_errors(app)

app.include_router(auth_router, tags = ['Authentication'], prefix = f'/{config.API_VERSION}/auth')
app.include_router(summ_router, tags = ['Summarization'], prefix = f'/{config.API_VERSION}/summarize')

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/ping")
def read_root():
    return {"message": "pong"}