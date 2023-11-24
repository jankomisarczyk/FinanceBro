import xlwings as xw

from src.interns.step import Execution
from src.llmopenai import Argument
from src.plugins.plugin import Plugin

PLUGIN_NAME = "switch_sheet"
PLUGIN_DESCRIPTION = "Switches active sheet."
ARGS_SCHEMA = {
    "sheet_name": Argument(type="string", description="The name of the sheet to be activated.")
}

class SwitchSheet(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["sheet_name"]
    categories = ["Excel"]
    
    @staticmethod
    async def arun(sheet_name: str) -> Execution:
        try:
            wb = xw.books.active
            all_sheet_names = [sheet.name for sheet in wb.sheets]
            if sheet_name not in all_sheet_names:
                raise ValueError(f"{sheet_name} doesn't exist in {wb.name}. List of Sheets that exist in {wb.name} is {all_sheet_names}")
            old_sheet_name = wb.sheets.active.name
            wb.sheets[sheet_name].activate()
            return Execution(
                observation=f"Successfully switched between sheets from {old_sheet_name} to {sheet_name}. Currently, active Excel is {xw.books.active.name} and active Sheet is {xw.sheets.active.name}."
            )
        except Exception as e:
            if str(e) == "Couldn't find any active App!":
                return Execution(
                    observation="No Excel is opened and thus also active."
                )
            return Execution(
                observation=f"Error on execution of {SwitchSheet.name}: {e}"
            )
