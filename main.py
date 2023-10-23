from fastapi import FastAPI
from httpx import AsyncClient

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
