import time
from fastapi import FastAPI, responses
from fastapi_mqtt import FastMQTT, MQTTConfig
from servers_mainipulation import DockerOperations
import requests
import models
import db
from fastapi.middleware.cors import CORSMiddleware
import random
import json
import requests

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

mqtt.init_app(app)



@app.get("/server_list")
async def server_list():
    data = db.get_all_servers()
    return data

@app.post("/change_config/{name}")
async def update_server_settings(name: str, conf: models.Config):
    port = db.get_server_info(name)
    print(port)
    print(port[0][0])
    res = requests.post(f"http://localhost:{port[0][0]}/update/config/", json={
        "method": conf.method,
        "port": conf.port,
        "interval": conf.interval,
        "source": conf.source,
        "channel": conf.channel,
        "server": conf.server
        })
    db.edit_server((conf.method, conf.port, conf.interval, conf.source, conf.channel, conf.server, name))
    return res.json()

@app.get("/clear")
async def clear():
    drv = DockerOperations()
    # res = drv.clear() -> Temporary solution until I provide way to stop and clean only generators
    res2 = db.clear_server()
    return True

@app.post("/data")
async def recv_data(data: models.Payload):
    print(data)

@app.post("/aggregator/upload/config")
async def aggregator_config(data: models.Gatherer): 
    """
    method to update config of aggregator
    TODO: make aggregator spawnable via docker
    """
    # make request to change config
    res = requests.post("http://0.0.0.0:8081/config", json=data.json())
    return res.text

@app.post("/aggregator")
async def aggregator_data(data: models.AggregatorData):
    print(data)

@app.get("/get_server_config/{name}")
async def get_server_info(name: str):
    data = requests.get(f"http://{name}:80/").json()
    return data

@app.post("/create_new")
async def create(conf: models.CreateParams):
    dvr = DockerOperations()
    data = dvr.spawn_new_container(conf)
    db.insert_new_server(data["short_id"], conf.name, conf.method, conf.port, conf.interval, conf.source, conf.channel, conf.server, data["port"])
    return data

@app.post("/create_empty")
async def create(conf: models.CreateParams):
    # dvr = DockerOperations()
    # data = dvr.spawn_new_container(conf)
    db.insert_new_server("FAKE", conf.name, conf.method, conf.port, conf.interval, conf.source, conf.channel, conf.server, random.randint(8000, 8250))
    return ["FAKE", random.randint(8000, 8250)]


#MQTT METGODS

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/data") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    dec_payload = payload.decode().replace("\'", "\"") # replace to double-quoted bc JSON requires this 
    dec_jsos  = json.loads(dec_payload)
    print(type(dec_jsos))
    print(dec_jsos)
