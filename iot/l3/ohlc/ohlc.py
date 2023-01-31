from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import utils


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def config(): 
    return utils.all_tools()

@app.get("/ohlc")
async def create_candles(instrument: str, time_unit: str, time_val: int):
    if time_unit not in ["minute", "minutes", "second", "seconds", "hour", "hours"]:
        return {
                "status": "fail",
                "value": "Time unit not found"
                }
    if (1 > time_val) or (100 < time_val):
        return {
                "status": "fail",
                "value": "Time value outside of range"
                }

    try:
        data = utils.generate_ohlc_values(instrument, time_unit, time_val)
        return data
    except ValueError:
        return {
                "status": "fail",
                "value": "Instrument not found"
                }

