from dataclasses import dataclass

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
    nodes: list[Node] = []
    lang: Language = Language(())

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
 

de__name__ == "__main__":
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
