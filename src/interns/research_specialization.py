from src.interns.specialization import Specialization
from src.plugins.exit import Exit
from src.plugins.export_variable import ExportVariable
from src.plugins.extract_information_from_webpage import ExtractInformationFromWebpage
from src.plugins.get_website_content import GetWebsiteContent
from src.plugins.google_search import GoogleSearch


PLANNING_PROMPT_TEMPLATE = """As the Research Strategist for an AI Assistant, your role is to strategize and plan research tasks efficiently and effectively. Avoid redundancy, such as unnecessary immediate verification of actions.

# Functions
## The AI Assistant have these functions at their disposal:
{functions}.

When calling functions provide sufficient detail in arguments to ensure the data returned is unambiguously related to your research task.

# Task
## The research task is:
{task}

Once the research task has been completed, instruct the AI Assistant to call the `exit` function with all arguments to indicate the completion of the research.

{history}
{variables}
{file_list}

# Instructions
Now, devise a concise and adaptable research plan to guide the AI Assistant. Follow these guidelines:

1. Ensure you interpret the execution history correctly while considering the order of execution. Avoid repetitive actions, especially when the outcomes are clear and confirmed by the previous functions. Trust the accuracy of past function executions, assuming the state of the system and your research workspace remain consistent with the historical outcomes.
2. Recognize when the research task has been successfully completed. If the task has been completed, instruct the AI Assistant to call the `exit` function.
3. Determine the next logical step in the research task, considering your current information, requirements, and available functions.
4. Direct the execution of the immediate next action using exactly one of the available functions, making sure to skip any redundant actions that are already confirmed by the historical context.

Provide a concise analysis of the past history, followed by a step-by-step summary of your plan going forward, and end with one sentence describing the immediate next action to be taken."""


class Research(Specialization):
    NAME = "Research Agent"
    DESCRIPTION = "Research Agent: Specializes at searching on the Internet for sources of information. Should be used only when research task can't be completed by any other agent. Is able to export a global variable."
    PLUGINS = {
        "extract_information_from_webpage": ExtractInformationFromWebpage,
        "get_website_content": GetWebsiteContent,
        "google_search": GoogleSearch,
        "export_variable": ExportVariable,
        "exit": Exit
    }
    planning_prompt_template = PLANNING_PROMPT_TEMPLATE

