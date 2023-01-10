import json
from typing import List
from pydantic import BaseModel
from enum import Enum
import os
from datetime import datetime, timezone
import redis
import requests
import asyncio

class Config(BaseModel):
    services: list 
    interval_value: str
    target: str

def overwrite_config():
    """
        This funcion is called whenever OS ENV variable is set upon creating docker container
    """

    with open("config.json", "r") as jsonfile:
        data = json.load(jsonfile)

    for x in ["interval_value","target"]:
        data[x.lower()] = os.environ[x]

    data["services"] = [x.split() for x in os.environ["SERVICES"]]
    
    with open("config.json", "w") as jsonfile:
        json.dump(data, jsonfile)

def filter_grabber(walors: List[str]) -> list:
    r = redis.Redis(host="0.0.0.0", port=6379, db=0, decode_responses=True)
    data = []
    for walor in walors:
        read = r.hgetall(walor+"_v")
        data.append(read)
    return data

async def send_data_to_config():
    """
    get lates 
    """
    while True:    
        with open("config.json", "r") as jsonfile:
            config = json.load(jsonfile)
        data = filter_grabber(config["services"])
        payload = {
                'status': 'OK',
                'values': data
                }
        print(payload)
        requests.post(config["target"], json = payload)
        await asyncio.sleep(int(config["interval_value"]))


if __name__ == "__main__":
    filter_grabber(["BITCOIN", "USDPLN", "DUPA"])
