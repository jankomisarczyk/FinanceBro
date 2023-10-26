import re
from src.plugins.plugin import Plugin
from src.llmopenai import Argument
import requests
from bs4 import BeautifulSoup
from src.plugins.templates import SUMMARIZATION_PROMPT_TEMPLATE
from src.llmopenai import call_llm, Message
from src.interns.step import Execution

PLUGIN_NAME = "get_website_content"
PLUGIN_DESCRIPTION = (
    "Extracts the text content from the HTML of a specified webpage. It is useful when you want to obtain the textual"
    "information from a webpage without the need for in-depth analysis."
)
ARGS_SCHEMA = {
    "url": Argument(type="string", description="The URL of the webpage from which to retrieve the text content.")
}
    

class GetWebsiteText(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["url"]
    categories = ["Web"]
    
    async def arun(url: str) -> Execution:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            stripped_text = re.sub(r"\s+", " ", soup.get_text().strip())
            document = await GetWebsiteText.filter_long_documents(stripped_text)
            return Execution(
                observation=document
            )
        except Exception as e:
            return Execution(
                observation=f"Error on execution of {GetWebsiteText.name}: {e}"
            )
    
    @staticmethod
    async def filter_long_documents(document: str) -> str:
        if len(document) > 1000:
            summary_prompt = SUMMARIZATION_PROMPT_TEMPLATE.format(long_text=document[:8000])
            summarization = await call_llm(messages=[Message(role="user", content=summary_prompt)])
            return f"The response was summarized as: {summarization.content}"

        return document
