import xlwings as xw

from src.interns.step import Execution
from src.llmopenai import Argument
from src.plugins.plugin import Plugin

PLUGIN_NAME = "set_color"
PLUGIN_DESCRIPTION = "Sets color of specified range. This action is performed on currently active Excel Sheet."
ARGS_SCHEMA = {
    "range": Argument(type="string", description="The Excel range where the color should be set."),
    "hex_color": Argument(type="string", description="The color represented as hex string like #FF0000 for red."),
}


class SetColor(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["range", "hex_color"]
    categories = ["Excel"]
    
    @staticmethod
    async def arun(range: str, hex_color: str) -> Execution:
        try:
            sheet = xw.sheets.active
            sheet[range].color = hex_color
            return Execution(
                observation=f"The color was successfully set. Currently, active Excel is {xw.books.active.name} and active Sheet is {xw.sheets.active.name}.",
                info="Color changed"
            )
        except Exception as e:
            if str(e) == "Couldn't find any active App!":
                return Execution(
                    observation="No Excel is opened and thus also active."
                )
            return Execution(
                observation=f"Error on execution of {SetColor.name}: {e}"
            )