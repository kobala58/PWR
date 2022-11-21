from docker.api import container
from docker.api.build import random
from db import main
import docker

class DockerOperations():
    def __init__(self) -> None:
        self.client = docker.from_env()

    def all_containers(self) -> list:
        data = []
        for x in self.client.containers.list():
            data.append(
                    {
                        "name": x.name,
                        "short_id": x.short_id
                        }
                    )
        return data
    
    def stop(self, id) -> dict[str, str | bool]: 
        try:
            container = self.client.containers.get(id)
        except docker.errors.NotFound:
            return {
                    "status": False,
                    "message": "Container not exist"
                    }
        try:
            container.stop()
            return {
                    "status": True,
                    "message": "Succesful"
                    }
        except docker.errors.APIError:
            return {
                    "status": False,
                    "message": "Interal API error"
                    }

    def spawn_new_container(self, name:str):
        port = random.randint(8000, 8250)
        resp = self.client.containers.run("iot_data_sender:0.9",
                                    detach = True,
                                    ports = {'80/tcp':port},
                                    name = name,
                                          # extra_hosts = {"host.docker.internal":"host-gateway"}
                                   )
        return{
                "short_id": resp.short_id,
                "port": port,
                "name": resp.name
                }
    
    def clear(self):
        for x in self.all_containers():
            if x["name"] != "mosquitto2":
                self.client.containers.get(x["short_id"]).stop()
