from dataclasses import dataclass

@dataclass
class Language():
    symbols = ()

@dataclass
class Node():
    name: str

    def __post_init__(self):
        self.directions = {}
    
    def add_direction(self, node_name: str, value: str):
        self.directions[value] = node_name
    
    @classmethod
    def from_dict(cls, data: dict):
        obj = cls(data.keys()[0])
        obj.add_direction()

    def move(self, val: str):
        """Method to move to next node based on provided value"""
        return self.directions[val]

    def __str__(self) -> str:
        return str(self.directions)

@dataclass()
class Machine():
    """
    Class for simulating 
    """


if __name__ == "__main__":
    bin = Language((0,1))
    rho = {
            "q0": {0: "q1", 1: "q0"},
            "q1": {0: "q3", 1: "q2"},
            "q2": {0: "q2", 1: "q0"},
            "q3": {0: "q2", 1: "q2"},
            }
    nodes = []
