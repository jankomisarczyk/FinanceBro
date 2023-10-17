import logging
import os.path
from typing import Union, Type

from src.config import Config
from src.decomposer import Decomposer
from src.interns import Specialization, Intern

logger = logging.getLogger(__name__)


class FinanceBro:
    task: str
    # saved Documents from previous steps done by interns
    # TODO implement Documents
    observations: list[str("Documents")]
    # Variables set / exported by interns
    global_variables: dict[str, str]

    interns = list[Intern]
    specialisation_registry: dict[str, Type[Specialization]]
    decomposer: Decomposer
    config: Config

    def __init__(self, task: str = "", config: Config = None):
        self.task = task
        self.config = config or Config.global_config()
        self.interns = []
        self.observations = []
        self.global_variables = {}
        self.specialisation_registry = {spec.NAME:spec for spec in Specialization.__subclasses__()}
        self.decomposer = Decomposer(
            task=task, 
            specialisation_registry=self.specialisation_registry, 
            model=self.config.decomposer_model)


        if not os.path.exists(self.config.workspace_path):
            os.makedirs(self.config.workspace_path, exist_ok=True)

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

        await self.current_intern.create_new_step()

        await self.save()

    async def cycle(self) -> str("Step"):
        # TODO implement Step that goes through intern
        """Step through one decide-execute-plan loop"""
        if self.is_done:
            return

        intern = self.current_intern
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
            specialization = self.specialisation_registry[step["agent"]]()
            intern = Intern(
                specialization=specialization,
                instructions=step["instructions"],
                inputs=step["inputs"],
                outputs=step["outputs"]
            )
            self.interns.append(intern)