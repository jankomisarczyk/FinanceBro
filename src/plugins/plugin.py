from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from src.interns.step import Execution
from src.llmopenai import Argument, Function, Parameters, Tool


class Plugin(ABC):
    name: str
    description: str
    args_schema: Dict[str, Argument]
    required: List[str]
    categories: Optional[List[str]] = None

    @staticmethod
    @abstractmethod
    async def arun(*args, **kwargs) -> Execution:
        pass

    @classmethod
    def to_openai_tool(cls) -> Tool:
        return Tool(
            function=Function(
                name=cls.name,
                description=cls.description,
                parameters=Parameters(
                    properties=cls.args_schema,
                    required=cls.required
                )
            )
        )
    
    @classmethod
    def to_functions_list(cls) -> str:
        args = []
        for arg_name, arg in cls.args_schema.items():
            arg_type = arg.type
            # re-naming 
            if arg_type == "string":
                arg_type = "str"
            elif arg_type == "boolean":
                arg_type = "bool"
            elif arg_type == "integer":
                arg_type = "int"
            elif arg_type == "number":
                arg_type = "float"
            # checking if required
            if arg_name in cls.required:
                args.append(f"{arg_name}: {arg_type}")
            else:
                args.append(f"{arg_name}: {arg_type} = None")

        return f"{cls.name}({', '.join(args)})"