from os import wait
import time
from paho.mqtt import client as mqtt_client
import json
import datasources


def connect_mqtt(settings):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client("test")
    client.on_connect = on_connect
    client.connect("172.17.0.2", settings["port"])
    return client


def publish(client, settings):
    data = datasources.get_ask_price(settings["source"])
    result = client.publish(settings["channel"], str(data))
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{data}` to topic {settings['channel']}")
    else:
        print(f"Failed to send message to topic")


def run():
    with open("./config.json", "r") as data:
        settings = json.load(data)
    client = connect_mqtt(settings)
    client.loop_start()
    publish(client, settings)


if __name__ == '__main__':
    run()
