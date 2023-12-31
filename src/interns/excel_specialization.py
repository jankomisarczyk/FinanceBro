from src.interns.specialization import Specialization
from src.plugins.create_new_excel import CreateNewExcel
from src.plugins.create_new_sheet import CreateNewSheet
from src.plugins.csv_to_excel import CsvToExcel
from src.plugins.exit import Exit
from src.plugins.get_active_excel_and_sheet import GetActiveExcelAndSheet
from src.plugins.open_excel import OpenExcel
from src.plugins.read_value import ReadValue
from src.plugins.set_color import SetColor
from src.plugins.set_value import SetValue
from src.plugins.switch_excel import SwitchExcel
from src.plugins.switch_sheet import SwitchSheet

PLANNING_PROMPT_TEMPLATE = """As the AI Excel Agent, your role is to strategize and plan the execution of tasks efficiently and effectively. Avoid redundancy, such as unnecessary immediate verification of actions.

# Functions
## The AI Excel Agent can call only these functions:
{functions}.

Functions `create_new_sheet`, `csv_to_excel`, `set_value`, `read_value`, `set_color` are executed on currently active Excel Sheet. To get information about currently active Excel Sheet, call `get_active_excel_and_sheet` function. In order to switch between Excels or Sheets use `switch_excel` and `switch_sheet` respectively.

If you want to use a function that requires `range` argument, please format `range` argument always for a single cell e.g. A1 use: range="A1".
This means if you want to use a function `set_value` or `set_color` for cells from A1 to B2 i.e. "A1:B2", you need to call the function for every single cell in the range that is "A1", "A2", "B1" and "B2".

Once the Excel task has been completed, instruct the AI Excel Agent to call the `exit` function.

# Task
## Your Excel task, given by the human, is:
{task}

{history}
{variables}
{file_list}

# Instructions
##  Now, devise a concise and adaptable plan to guide the AI Excel Analyst. Follow these guidelines:

1. Ensure you interpret the execution history correctly while considering the order of execution. Avoid repetitive actions, e.g. you don't need to call `get_active_excel_and_sheet`, if you know from the last executed function in history what currently active Excel Sheet is.
2. Regularly evaluate your progress towards the task goal. This includes checking the current state of the system against the task requirements and adjusting your strategy if necessary.
3. If the human hasn't specified Excel Sheet on which the task should be executed, perform all required steps of the task on currently active Excel Sheet.
4. Recognize when the task has been successfully completed according to the defined goal and exit conditions. If the task has been completed, instruct the AI Excel Agent to call the `exit` function.
5. Determine the most efficient next action towards completing the task, considering your current information, requirements, and available functions.
6. Direct the execution of the immediate next action using exactly one of the callable functions, making sure to skip any redundant actions that are already confirmed by the historical context.

Provide a concise analysis of the past history, followed by an overview of your plan going forward, and end with one sentence describing the immediate next action to be taken."""

class Excel(Specialization):
    NAME = "Excel Agent"
    DESCRIPTION = "Excel Agent: Specializes at opening, creating and modifying .xlsx files. It allows to interact with Excel. NOT able to export a global variable."
    PLUGINS = {
        "open_excel": OpenExcel,
        "create_new_excel": CreateNewExcel,
        "get_active_excel_and_sheet": GetActiveExcelAndSheet,
        "switch_excel": SwitchExcel,
        "create_new_sheet": CreateNewSheet,
        "switch_sheet": SwitchSheet,
        "csv_to_excel": CsvToExcel,
        "set_value": SetValue,
        "read_value": ReadValue,
        "set_color": SetColor,
        "exit": Exit
    }
    planning_prompt_template = PLANNING_PROMPT_TEMPLATE