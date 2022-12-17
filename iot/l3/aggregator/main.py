from fastapi import FastAPI
from pydantic import BaseModel
import json
import os


app = FastAPI()


@app.post("/data")
async def get_Data(data: Payload):
    pass


@app.get("/temp"):



@app.on_event('startup')
async def est_conn():
    if "METHOD" in os.environ:
        overwrite_config()
