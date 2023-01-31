import json
from pydantic import BaseModel
from enum import Enum
import os
from sql import Queries 
from datetime import datetime
from datetime import timezone
import redis
import requests

class AggregatorType(str, Enum):
    COUNT = "count"
    INTERVAL = "interval"

class Config(BaseModel):
    name: str
    method: str
    sender_port: int
    channel: str
    server: str


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

def overwrite_config():
    """
        This funcion is called whenever OS ENV variable is set upon creating docker container
    """

    with open("config.json", "r") as jsonfile:
        data = json.load(jsonfile)

    for x in ["METHOD", "PORT", "CHANNEL", "SERVER", "TYPE_INTERVAL", "INTERVAL_VALUE"]:
        data[x.lower()] = os.environ[x]
    
    with open("config.json", "w") as jsonfile:
        json.dump(data, jsonfile)

def send_data_to_config():
    pass

def save_message_to_database(data: dict) -> bool:
    r = redis.Redis(host="cache", port=6379, db=0, decode_responses=True)
    r.incr(data["walor"])
    r.hset(data["walor"]+"_v", mapping=data)
    counter = r.get(data["walor"])
    drv = Queries()
    with open("config.json", "r") as jsonfile:
        config = json.load(jsonfile)
    if int(config["interval_value"]) <= int(counter):
        res = drv.select_top_walor(data["walor"], int(config["interval_value"]))
        send_data_to_server(list(res), data["walor"])
        r.set(data["walor"], 0)
    else:
        print(f"{data['walor']}: {counter}")
    payload = (data["walor"],
        datetime.fromtimestamp(data["time"], tz=timezone.utc),
        data["bid"],
        data["ask"])
    drv.insert_val(payload)

def send_data_to_server(data, walor):
    payload = {
            "walor": walor,
            "bid_min": data[0],
            "bid_max": data[1],
            "bid_avg": data[2]
            }
    print(payload)
    requests.post("http://172.18.0.1:8080/aggregator", json=payload)


