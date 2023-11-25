import xlwings as xw

from src.interns.step import Execution
from src.llmopenai import Argument
from src.plugins.plugin import Plugin

PLUGIN_NAME = "read_value"
PLUGIN_DESCRIPTION = "Reads value in specified range. This action is performed on currently active Excel Sheet."
ARGS_SCHEMA = {
    "range": Argument(type="string", description="The Excel range where the value should be set.")
}

class ReadValue(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["range"]
    categories = ["Excel"]
    
    @staticmethod
    async def arun(range: str) -> Execution:
        try:
            sheet = xw.sheets.active
            return Execution(
                observation=f"The value of {range} is equal to {sheet[range].value}. Currently, active Excel is {xw.books.active.name} and active Sheet is {xw.sheets.active.name}."
            )
        except Exception as e:
            if str(e) == "Couldn't find any active App!":
                return Execution(
                    observation="No Excel is opened and thus also active."
                )
            return Execution(
                observation=f"Error on execution of {ReadValue.name}: {e}"
            )
