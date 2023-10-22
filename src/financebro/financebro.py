import logging
import os.path
from typing import Union, Type, List, Dict

from src.interns.intern import Intern
from src.interns.specialization import Specialization
from src.config import Config
from src.decomposer.decomposer import Decomposer
    
    
    

logger = logging.getLogger(__name__)


class FinanceBro:
    task: str
    # saved Documents from previous steps done by interns
    # TODO implement Documents
    observations: List[str("Documents")]
    # Variables set / exported by interns key:value
    global_variables: Dict[str, str]
    # Files created by interns and their description name:summary
    global_files: Dict[str, str]

    interns: List[Intern]
    specialisation_registry: Dict[str, Type[Specialization]]
    decomposer: Decomposer
    config: Config

    def __init__(self, task: str = "", config: Config = None):
        self.task = task
        # do I need this ???
        self.config = config or Config()
        self.interns = []
        self.observations = []
        self.global_variables = {}
        self.global_files = {}
        self.specialisation_registry = {spec.NAME:spec for spec in Specialization.__subclasses__()}
        self.decomposer = Decomposer(
            task=task, 
            specialisation_registry=self.specialisation_registry, 
            model=self.config.decomposer_model)

        if not os.path.exists(self.config.workspace_path):
            os.makedirs(self.config.workspace_path, exist_ok=True)

    @property
    def global_variables(self) -> Dict[str, str]:
        return self.global_variables
    
    @global_variables.setter
    def global_variables(self, value) -> None:
        if isinstance(value, dict):
            for key in value:
                if key in self.global_variables:
                    print(f"Overwriting global variable {key}:{self.global_variables[key]} with new value {value[key]}")
                self.global_variables[key] = value[key]
        else:
            raise ValueError("To add a global variable it must be in dictionary")
        
    @property
    def global_files(self) -> Dict[str, str]:
        return self.global_files
    
    @global_files.setter
    def global_files(self, value) -> None:
        if isinstance(value, dict):
            for key in value:
                if key in self.global_files:
                    print(f"Overwriting global file description {key}:{self.global_files[key]} with new value {value[key]}")
                self.global_files[key] = value[key]
        else:
            raise ValueError("To add a global file it must be in dictionary")

    @property
    def current_intern(self) -> Union[Intern, None]:
        try:
            return next(
                intern
                for intern in self.interns
                if not intern.complete
            )
        except StopIteration:
            return None

    @property
    def is_done(self):
        return self.current_intern is None

    async def setup(self):
        await self.decompose_task()

    async def cycle(self) -> str("Step"):
        # TODO implement Step that goes through intern
        """Step through one decide-execute-plan loop"""
        if self.is_done:
            return

        intern = self.current_intern
        # each intern plans, rapairs, decide and execute a step
        step = await intern.cycle()

        # If this subtask is complete, prime the next subtask
        if intern.complete:
            next_intern = self.current_intern
            # We're done
            if not next_intern:
                return None

            if not next_intern.current_step:
                await next_intern.create_new_step()

            if next_intern:
                documents = await intern.current_step.documents
                for name, document in documents.items():
                    if name in next_intern.inputs:
                        await next_intern.current_step.add_document(document)

        # logger(
        #     "CycleComplete",
        #     payload={
        #         "oversight": step.oversight.__dict__ if step.oversight else None,
        #         "plan": step.plan.__dict__ if step.plan else None,
        #         "decision": step.decision.__dict__ if step.decision else None,
        #         "observation": step.observation.__dict__ if step.observation else None,
        #     },
        # )

        return step

    async def decompose_task(self):
        """Turn the initial task of financebro into subtasks that are executed by their interns"""
        decomposed = await self.decomposer.decompose()
        for step in decomposed:
            # WHAT other arguments need intern ?? TODO
            specialization = self.specialisation_registry[step["agent"]](
                llm_planner=self.config.planner_model,
                llm_decider=self.config.decider_model
            )
            
            intern = Intern(
                financebro=self,
                specialization=specialization,
                instructions=step["instructions"],
                inputs=step["inputs"],
                outputs=step["outputs"],
                global_variables=self.global_variables,
                global_files=self.global_files
            )
            self.interns.append(intern)