from fastapi import FastAPI
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

import os

app = FastAPI()
client = AsyncIOMotorClient(os.getenv("CONNECTION_STRING"))

@app.get("/")
async def root():
    db_names = await client.list_database_names()
    return {"message": "Hello World", "dbs": db_names}
