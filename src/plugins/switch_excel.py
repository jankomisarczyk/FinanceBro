import xlwings as xw

from src.interns.step import Execution
from src.llmopenai import Argument
from src.plugins.plugin import Plugin

PLUGIN_NAME = "switch_excel"
PLUGIN_DESCRIPTION = "Switches active Excel"
ARGS_SCHEMA = {
    "excel_name": Argument(type="string", description="The name of the Excel to be activated.")
}

class SwitchExcel(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["excel_name"]
    categories = ["Excel"]
    
    @staticmethod
    async def arun(excel_name: str) -> Execution:
        try:
            all_books_names = [book.name for book in xw.books]
            if excel_name not in all_books_names:
                raise ValueError(f"{excel_name} is not opened. List of currently opened Excels is {all_books_names}")
            old_book_name = xw.books.active.name
            xw.books[excel_name].activate()
            return Execution(
                observation=f"Successfully switched between Excels from {old_book_name} to {excel_name}. Currently, active Excel is {xw.books.active.name} and active Sheet is {xw.sheets.active.name}."
            )
        except Exception as e:
            if str(e) == "Couldn't find any active App!":
                return Execution(
                    observation="No Excel is opened and thus also active."
                )
            return Execution(
                observation=f"Error on execution of {SwitchExcel.name}: {e}"
            )
