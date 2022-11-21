import time
from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
from pydantic import BaseModel 
from servers_mainipulation import DockerOperations
import requests

mqtt_config = MQTTConfig(host = "mosquitto2",
    port= 1883,
    keepalive = 60)

app = FastAPI()

mqtt_config = MQTTConfig()

mqtt = FastMQTT(
    config=mqtt_config
)

mqtt.init_app(app)

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


@app.get("/server_list")
async def server_list():
    drv = DockerOperations()
    return drv.all_containers()

@app.post("/change_config")
async def update_server_settings(conf: Config):
    """
    Endpoint to change
    """ 
    pass

@app.get("/clear")
async def clear():
    drv = DockerOperations()
    drv.clear()

@app.post("/data")
async def recv_data(data: Payload):
    print(data)
    

@app.get("/get_server_config")
async def get_server_info(id: str):
    pass

@app.post("/create_new")
async def create(conf: CreateParams):
    dvr = DockerOperations()
    data = dvr.spawn_new_container(conf.name)
    time.sleep(5)
    requests.post("localhost:"+str(data["port"])+"/update/config/", json={
        "method": conf.method,
        "port": conf.port,
        "interval": conf.interval,
        "source": conf.source,
        "channel": conf.channel,
        "server": conf.server
        })    



#MQTT METGODS

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/data") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)
