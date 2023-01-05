from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
from fastapi.middleware.cors import CORSMiddleware
import os
import utils
import json

app = FastAPI()

mqtt_config = MQTTConfig(host = "172.18.0.2",
    port= 1883,
    keepalive = 60)

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


mqtt_config = MQTTConfig()

mqtt = FastMQTT(
    config=mqtt_config
)

@app.post("/ohlc")
async def get_ohlc_data():
    pass

@app.post("/data")
async def get_Data(data: utils.Payload):
    print(data)
    utils.save_message_to_database(data.dict())

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
 
@app.get("/temp")
async def ex_8_Impl():
    return "In development"


@app.on_event('startup')
async def est_conn():
    if "METHOD" in os.environ:
        utils.overwrite_config()

#MQTT METHODS

mqtt.init_app(app)
@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/data") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    dec_payload = payload.decode().replace("\'", "\"") # replace to double-quoted bc JSON requires this 
    dec_jsos  = json.loads(dec_payload)
    utils.save_message_to_database(dec_jsos)
