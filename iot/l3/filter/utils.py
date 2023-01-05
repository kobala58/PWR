import json
from typing import List
from pydantic import BaseModel
from enum import Enum
import os
from datetime import datetime, timezone
import redis
import requests
import asyncio

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
        requests.post(config["target"], json = payload)
        await asyncio.sleep(config["interval_value"])


if __name__ == "__main__":
    filter_grabber(["BITCOIN", "USDPLN", "DUPA"])
