from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

class NodeTypes(Enum):
    START = "start"
    END = "end"
    NORMAL = "normal"

@dataclass
class Language():
    symbols: tuple
    

@dataclass
class Node():
    name: str
    
    def __post_init__(self):
        self.directions = {}
    
    def add_direction(self, node_name: str, value: str):
        self.directions[value] = node_name
    
    @classmethod
    def from_dict(cls, key: str, data: dict):
        tmp = cls(key)
        for key, val in data.items():
            tmp.add_direction(node_name=key, value=val)
        
        print(f"Node check: \n{tmp.__str__()}\n-------------\n")
        return tmp

    def move(self, val: str):
        """Method to move to next node based on provided value"""
        return self.directions[val]

    def __str__(self) -> str:
        return f"Node name: {self.name}\nedges: {str(self.directions)}"

@dataclass()
class Machine():
    """
    Class for simulating machine 
    """
    start_node: str = "q"
    end_node: str = "q"
    nodes: Dict = {}
    lang: Language = Language(())

    def __post_init__(self):
        self.pos = 0
        
        # set up curr_node as start node
        self.curr_node = ""

    @classmethod
    def create_nodes_from_dict(cls, nodes_l: dict):
        tmp_nodes = []
        for key, val in nodes_l.items():
            tmp_node = Node.from_dict(key, val)
            tmp_nodes.append(tmp_node)
        
        print("Nodes created succesfully")

    def __str__(self) -> str:
        return "Chuj"

    def check_integrity(self) -> bool:
        """Check if language matches nodes edges"""
        nd = set()
        for node in self.nodes:
            for key,val in node.items():
                nd.add()
        # TODO 
        return True
    
    def run_test(self, word: list) -> List[bool, str]:
        """
        Method to run word in language
        """

        # catch not implemented lang or nodes
        if self.nodes == []:
            return [False, "Nodes list is empty"]
        if self.lang.symbols == ():
            return [False, "Lang is not provided"]
        
        for letter in word:
            # grab start node

            

        


if __name__ == "__main__":
    bin = Language((0,1))
    rho = {
            "q0": {0: "q1", 1: "q0"},
            "q1": {0: "q3", 1: "q2"},
            "q2": {0: "q2", 1: "q0"},
            "q3": {0: "q2", 1: "q2"},
            }

    nodes = []

    for key, val in rho.items():
        z = Node.from_dict(key, val)
