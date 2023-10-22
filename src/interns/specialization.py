import logging
import json
from src.llmopenai import call_llm, Message
from src.interns.prompt_templates import PLANNING_PROMPT_TEMPLATE, DECIDING_PROMPT_TEMPLATE
from src.interns.step import Decision

logger = logging.getLogger(__name__)

class Specialization:
    NAME = ""
    TOOLS = []
    DESCRIPTION = ""
    llm_planner: str
    planning_prompt_template: str = PLANNING_PROMPT_TEMPLATE
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

    async def decide(self, prompt_variables: dict[str, str]) -> Decision:
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
            functions=[Function()]
        )
        
        logger.info("\n=== Decision Created ===")
        logger.info(json.dumps(response.function_call , indent=4))

        return await interpret_llm_response(
            prompt_variables=prompt_variables, response=response
        )

    def execute():
        """Execute the decieded action"""
        pass