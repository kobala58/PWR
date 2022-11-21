from pydantic import BaseModel
from fastapi import FastAPI
import json
import data_sender
from fastapi.middleware.cors import CORSMiddleware
import asyncio

class NewConfig(BaseModel):
    method: str
    port: str
    interval: int
    source: str
    channel: str
    server: str

with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def config():
    with open("config.json", "r") as data:
        test = json.load(data)
        return test


@app.post("/update/config/")
async def update_config(conf: NewConfig):
    with open("config.json", "r") as jsonfile:
        data = json.load(jsonfile)
    print(data)
    for key, val in conf:
        data[key] = val
    with open("config.json", "w") as jsonfile:
        json.dump(data, jsonfile)
    return {
        "status": "updated",
        "config": data
    }

import time
@app.on_event('startup')
async def daemon_startup() -> None:
    await asyncio.sleep(10)
    asyncio.create_task(data_sender.sender())
