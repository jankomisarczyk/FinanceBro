from src.plugins.plugin import Plugin
from src.llmopenai import Argument
from src.interns.step import Execution
from src.llmopenai import call_llm, Message
from bs4 import BeautifulSoup
import requests


PLUGIN_NAME = "extract_information_from_webpage"
PLUGIN_DESCRIPTION = "Extracts specific information from a webpage's content."
ARGS_SCHEMA = {
    "url": Argument(type="string", description="The URL of the webpage to analyze."),
    "information": Argument(type="string", description="The type of information to extract.")
}


QUESTION_PROMPT_TEMPLATE = """You are a language model tasked with answering a specific question based on the given content from the website {url}. Please provide an answer to the following question:

Question: {question}

Content:
{content}

Answer:
"""

class ExtractInformationFromWebpage(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["url", "information"]
    categories = ["Web"]

    @staticmethod
    async def arun(url: str, information: str) -> Execution:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            body_element = soup.find("body")
            if body_element:
                text = body_element.get_text(separator="\n")[:8000]
            else:
                return Execution(
                    observation=f"Error on execution of {ExtractInformationFromWebpage.name}: Error: Could not extract information from URL."
                    )
            
            prompt = QUESTION_PROMPT_TEMPLATE.format(content=text, question=information, url=url)
            response = await call_llm(messages=[Message(role="user", content=prompt)])

            return Execution(observation=response.content)
        except Exception as e:
            return Execution(
                observation=f"Error on execution of {ExtractInformationFromWebpage.name}: {e}"
            )



        