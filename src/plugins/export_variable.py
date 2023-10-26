from src.plugins.plugin import Plugin
from src.llmopenai import Argument
from src.interns.step import Execution

PLUGIN_NAME = "export_variable"
PLUGIN_DESCRIPTION = "Set and export a variable to make it globally available to other subtasks."
ARGS_SCHEMA = {
    "name": Argument(type="string", description="Name of a variable"),
    "value": Argument(type="string", description="Value of a variable")
}

class ExportVariable(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    categories = []

    async def arun(name: str, value: str) -> Execution:
        return Execution(observation="Variable export was successful", set_variables={name: value})