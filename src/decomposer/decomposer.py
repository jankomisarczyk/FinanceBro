from __future__ import annotations

import json
import logging
import os
from json import JSONDecodeError
from typing import Any, TYPE_CHECKING
from src.llmopenai import call_llm
from src.llmopenai import Message

if TYPE_CHECKING:
    from src.interns.specialization import Specialization

logger = logging.getLogger(__name__)

class Decomposer:
    specialisation_registry: dict[str, Specialization]
    task: str
    model: str

    def __init__(self, task = None, specialisation_registry = None, model = None):
        self.task = task
        self.specialisation_registry = specialisation_registry
        self.model = model

    async def decompose(self) -> Any:
        agent_list = "- " + "\n- ".join([specialisation.DESCRIPTION for specialisation in self.specialisation_registry.values()])
        prompt = DECOMPOSER_TEMPLATE.format(
            agent_list=agent_list, task=self.task, files=self.starting_files()
        )

        logger.info("\n=== Task Decomposition given to LLM ===")
        logger.info(prompt)
        #CHECK if better is not use "user" as message to decompose?
        response = await call_llm(
            messages=[Message(role="system", content=prompt)],
            model=self.model
        )
        logger.info("\n=== Task Decomposition received from LLM ===")
        logger.info(response.content)

        try:
            parsed_response = json.loads(response.content)
        except JSONDecodeError as e:
            logger.error(f"Could not decode response {e}: {response}")
            # TODO: Handle error better
            raise e
        # TODO do validation of all agents if all params are here
        return parsed_response

    def starting_files(self) -> str:
        #TODO I need to re-factor this, so that each file already existing in workspace is in global files

        file_list = []
        for file in os.listdir():
            abs_path = os.path.abspath(os.path.join(file.replace("/", "_")))
            if not os.path.isdir(abs_path):
                file_list.append(f"- {file}")

        if not file_list:
            return ""

        file_list.sort()
        file_list_output = "\n".join(file_list)
        return (
            f"**Files**: Each subtask may have access to any of the following files if included in its inputs:\n"
            f"{file_list_output}"
        )
    

DECOMPOSER_TEMPLATE = """
**Role**: You are a subtask analyzer AI, and your goal is to analyze a human-provided task into one or more interns for specialized AI Agents. Your analysis must be exact and must only include the actions necessary to fulfill the specific requirements stated in the human task. Avoid over-complicating simple tasks.

**Note**: Follow the human task to the letter. Any deviation or addition outside the task will increase costs. The human task may vary in complexity, so tailor the number of subtask(s) accordingly.

**Human Task**: `{task}`

**Agents**:
Agents are Autonomous AI Entities. They will strictly follow your instructions, so be clear and avoid actions that aren't required by the human task.

The following agents are specialized AI entities, each excelling in a certain area. 
{agent_list}

In addition to these specialized agents, there is a Generalist Agent which can handle a wide variety of interns. If a subtask doesn't fit in any area of expertise of the specialized agents, assign it to the Generalist Agent.

{files}

**Guidelines**:
1. **Analyze the Task**: Carefully dissect the human task, identifying the exact requirements without adding or inferring extra actions.
2. **Develop Instructions**: Create detailed step-by-step instructions for each subtask. To ensure the AI Agent is able to correctly determine when the task is complete, clearly stipulate all required outcomes and establish concrete exit conditions. Each subtask is executed in isolation, without context. If data collected in one subtask must be used in a future subtask, include instructions to export that data as a global variable. Be sure to explicitly include instructions for input files, output files, and variable exports.
3. **Assign interns**: Detail each subtask and assign it to the most appropriate agent, specifying the input filenames, the instructions for the agent, and the expected output filenames. Do not include interns that simply mark task completion or have no specific actions associated with them.

**Response Format**:
Responses should be valid JSON and should not include any other explanatory text. Example:
[
    {{"agent": "Research Agent", "inputs": ["my_topics.txt"], "outputs": [], "instructions": "Read the file my_topics.txt. Analyze the topics and export your analysis to the `topic_analysis` global variable."}},
    {{"agent": "Generalist Agent", "inputs": [], "outputs": ["topic_summary.txt"], "instructions": "Write the contents of the global variable `topic_analysis` to the file topic_summary.txt"}}
]
"""