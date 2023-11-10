from src.plugins.plugin import Plugin
from src.llmopenai import Argument
from src.interns.step import Execution
from src.plugins.templates import SUMMARIZATION_PROMPT_TEMPLATE
from src.llmopenai import call_llm, Message

PLUGIN_NAME = "read_file"
PLUGIN_DESCRIPTION = (
    "Reads and returns the content of a specified file."
)
ARGS_SCHEMA = {
    "filename": Argument(type="string", description="The name of the file to be read.")
}

class ReadFile(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["filename"]
    categories = ["Files"]

    @staticmethod
    async def arun(filename: str) -> Execution:
        try:
            with open(filename, 'r') as file:
                content = file.read()
            document = await ReadFile.filter_long_files(content)
            return Execution(
                observation=document
            )
        except Exception as e:
            return Execution(
                observation=f"Error on execution of {ReadFile.name}: {e}"
            )
    
    @staticmethod
    async def filter_long_files(document: str) -> str:
        if len(document) > 1000:
            summary_prompt = SUMMARIZATION_PROMPT_TEMPLATE.format(long_text=document[:8000])
            summarization = await call_llm(messages=[Message(role="user", content=summary_prompt)])
            return f"The file's content was summarized as: {summarization.content}"

        return document
    
