from __future__ import annotations

from typing import Union, List, TYPE_CHECKING
from src.interns.step import Step
from src.interns.status import Status
import json

if TYPE_CHECKING:
    from src.financebro.financebro import FinanceBro
    from src.interns.specialization import Specialization



class Intern:
    financebro: FinanceBro
    specialization: Specialization
    instructions: str
    inputs: List[str]
    outputs: List[str]
    complete: bool
    steps: List[Step]
    status: Status

    def __init__(self,
                 financebro: FinanceBro = None, 
                 specialization: Specialization = None, 
                 instructions: str = None, 
                 inputs: List[str]  = None,
                 outputs: List[str] = None,
                 complete: bool = False):
        self.financebro = financebro
        self.specialization = specialization
        self.instructions = instructions
        self.inputs = inputs
        self.outputs = outputs
        self.complete = complete
        self.status = Status()
        self.steps = []

    @property
    def current_step(self) -> Union[Step, None]:
        return self.steps[-1] if self.steps else None
    
    def compile_history(self) -> str:
        step_table = []

        for step in self.steps:
            if not step.execution:
                continue

            tool_arg_list = [
                f"{name}={json.dumps(value)}"
                for name, value in step.decision.tool_args.items()
            ]
            tool_args = ", ".join(tool_arg_list)
            
            step_table.append(f">>> {step.decision.tool_name}({tool_args})")
            step_table.append(step.execution)

        if not step_table:
            return ""
        
        header = (
                "# History:\n## The AI Assistant has a history of functions and outputs that the AI Assistant has already executed for this "
                "task. Here is the history, in order, starting with the first function executed:\n"
            )
        return header + "\n".join(step_table)
        
    def compile_files(self) -> str:
        files_table = []

        for name, description in self.financebro.global_files.items():
            if description:
                file_row = f'"""{name}""" contains {description}'
                files_table.append(file_row)

        if not files_table:
            return ""

        header = (
            "\n# Files\n## The AI Assistant has access to the following files. "
            'Each file name is enclosed in triple quotes ("""):\n'
        )
        return header + "\n".join(files_table)
    
    def compile_global_variables(self) -> str:
        variable_table = []

        for name, value in self.financebro.global_variables.items():
            if value:
                variable_row = f'{name} = """{value}"""'
                variable_table.append(variable_row)

        if not variable_table:
            return ""

        header = (
            "\n# Variables\n## The AI Assistant has access to these global variables. "
            'Each variable is a string with the value enclosed in triple quotes ("""):\n'
        )
        return header + "\n".join(variable_table)
    
    def compile_functions(self) -> str:
        function_table = []
        for plugin in self.specialization.PLUGINS.values():
            function_table.append(plugin.to_functions_list())
        
        return "\n".join(function_table)
    
    def prompt_kwargs(self) -> dict[str, str]:
        task = self.instructions
        variables = self.compile_global_variables()
        files = self.compile_files()
        history = self.compile_history()
        functions = self.compile_functions()

        return {
            "task": task,
            "functions": functions,
            "file_list": files,
            "variables": variables,
            "history": history,
        }

    async def do_step(self) -> Union[Step, None]:
        if self.complete:
            return None
        
        self.steps.append(Step())
        self.current_step.intern_name = self.specialization.NAME

        #planning
        self.status.plan()
        prompt_variables = self.prompt_kwargs()
        plan = await self.specialization.plan(prompt_variables)
        self.current_step.plan = plan

        #deciding
        self.status.decide()
        prompt_variables["plan"] = plan
        decision = await self.specialization.decide(prompt_variables)
        self.current_step.decision = decision

        #executing
        self.status.execute()
        execution = await self.specialization.execute(decision)
        self.current_step.execution = execution

        if self.current_step.execution.complete:
            self.complete = True

        return self.current_step

