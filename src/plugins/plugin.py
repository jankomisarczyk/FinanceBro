from src.llmopenai import Function, Parameters, Argument
from abc import ABC, abstractclassmethod
from typing import List, Optional, Dict

class Plugin(ABC):
    name: str
    description: str
    args_schema: Dict[str, Argument]
    required: List[str]
    categories: Optional[List[str]] = None

    @abstractclassmethod
    def arun(self, *args, **kwargs):
        pass

    def to_openai_function(self):
        return Function(
            name=self.name,
            description=self.description,
            parameters=Parameters(
                properties=self.args_schema,
                required=self.required
            )
        )