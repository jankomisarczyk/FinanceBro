from src.interns.specialization import Specialization
from src.plugins.exit import Exit
from src.plugins.shell_plugin import SuggestAndExecuteShellCommand
from src.plugins.export_variable import ExportVariable
from src.plugins.write_file import WriteFile
from src.plugins.read_file import ReadFile
from src.plugins.list_files import ListFiles


PLANNING_PROMPT_TEMPLATE = """As the AI File Manager, your role is to strategize and plan the execution of tasks efficiently and effectively. Avoid redundancy, such as unnecessary immediate verification of actions.

# Functions
## The AI File Manager can call only these functions:
{functions}.
Function `suggest_and_execute_shell_command(goal: str)` should only be called, when a subtask can't be achieved by other functions.

Once the filesystem task has been completed, instruct the AI File Manager to call the `exit` function with all arguments to indicate the completion of the task.

# Task
## Your filesystem task, given by the human, is:
{task}

{history}
{variables}
{file_list}

# Instructions
##  Now, devise a concise and adaptable plan to guide the AI File Manager. Follow these guidelines:

1. Ensure you interpret the execution history correctly while considering the order of execution. Avoid repetitive actions, e.g. if the same file has been read previously and the content hasn't changed.
2. Regularly evaluate your progress towards the task goal. This includes checking the current state of the system against the task requirements and adjusting your strategy if necessary.
3. If an error occurs (like 'File not found'), take a step back and analyze if it's an indicator of the next required action (like creating the file). Avoid getting stuck in loops by not repeating the action that caused the error without modifying the approach.
4. Recognize when the task has been successfully completed according to the defined goal and exit conditions. If the task has been completed, instruct the AI File Manager to call the `exit` function.
5. Determine the most efficient next action towards completing the task, considering your current information, requirements, and available functions.
6. Direct the execution of the immediate next action using exactly one of the callable functions, making sure to skip any redundant actions that are already confirmed by the historical context.

Provide a concise analysis of the past history, followed by an overview of your plan going forward, and end with one sentence describing the immediate next action to be taken."""

class FileManager(Specialization):
    NAME = "File Manager Agent"
    DESCRIPTION = "File Manager Agent: Excels at managing files and folders. It can perform wide verity of operations on files, including opening (viewing or printing), writing to a file, renaming, copying, moving, deleting and searching for files."
    PLUGINS = {
        "read_file": ReadFile,
        "open_file": TODO,
        "list_files": ListFiles,
        "write_file": WriteFile,
        "export_variable": ExportVariable,
        "suggest_and_execute_shell_command": SuggestAndExecuteShellCommand,
        "exit": Exit
    }
    planning_prompt_template = PLANNING_PROMPT_TEMPLATE