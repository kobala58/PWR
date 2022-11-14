from pydantic import BaseModel
from fastapi import FastAPI
import json
from multiprocessing import Process
import iot_source.data_sender
from fastapi.middleware.cors import CORSMiddleware

process = Process(iot_source.data_sender.sender())


class NewConfig(BaseModel):
    method: str
    port: str
    interval: int
    source: str
    channel: str


app = FastAPI(root_path="l3/iot_source")

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
    with open("iot_source/config.json", "r") as data:
        test = json.load(data)
        return {
            "config": "DUPA"
        }


@app.post("/update/config/")
async def update_config(conf: NewConfig):
    with open("iot_source/config.json", "r") as jsonfile:
        data = json.load(jsonfile)
    print(data)
    for key, val in conf:
        data[key] = val
    with open("iot_source/config.json", "w") as jsonfile:
        json.dump(data, jsonfile)
    process.terminate()
    process.start()
    return {
        "status": "updated",
        "config": data
    }


@app.on_event('startup')
async def start():
    process.start()
