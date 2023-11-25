import csv

import xlwings as xw

from src.interns.step import Execution
from src.llmopenai import Argument
from src.plugins.plugin import Plugin

PLUGIN_NAME = "csv_to_excel"
PLUGIN_DESCRIPTION = "Inputs data from .csv file into active Excel Sheet. Optionally, you can specify where the data table should be inputed via range."
ARGS_SCHEMA = {
    "csv_filename": Argument(type="string", description="The name of the .csv file containing the data."),
    "range": Argument(type="string", description="The top-left cell of the Excel range where the data table should be inputted.")
}

class CsvToExcel(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["csv_filename"]
    categories = ["Excel"]
    
    @staticmethod
    async def arun(sheet_name: str, range: str = None) -> Execution:
        try:
            if not sheet_name[-4:] == ".csv":
                sheet_name += ".csv"
            if not range:
                range = "A1"
            data = []
            with open(sheet_name, 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    data.append(row)
            sheet = xw.sheets.active
            sheet[range].value = data
            sheet[range].expand().columns.autofit()
            return Execution(
                observation=f"Successfully inputed data table from .csv file. Currently, active Excel is {xw.books.active.name} and active Sheet is {xw.sheets.active.name}."
            )
        except Exception as e:
            if str(e) == "Couldn't find any active App!":
                return Execution(
                    observation="No Excel is opened and thus also active."
                )
            return Execution(
                observation=f"Error on execution of {CsvToExcel.name}: {e}"
            )
