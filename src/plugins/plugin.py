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

    def to_openai_function(self) -> Function:
        return Function(
            name=self.name,
            description=self.description,
            parameters=Parameters(
                properties=self.args_schema,
                required=self.required
            )
        )
    
    def to_functions_list(self) -> str:
        args = []
        for arg_name, arg in self.args_schema.items():
            arg_type = arg.type
            if arg_type == "string":
                arg_type = "str"
            elif arg_type == "boolean":
                arg_type = "bool"
            elif arg_type == "integer":
                arg_type = "int"
            elif arg_type == "number":
                arg_type = "float"
            args.append(f"{arg_name}: {arg_type}")

        return f"{self.name}({', '.join(args)})"