from pydantic import BaseModel

class Config(BaseModel):
    svr_id: str
    method: str
    port: str
    interval: int
    source: str
    channel: str
    server: str

class CreateParams(BaseModel):
    name: str
    method: str
    port: str
    interval: int
    source: str
    channel: str
    server: str

class Payload(BaseModel):
    time: int
    walor: str
    bid: str
    ask: str
