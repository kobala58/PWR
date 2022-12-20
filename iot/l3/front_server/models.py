from pydantic import BaseModel
from enum import Enum

class IntervalTime(Enum):
    COUNT = "count"
    TIME = "time"
    

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

class Gatherer(BaseModel):
    walor: str
    type_interval: IntervalTime
    interval_value: int # seconds or count

class AggregatorData(BaseModel):
    walor: str
    bid_min: float 
    bid_max: float
    bid_avg: float
