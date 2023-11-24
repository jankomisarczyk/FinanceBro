from src.interns.specialization import Specialization
from src.plugins.exit import Exit
from src.plugins.open_excel import OpenExcel
from src.plugins.create_new_excel import CreateNewExcel
from src.plugins.get_active_excel_and_sheet import GetActiveExcelAndSheet
from src.plugins.switch_sheet import SwitchSheet
from src.plugins.switch_excel import SwitchExcel
from src.plugins.create_new_sheet import CreateNewSheet

PLANNING_PROMPT_TEMPLATE = """As the AI Excel Agent, your role is to strategize and plan the execution of tasks efficiently and effectively. Avoid redundancy, such as unnecessary immediate verification of actions.

# Functions
## The AI Excel Agent can call only these functions:
{functions}.

For dunction set value read and so one we get from active sheet and active excel..........

For the function `set_value`, please format `range` argument according to the rules:
- to edit a Single Cell use: `range="A1"`
- to edit Cells from A1 to B2 use: `range="A1:B2"`
- to edit Column A use: `range="A:A"`
- to edit Columns A to B use: `range="A:B"`
- to edit Row 1 use: `range="1:1"`
- to edit Rows 1 to 2 use: `range="1:2"`

Once the Excel task has been completed, instruct the AI Excel Agent to call the `exit` function.

# Task
## Your Excel task, given by the human, is:
{task}

{history}
{variables}
{file_list}

# Instructions
##  Now, devise a concise and adaptable plan to guide the AI Excel Analyst. Follow these guidelines:

1. Ensure you interpret the execution history correctly while considering the order of execution. Avoid repetitive actions, e.g. if the same !!!!!!!!!!! if excel is opend it is already active !!!!!  file has been read previously and the content hasn't changed.
2. Regularly evaluate your progress towards the task goal. This includes checking the current state of the system against the task requirements and adjusting your strategy if necessary.
3. 

if user doenst specif excel file, jsut assume that he meant currently active excel and sheet, thus you dont need to execute `get active excel and sheet` and just go ahead to perform actual task

7. Recognize when the task has been successfully completed according to the defined goal and exit conditions. If the task has been completed, instruct the AI Excel Agent to call the `exit` function.
8. Determine the most efficient next action towards completing the task, considering your current information, requirements, and available functions.
9. Direct the execution of the immediate next action using exactly one of the callable functions, making sure to skip any redundant actions that are already confirmed by the historical context.

Provide a concise analysis of the past history, followed by an overview of your plan going forward, and end with one sentence describing the immediate next action to be taken."""

class Excel(Specialization):
    NAME = "Excel Agent"
    DESCRIPTION = "Excel Agent: Specializes at opening and modifying .xlsx files. It allows to interact with Excel."
    PLUGINS = {
        "open_excel": OpenExcel, # here Execution obs should be "I have opened excel file .. and current active sheet is ...
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