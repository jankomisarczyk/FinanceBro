from src.plugins.plugin import Plugin
from src.interns.step import Execution
from src.llmopenai import Argument
import subprocess

PLUGIN_NAME = "open_file"
PLUGIN_DESCRIPTION = "Opens specified file."
ARGS_SCHEMA = {
    "filename": Argument(type="string", description="The name of the file to be opened.")
}

class OpenFile(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["filename"]
    categories = ["System"]

    @staticmethod
    async def arun(filename: str) -> Execution:
        try:
            command = 'start ' + filename
            subprocess.run(command, shell=True, check=True)
            return Execution(observation=f"Successfully opened the file {filename}.")
        except subprocess.CalledProcessError as e:
            return Execution(
                observation=f"Error on execution of {OpenFile.name}: {e}"
            )
