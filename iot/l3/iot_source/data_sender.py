import time
import iot_source.datasources
import requests
import json
import iot_source.mqtt_sender


def sender():
    with open("iot_source/config.json", "r") as data:
        settings = json.load(data)
    if settings["method"] == "REST":
        while True:
            payload = iot_source.datasources.get_ask_price(settings["source"])
            requests.post("localhost:" + str(settings["port"]), json=payload)
            time.sleep(settings["interval"])
    elif settings["method"] == "MQTT":
        iot_source.mqtt_sender.run()
    else:
        raise ValueError("Suitable method not found, try using REST/MQTT params")


if __name__ == '__main__':
    sender()
