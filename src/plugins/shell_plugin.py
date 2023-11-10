from src.plugins.plugin import Plugin
from src.llmopenai import Argument
from src.interns.step import Execution
from src.llmopenai import call_llm, Message
import json
import mistune
import subprocess

PLUGIN_NAME = "suggest_and_execute_shell_command"
PLUGIN_DESCRIPTION = "Suggests and then executes a shell command given user's goal."
ARGS_SCHEMA = {
    "goal": Argument(type="string", description="The goal to achieve.")
}

SYSTEM_MESSAGE = """You are an expert at using shell commands. I need you to provide a response in the format `{"command": "your_shell_command_here"}`. Only provide a single executable line of shell code as the value for the "command" key. Never output any text outside the JSON structure. The command will be directly executed in a shell. For example, if I ask to display the message 'Hello, World!', you should respond with ```json\n{"command": "echo 'Hello, World!'"}```"""
USER_MESSAGE = """Here's what I'm trying to do: {goal}"""

class PythonCodeBlockParser(mistune.HTMLRenderer):
    def __init__(self, *args, **kwargs):
        super(PythonCodeBlockParser, self).__init__(*args, **kwargs)
        self.code_blocks = []
        self.codespans = []

    def codespan(self, code):
        self.codespans.append(code)
        return super().codespan(code)

    def block_code(self, code, info=None):
        #lang = info.split(None, 1)[0] if info else None
        self.code_blocks.append(code)
        return super().block_code(code)

class SuggestAndExecuteShellCommand(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["goal"]
    categories = ["System"]

    @staticmethod
    async def arun(goal: str) -> Execution:
        # 1 calling LLM for shell command
        try:
            prompt = USER_MESSAGE.format(goal=goal)
            response = await call_llm(messages=[Message(role="system", content=SYSTEM_MESSAGE), Message(role="user", content=prompt)])
        except Exception:
            return Execution(
                observation=f"Error on execution of {SuggestAndExecuteShellCommand.name}: AI wasn't able to suggest a shell command for {goal}."
            )

        # 2 parsing the response
        try:
            json_content = SuggestAndExecuteShellCommand.code_parser(response.content)
            command_json = json.loads(json_content)
            command = command_json.get("command", "")
            if not command:  # Ensure the command is not empty
                return Execution(
                    observation=f"Error on execution of {SuggestAndExecuteShellCommand.name}: AI suggested an empty shell command."
                )
        except json.JSONDecodeError:
            # Fallback: treat the message as a command
            command = response.content

        # 2.5 intercepting ALL curl commands
        if ('curl' in command) and ('-L' not in command):
            #command = "curl -L" + command[command.find("curl") + 4:]
            command = "curl -L" + command[4:]

        # 3 executing
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            return Execution(
                observation=f"Error on execution of {SuggestAndExecuteShellCommand.name}: {e}"
            )

        return Execution(observation=f"Successfully suggested and executed shell command for the goal.")
    
    @staticmethod
    def code_parser(markdown):
        renderer = PythonCodeBlockParser()
        parser = mistune.create_markdown(renderer=renderer)
        parser(markdown)

        if renderer.code_blocks:
            return "".join(renderer.code_blocks)
        if renderer.codespans:
            return "\n".join(renderer.codespans)
        return markdown 
