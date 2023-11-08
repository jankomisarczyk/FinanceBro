import logging
import json
from typing import Dict
from src.llmopenai import call_llm, Message
from src.interns.prompt_templates import DECIDING_PROMPT_TEMPLATE
from src.interns.step import Decision, Execution
from src.plugins.plugin import Plugin

logger = logging.getLogger(__name__)

class Specialization:
    NAME: str
    DESCRIPTION: str
    PLUGINS: Dict[str, Plugin]
    llm_planner: str
    planning_prompt_template: str
    llm_decider: str
    deciding_prompt_template: str = DECIDING_PROMPT_TEMPLATE

    def __init__(self, llm_planner: str, llm_decider: str):
        #what I need to pass into specialization from INtern
        self.llm_planner = llm_planner
        self.llm_decider = llm_decider
    
    async def plan(self, prompt_variables: dict[str, str]) -> str:
        """Take the current task and history to develop a plan"""
        prompt = self.planning_prompt_template.format(**prompt_variables)

        logger.info("\n=== Plan Request ===")
        logger.info(prompt)
        
        response = await call_llm(
            messages=[Message(role="user", content=prompt)],
            model=self.llm_planner
        )

        logger.info("\n=== Plan Created ===")
        logger.info(response.content)
        return response.content

    async def decide(self, prompt_variables: Dict[str, str]) -> Decision:
        """Take the current plan to make a decision about next action"""
        prompt = self.deciding_prompt_template.format(**prompt_variables)

        logger.info("\n=== Decision Request ===")
        logger.info(prompt)

        #TODO how to implement functions in kwargs as descriptions and also in Function Calling of OPENAI
        #I should delete {functions} from prompt template??? or maybe I dont need to attach Functions_Calling_openai???
        #should I delete {history} from prompt if I do an array of Messages? i think No because GPT-4 is not capab
        # I need to CHECK if is able to call 2 functions in row before giving output to user ???
        # messages=[user, assistant, function1, assistant, function2] after function1 the gpt-4 should call function2

        # I need also answer if there is .content != None when function calling hmmm, when I only send call 
        # without attaching Functions_Calling_openai??? IMPORTANT !!!! this is original logic
        
        response = await call_llm(
            messages=[Message(role="user", content=prompt)],
            model=self.llm_decider,
            functions=[plugin.to_openai_function() for plugin in self.PLUGINS.values()]
        )
        
        logger.info("\n=== Decision Created ===")
        logger.info(response.function_call)

        #TODO logic to re-try Deciding if response is NOT valid function

        return Decision(
            tool_name=response.function_call.name,
            tool_args=response.function_call.arguments
        )

    async def execute(self, decision: Decision) -> Execution:
        """Execute the decieded action"""
        plugin = self.PLUGINS[decision.tool_name]
        if not plugin:
            return Execution(
                observation=f"Invalid tool name received: {decision.tool_name}."
                )
        
        execution = await plugin.arun(**decision.tool_args)
        logger.info("\n=== Execution observation ===")
        logger.info(execution.observation)

        return execution