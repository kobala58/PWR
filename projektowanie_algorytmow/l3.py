from enum import Enum
from dataclasses import dataclass
from typing import Dict

# TODO:
# detect first position 
# transfrom letter into another letter
# move left and right
# 

class Moves(Enum):
    LEFT = "l"
    RIGHT = "r"
    TRANSFORM = "t"
    NONE = "r"

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
    lang: Language
    nodes: Dict
    end_node: list
    start_node: str = "q"

    def __post_init__(self):
        
        self.pos = 0
        self.curr_node = ""

    def create_nodes_from_dict(self, nodes_l: dict):
        tmp_nodes = []
        for key, val in nodes_l.items():
            tmp_node = Node.from_dict(key, val)
            tmp_nodes.append(tmp_node)
        
        print("Nodes created succesfully")

    def __str__(self) -> str:
        return "Kek"

    def check_integrity(self, word: str) -> bool:
        """Check if word is valid"""

        return set(word).issubset(set(self.lang.symbols))
    
    def run_test(self, word: str):
        """
        Method to run word in language
        """
        # WARNING - spaghetti below
        # check if word is even valid in this language
        if not self.check_integrity(word):
            print("Word is not valid in this lang")
            return False
        print(f"---START---\nTesting word {word}")
        # catch not implemented lang or nodes
        if self.nodes == []:
            return [False, "Nodes list is empty"]
        if self.lang.symbols == ():
            return [False, "Lang is not provided"]
        
        next_node = self.start_node
        # for letter in word:
        #     # grab start node
        #     nn = next_node
        #     # move to next node
        #     next_node = self.nodes[next_node][letter]
        #     print(f"Moved from {nn} to {next_node} by letter {letter}")
        
        cnt = 0 
        word = [x for x in word]

        while (cnt != -1) or (cnt == len(word)):
            nn = next_node
            tmp = self.nodes[next_node][word[cnt]]["to"]
            # if rename exists 
            if self.nodes[next_node][word[cnt]]["rename"] is not None:
                word[cnt]=self.nodes[next_node][word[cnt]]["rename"]
            
            # now cnt manipulation

            match self.nodes[next_node][word[cnt]]["direction"]:
                case "left":
                    cnt -= 1
                case "right":
                    cnt += 1

            
        # results
        print("\n\n---Result---")
        if next_node in self.end_node:
            print(f"Word {word} is valid")
        else:
            print(f"Word {word} is invalid")
        print("\n\n")


def ex1():
    rho2 = {
            "q0": {"a": {"to": "q1",
                         "rename": "a_dot",
                         "direction": "left"
                         }}
            }

    ex1 = Machine(
            start_node="q0",
            end_node=["q3"],
            lang=Language(("0","1")),
            nodes=rho
            )
    # ex1.run_test("1100101011")
    # ex1.run_test("11100")
    ex1.run_test(input("Enter word in lang: "))


if __name__ == "__main__":
    ex1()
