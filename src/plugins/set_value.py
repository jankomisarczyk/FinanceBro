import xlwings as xw

from src.interns.step import Execution
from src.llmopenai import Argument
from src.plugins.plugin import Plugin

PLUGIN_NAME = "set_value"
PLUGIN_DESCRIPTION = "Sets value in specified range. This action is performed on currently active Excel Sheet."
ARGS_SCHEMA = {
    "range": Argument(type="string", description="The Excel range where the value should be set."),
    "value": Argument(type="string", description="The value.")
}

class SetValue(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["range", "value"]
    categories = ["Excel"]
    
    @staticmethod
    async def arun(range: str, value: str) -> Execution:
        try:
            sheet = xw.sheets.active
            sheet[range].value = value
            return Execution(
                observation=f"The value was successfully set. Currently, active Excel is {xw.books.active.name} and active Sheet is {xw.sheets.active.name}."
            )
        except Exception as e:
            if str(e) == "Couldn't find any active App!":
                return Execution(
                    observation="No Excel is opened and thus also active."
                )
            return Execution(
                observation=f"Error on execution of {SetValue.name}: {e}"
            )
