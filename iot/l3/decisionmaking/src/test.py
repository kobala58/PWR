from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
from fastapi.middleware.cors import CORSMiddleware
import os
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

data = "dupa"
 
@app.get("/config")
async def ex_8_Impl():
    return "In development"

@app.get("/state")
async def state():
    global data

    return data



#MQTT METHODS

mqtt.init_app(app)
@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/heater/temp") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)
    print("test")

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    dec_payload = payload.decode().replace("\'", "\"") # replace to double-quoted bc JSON requires this 
    dec_jsos  = json.loads(dec_payload)
    print(dec_jsos)
