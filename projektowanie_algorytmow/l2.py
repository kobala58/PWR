from dataclasses import dataclass
from enum import Enum
from typing import Dict, List
import re
import json

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
        
        # set up curr_node as start node
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
        for letter in word:
            # grab start node
            nn = next_node
            next_node = self.nodes[next_node][letter]
            print(f"Moved from {nn} to {next_node} by letter {letter}")
        print("\n\n---Result---")

        if next_node in self.end_node:
            print(f"Word {word} is valid")
        else:
            print(f"Word {word} is invalid")
        print("\n\n")

def ex1():
    rho = {
            "q0": {"0": "q1", "1": "q0"},
            "q1": {"0": "q3", "1": "q2"},
            "q2": {"0": "q2", "1": "q0"},
            "q3": {"0": "q2", "1": "q2"},
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


def ex2():
    rho = {
            "q0": {"a": "q2", "b": "q2", "c": "q2"},
            "q1": {"a": "q4", "b": "q0", "c": "q3"},
            "q2": {"a": "q1", "b": "q1", "c": "q6"},
            "q3": {"a": "q3", "b": "q3", "c": "q3"},
            "q4": {"a": "q0", "b": "q5", "c": "q5"},
            "q5": {"a": "q4", "b": "q4", "c": "q4"},
            "q6": {"a": "q3", "b": "q3", "c": "q3"},
            }

    ex2 = Machine(
            start_node="q0",
            end_node=["q4", "q5"],
            lang=Language(("a","b","c")),
            nodes=rho
            )
    # ex1.run_test("1100101011")
    # ex1.run_test("11100")
    ex2.run_test(input("Enter word in lang: "))

def ex3(word: str):
    rho = {
            "q0": {"a": "q2", "0": "q3", "1": "q3"},
            "q1": {"0": "q1", "1": "q1", "a": "q2"},
            "q2": {"0": "q2", "1": "q2", "a":"q3"},
            "q3": {"0": "q3", "1": "q3", "a":"q3"}
            }
    
    mach = Machine(
                start_node="q0",
                end_node=["q3"],
                lang=Language(("0","1","a")),
                nodes=rho
                )

    mach.run_test(word)

def ex4(word: str):
    
    rho = {
            "q0": {"a": "q0", "b": "q2", "c": "q1", "d":"q1"},
            "q1": {"a": "q1", "b": "q1", "c": "q1", "d":"q1"},
            "q2": {"c": "q3", "a": "q1", "b":"q1", "d":"q1"},
            "q3": {"a": "q1", "b": "q1", "c":"q1", "d":"q3"}
            }
    
    mach = Machine(
                start_node="q0",
                end_node=["q3"],
                lang=Language(("a","b","c","d")),
                nodes=rho
                )

    mach.run_test(word)

def ex5(filename: str):    
    with open(filename+".json", "r") as file:
        data = json.load(file)
    
    Machine(
            start_node=data["start_node"],
            end_node = data["end_node"],
            lang = Language(tuple(data["lang"])),
            nodes = data["nodes"]
            ).run_test(data["text"])

if __name__ == "__main__":
    # ex2()
    # print(ex4("abcd"))
    # print(ex4("aaaabcd"))
    ex5("ex5")
