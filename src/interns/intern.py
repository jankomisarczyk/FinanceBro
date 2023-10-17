from src.interns import Specialization
from typing import Type

class Intern:
    specialization: Type[Specialization]
    instructions: str
    inputs: list[str]
    outputs: list[str]
    complete: bool

    def __init__(self, 
                 specialization: Type[Specialization] = None, 
                 instructions: str = None, 
                 inputs: list[str]  = None,
                 outputs: list[str] = None,
                 complete: bool = False):
        self.specialization = specialization
        self.instructions = instructions
        self.inputs = inputs
        self.outputs = outputs
        self.complete = complete
