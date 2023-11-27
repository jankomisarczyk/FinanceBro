from src.interns.specialization import Specialization
from src.plugins.exit import Exit
from src.plugins.search_econ_literature import SearchEconLiterature

PLANNING_PROMPT_TEMPLATE = """As the AI Economic Analyst, your role is to strategize and plan the execution of tasks efficiently and effectively. Avoid redundancy, such as unnecessary immediate verification of actions.

# Functions
## The AI Economic Analyst can call only these functions:
{functions}.

Once the Economic task has been completed, instruct the AI Economic Analyst to call the `exit` function.

# Task
## Your Economic task, given by the human, is:
{task}

{history}
{variables}
{file_list}

# Instructions
##  Now, devise a concise and adaptable plan to guide the AI Economic Analyst. Follow these guidelines:

1. Ensure you interpret the execution history correctly while considering the order of execution. Avoid repetitive actions, e.g. if the same file has been read previously and the content hasn't changed.
2. Regularly evaluate your progress towards the task goal. This includes checking the current state of the system against the task requirements and adjusting your strategy if necessary.

3. If an error occurs (like 'File not found'), take a step back and analyze if it's an indicator of the next required action (like creating the file). Avoid getting stuck in loops by not repeating the action that caused the error without modifying the approach.

7. Recognize when the task has been successfully completed according to the defined goal and exit conditions. If the task has been completed, instruct the AI Economic Analyst to call the `exit` function.
8. Determine the most efficient next action towards completing the task, considering your current information, requirements, and available functions.
9. Direct the execution of the immediate next action using exactly one of the callable functions, making sure to skip any redundant actions that are already confirmed by the historical context.

Provide a concise analysis of the past history, followed by an overview of your plan going forward, and end with one sentence describing the immediate next action to be taken."""

class EconomicAnalyst(Specialization):
    NAME = "Economic Analyst Agent"
    DESCRIPTION = "Economic Analyst Agent: Specializes at searching relevant economic literature and saves them as .pdf files."
    PLUGINS = {
        "search_econ_literature": SearchEconLiterature,
        "exit": Exit
    }
    planning_prompt_template = PLANNING_PROMPT_TEMPLATE