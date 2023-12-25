import xlwings as xw

from src.interns.step import Execution
from src.llmopenai import Argument
from src.plugins.plugin import Plugin

PLUGIN_NAME = "create_new_excel"
PLUGIN_DESCRIPTION = "Creates new, empty .xlsx file."
ARGS_SCHEMA = {
    "excel_name": Argument(type="string", description="The name of the .xlsx file to be created.")
}
    

class CreateNewExcel(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["excel_name"]
    categories = ["Excel"]
    
    @staticmethod
    async def arun(excel_name: str) -> Execution:
        try:
            if not excel_name[-5:] == ".xlsx":
                excel_name += ".xlsx"
            wb = xw.Book()
            wb.save(rf"{excel_name}")
            return Execution(
                observation=f"Successfully created the Excel {excel_name}. Currently, active Excel is {excel_name} and active Sheet is {wb.sheets.active.name}.",
                set_files={excel_name: "Excel"},
                info=f"Created {excel_name}"
            )
        except Exception as e:
            return Execution(
                observation=f"Error on execution of {CreateNewExcel.name}: {e}"
            )
