import logging

from src.plugins.plugin import Plugin
from src.llmopenai import Argument
from src.interns.step import Execution
from src.plugins.templates import DESCRIPTION_PROMPT_TEMPLATE
from src.llmopenai import call_llm, Message

PLUGIN_NAME = "write_file"
PLUGIN_DESCRIPTION = (
    "Allows you to write specified text content to a file, creating a new file or overwriting an existing one as "
    "necessary."
)
ARGS_SCHEMA = {
    "filename": Argument(type="string", description="Specifies the name of the file to which the content will be written."),
    "text_content": Argument(type="string", description="The content that will be written to the specified file.")
}

logger = logging.getLogger(__name__)

class WriteFile(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["filename", "text_content"]
    categories = ["Files"]

    @staticmethod
    async def arun(filename: str, text_content: str) -> Execution:
        # Writing to file
        with open(f'{filename}.txt', 'w') as f:
            f.write(text_content)
        
        description = await WriteFile.summarize_content(text_content)
        return Execution(
            observation="Write file was successful.",
            set_files={filename: description}
            )
    
    @staticmethod
    async def summarize_content(document: str) -> str:
        description_prompt = DESCRIPTION_PROMPT_TEMPLATE.format(file_text=document)
        description = await call_llm(messages=[Message(role="user", content=description_prompt)])
        return description
    
