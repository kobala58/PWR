import json
from pydantic import BaseModel
from enum import Enum
import os

class AggregatorType(str, Enum):
    COUNT = "count"
    INTERVAL = "interval"


def overwrite_config():
    """
        This funcion is called whenever OS ENV variable is set upon creating docker container
    """

    with open("config.json", "r") as jsonfile:
        data = json.load(jsonfile)

    for x in ["METHOD", "PORT", "INTERVAL", "SOURCE", "CHANNEL", "SERVER"]:
        data[x.lower()] = os.environ[x]
    
    with open("config.json", "w") as jsonfile:
        json.dump(data, jsonfile)

class Payload(BaseModel):
    time: int
    walor: str
    bid: str
    ask: str

class GatherPayload(BaseModel):
    walor: str 
    type: AggregatorType
    interval: int
    count: int = 5

