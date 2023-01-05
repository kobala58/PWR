from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import utils

app = FastAPI()

@app.get("/")
async def config(): 
    with open("config.json", "r") as jsonfile:
        return jsonfile

@app.post("/change_config")
async def config_change(config: utils.Config):
    with open("config.json", "r") as jsonfile:
        data = json.load(jsonfile)
    print(data)
    for key, val in config:
        data[key] = val
    with open("config.json", "w") as jsonfile:
        json.dump(data, jsonfile)
    return {
        "status": "updated",
        "config": data
    }

@app.on_event('startup')
async def est_conn():
    if "METHOD" in os.environ:
        utils.overwrite_config()

