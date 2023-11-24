import xlwings as xw

from src.interns.step import Execution
from src.llmopenai import Argument
from src.plugins.plugin import Plugin

PLUGIN_NAME = "get_active_excel_and_sheet"
PLUGIN_DESCRIPTION = "Gets information about currently active Excel and Sheet."
ARGS_SCHEMA = {}
    

class GetActiveExcelAndSheet(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = []
    categories = ["Excel"]
    
    @staticmethod
    async def arun() -> Execution:
        try:
            obs = f"Currently, active Excel is {xw.books.active.name} and active Sheet is {xw.sheets.active.name}."
            return Execution(
                observation=obs
            )
        except Exception as e:
            if str(e) == "Couldn't find any active App!":
                return Execution(
                    observation="No Excel is opened and thus also active."
                )
            return Execution(
                observation=f"Error on execution of {GetActiveExcelAndSheet.name}: {e}"
            )
