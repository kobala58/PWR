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
        return {
                "status": "success",
                "value": data
                }
    except ValueError:
        return {
                "status": "fail",
                "value": "Instrument not found"
                }

