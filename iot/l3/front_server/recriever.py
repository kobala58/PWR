from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
from servers_mainipulation import DockerOperations
import requests
import models
import db
from fastapi.middleware.cors import CORSMiddleware
import random
import json
import requests


# TODO -> MOVE TO CONTAINER 
# REMOVE MQTT SUPPORT


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
    """
    Return active server list (at least i hope so)
    """
    data = db.get_all_servers()
    return data

@app.post("/change_config/{name}")
async def update_server_settings(name: str, conf: models.Config):
    """
    Update server config file via REST service
    """

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
    """
    Clear existing images and databases entries
    """

    drv = DockerOperations()
    res2 = db.clear_server()
    return True

@app.post("/data")
async def recv_data(data: models.Payload):
    """
    Data entry endpoint 
    """
    # TODO idk why i need to implement this endpoint

    print(data)

@app.post("/aggregator/upload/config")
async def aggregator_config(data: models.Gatherer): 
    """
        Endpoint to update config of aggregator microservice
    """
    # make request to change config

    res = requests.post("http://0.0.0.0:8081/config", json=data.json()) #hard coded solution - not nice
    return res.text

@app.post("/aggregator")
async def aggregator_data(data: models.AggregatorData):
    """
    Endpoint to handle data from aggregator
    """
    print("--Aggregator--")
    print(data)
    print("------")

@app.get("/generator/{name}/config")
async def get_server_info(name: str):
    """
    Endpoint handling config of requested service
    """
    data = requests.get(f"http://{name}:80/").json()
    return data

@app.post("/generator/create_new")
async def create_generator(conf: models.CreateParams):
    """
    Endpoint to handle creation of new generator
    """
    dvr = DockerOperations()
    data = dvr.spawn_new_container(conf)
    # db.insert_new_server(data["short_id"], conf.name, conf.method, conf.port, conf.interval, conf.source, conf.channel, conf.server, data["port"])
    return data

@app.post("/generator/create_empty")
async def create(conf: models.CreateParams):
    """
    Create Empty generatir config
    """
    db.insert_new_server("FAKE", conf.name, conf.method, conf.port, conf.interval, conf.source, conf.channel, conf.server, random.randint(8000, 8250))
    return ["FAKE", random.randint(8000, 8250)]

@app.post("/filter/data")
async def filter_data(data: models.FilterData):
    print("----")
    print("Recrived from filter")
    print(data)
    print("----")


@app.post("/filter/create")
async def filter_create():
    """
    Endpoint to create new filter endpoint
    """
    pass

@app.post("/filter/config/edit")
async def filter_edit_config(config: models.FilterConfig):
    """
    Endpoint for editing filter
    """ 
    res = requests.post(
            "http://0.0.0.0:8083/config",
            json=config.dict(),
            headers={"Content-Type": "application/json; charset=utf-8"}
            ) #hard coded solution - not nice
    return res.json()
    

@app.get("/filter/{name}/config")
async def filter_show_config(name: str):
    """
    Endpoint for showing config of selected filter
    """
    pass
# MQTT METGODS
# TODO Move MQTT-relate functions to outside file
# TODO Remove mqtt method to make moving into Container possible
@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/data") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    dec_payload = payload.decode().replace("\'", "\"") # replace to double-quoted bc JSON requires this 
    dec_jsos  = json.loads(dec_payload)
    # print(type(dec_jsos))
    # print(dec_jsos)
