from os import wait
import psutil
import time
from paho.mqtt import client as mqtt_client
import json

 
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client("1314")
    client.on_connect = on_connect
    client.connect("localhost", 1883)
    return client


def publish(client):
    while True:
        time.sleep(2)
        data = {
            "timestamp": time.time(),
            "val": psutil.sensors_temperatures()['nvme'][0].current
            }
        result = client.publish("/cpu", str(data))
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{data}` to topic \cpu")
        else:
            print(f"Failed to send message to topic \cpu")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
      
