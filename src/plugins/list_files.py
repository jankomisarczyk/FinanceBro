from src.plugins.plugin import Plugin
from src.interns.step import Execution
import subprocess

PLUGIN_NAME = "list_files"
PLUGIN_DESCRIPTION = "Provides a list of all accessible files."
ARGS_SCHEMA = {}

class ListFiles(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = []
    categories = ["System"]

    @staticmethod
    async def arun() -> Execution:
        try:
            output = subprocess.check_output('ls', shell=True)
            list_of_files = output.decode("utf-8")
        except subprocess.CalledProcessError as e:
            return Execution(
                observation=f"Error on execution of {ListFiles.name}: {e}"
            )

        return Execution(observation=list_of_files)
