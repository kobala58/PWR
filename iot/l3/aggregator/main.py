from fastapi import FastAPI
from pydantic import BaseModel

class Payload(BaseModel):
    time: int
    walor: str
    bid: str
    ask: str

app = FastAPI()


@app.post("/data")
async def get_Data(data: Payload):
    pass


@app.on_event('startup')
async def est_conn():
    pass
