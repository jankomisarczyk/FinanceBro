import xlwings as xw

from src.interns.step import Execution
from src.llmopenai import Argument
from src.plugins.plugin import Plugin

PLUGIN_NAME = "create_new_sheet"
PLUGIN_DESCRIPTION = "Creates new, empty Sheet in active Excel."
ARGS_SCHEMA = {
    "sheet_name": Argument(type="string", description="The name of Sheet to be created.")
}
    

class CreateNewSheet(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["sheet_name"]
    categories = ["Excel"]
    
    @staticmethod
    async def arun(sheet_name: str) -> Execution:
        try:
            xw.sheets.add(name=sheet_name)
            return Execution(
                observation=f"Successfully created new Sheet {sheet_name}. Currently, active Excel is {xw.books.active.name} and active Sheet is {xw.sheets.active.name}."
            )
        except Exception as e:
            if str(e) == "Couldn't find any active App!":
                return Execution(
                    observation="No Excel is opened and thus also active."
                )
            return Execution(
                observation=f"Error on execution of {CreateNewSheet.name}: {e}"
            )
