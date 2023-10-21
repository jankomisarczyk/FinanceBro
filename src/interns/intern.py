from __future__ import annotations

from typing import Type, Union, TYPE_CHECKING
from src.interns.step import Step
from src.interns.status import Status

if TYPE_CHECKING:
    from src.financebro.financebro import FinanceBro
    from src.interns.specialization import Specialization



class Intern:
    financebro: FinanceBro
    specialization: Type[Specialization]
    instructions: str
    inputs: list[str]
    outputs: list[str]
    complete: bool
    steps: list[Step]
    status: Status

    def __init__(self,
                 financebro: FinanceBro = None, 
                 specialization: Type[Specialization] = None, 
                 instructions: str = None, 
                 inputs: list[str]  = None,
                 outputs: list[str] = None,
                 complete: bool = False):
        self.financebro = financebro
        self.specialization = specialization
        self.instructions = instructions
        self.inputs = inputs
        self.outputs = outputs
        self.complete = complete
        self.status = Status()

    def do_step(self) -> Union[Step, None]:
        if self.complete:
            return None

    def create_step():
        pass
