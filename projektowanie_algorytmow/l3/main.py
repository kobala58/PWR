from dataclasses import dataclass
from typing import Dict, List
import json

@dataclass()
class TuringMachine:
    nodes: List[str]
    start_node: str
    accept_node: List[str]
    rejecting_node: List[str]
    lang: List[str]
    edges: Dict
    
    @classmethod
    def read_from_json(cls, jfile: str):
        with open(jfile+".json") as file:
            data = json.load(file)
        
        return cls(data["nodes"], data["start_node"],
                   data["accept_node"], data["rejecting_node"],
                   data["lang"], data["edges"])

    def run_word(self, word: str):
        if not self.valid_word(word):
            print(f"Invalid word: {word}")

        tape = [x for x in word]
        # for _ in range(3):
            # tape.append("_")
        tape.append("_")
        curr_node = self.start_node
        print(curr_node, tape)
        idx = 0

        while True:

            if curr_node in self.accept_node:
                print("Accepted")
                break
            if curr_node in self.rejecting_node:
                print("Rejected")
                break
            
            old_tape = tape[idx]
            old_state = curr_node
            tape[idx] = self.edges[curr_node][old_tape][0]
            curr_node = self.edges[curr_node][old_tape][1]
            print(curr_node, tape, self.edges[old_state][old_tape][2])

            if self.edges[old_state][old_tape][2] == "R":
                idx += 1
                if idx == len(tape) - 1: # detect end
                    tape.append("_")
            else: #detect left movment
                if idx == 0:
                    continue
                else:
                    idx -= 1



    def valid_word(self, word) -> bool:
        print(set(word))
        print(set(self.lang))
        return set(word).issubset(set(self.lang))


def ex1():
    test = TuringMachine.read_from_json("e1")
    # test.run_word(input("Podaj slowo: "))
    test.run_word("aaaaa")

def ex2():
    test = TuringMachine.read_from_json("e2")
    test.run_word("1b1")

def ex3():
    print("---E3---")
    test = TuringMachine.read_from_json("e3")
    test.run_word("x")
    # test.run_word("hexhf")
    # test.run_word("hexhff")

def ex4():
    print("---E4---")
    test = TuringMachine.read_from_json("e4")
    test.run_word("[(01,11),(10,11)#01,11,10]")
    
if __name__ == "__main__":
    ex1()
    ex2()
    ex3()
    ex4()
    # ex5()
