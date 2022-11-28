import asyncio
import time
import datasources
import requests
import json
import mqtt_sender
import paho.mqtt.publish as publish


async def sender():
    while True:
        with open("config.json", "r") as data:
            settings = json.load(data)

        payload = datasources.get_ask_price(settings["source"])
        
        if settings["method"] == "REST":
            requests.post(f"http://{settings['server']}:{settings['port']}{settings['channel']}", json=payload)
        
        elif settings["method"] == "MQTT":
            publish.single(
                    topic=settings["channel"],
                    payload = str(payload),
                    hostname = settings["server"],
                    )
        else:
            raise ValueError("Suitable method not found, try using REST/MQTT params")
        await asyncio.sleep(int(settings["interval"]))

if __name__ == '__main__':
    pass
