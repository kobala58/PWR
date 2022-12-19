from docker.api import container
from docker.api.build import random
import pydantic
import db
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

    def spawn_new_container(self, conf = pydantic.BaseModel):
        port = random.randint(8000, 8250)
        envvars = {key.upper():val for key,val in dict(conf).items()}
        resp = self.client.containers.run("iot_data_sender:1.2",
                                    detach = True,
                                    ports = {'80/tcp':port},
                                    name = conf.name,
                                    environment = envvars,
                                    network = "iot",
                                    extra_hosts = {"host.docker.internal":"172.18.0.1"}
                                   )
        
        return{
                "short_id": resp.short_id,
                "port": port,
                "name": resp.name
                }
    
    def clear(self):
        # Todo: rewrite it to only clean images present in database
        for x in self.all_containers():
            if x["name"] != "mosquitto":
                self.client.containers.get(x["short_id"]).stop()
        return True
