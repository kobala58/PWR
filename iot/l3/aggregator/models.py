from pydantic import BaseModel

class Config(BaseModel):
    name: str
    method: str
    sender_port: int
    channel: str
    server: str

