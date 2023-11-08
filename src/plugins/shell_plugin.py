from src.plugins.plugin import Plugin
from src.llmopenai import Argument
from src.interns.step import Execution
from src.llmopenai import call_llm, Message


PLUGIN_NAME = "suggest_and_execute_shell_command"
PLUGIN_DESCRIPTION = "Suggests and then executes a shell command given user's goal."
ARGS_SCHEMA = {
    "goal": Argument(type="string", description="The goal to achieve.")
}


SYSTEM_MESSAGE = """You are an expert at using shell commands. I need you to provide a response in the format `{"command": "your_shell_command_here"}`. Only provide a single executable line of shell code as the value for the "command" key. Never output any text outside the JSON structure. The command will be directly executed in a shell. For example, if I ask to display the message 'Hello, World!', you should respond with ```json\n{"command": "echo 'Hello, World!'"}```"""
USER_MESSAGE = """Here's what I'm trying to do: {goal}"""

class SuggestAndExecuteShellCommand(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["goal"]
    categories = ["System"]

    @staticmethod
    async def arun(goal: str) -> Execution:
        try:
            prompt = USER_MESSAGE.format(goal=goal)
            response = await call_llm(messages=[Message(role="system", content=SYSTEM_MESSAGE), Message(role="user", content=prompt)])
        except Exception as e:
            return Execution(
                observation=f"Suggestede {SuggestAndExecuteShellCommand.name}: {e}"
            )
                #TODO
        #tun soubprocoess
        return Execution(observation=response.content)
