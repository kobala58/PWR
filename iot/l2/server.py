from fastapi import FastAPI
from pydantic import BaseModel
import time
import json

from requests.sessions import Request
recent_data = []
app = FastAPI()


class TmpData(BaseModel):
    tmp: float
    timestamp: float


@app.get("/")
async def root():
    return recent_data

@app.post("/data")
async def data(req: TmpData):
    print(req)
    global recent_data 
    recent_data = req
    return {"message": True}

