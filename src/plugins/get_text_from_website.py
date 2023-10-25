import re
from src.plugins.plugin import Plugin
from src.llmopenai import Argument
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from src.plugins.templates import SUMMARIZATION_PROMPT_TEMPLATE
from src.llmopenai import call_llm, Message

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
    
    async def arun(self, url: str) -> str:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        stripped_text = re.sub(r"\s+", " ", soup.get_text().strip())
        return await self.filter_long_documents(stripped_text)
    
    async def filter_long_documents(document: str) -> str:
        if len(document) > 1000:
            summary_prompt = SUMMARIZATION_PROMPT_TEMPLATE.format(long_text=document[:8000]).content
            summarization = await call_llm(messages=[Message(role="user", content=summary_prompt)])
            return f"The response was summarized as: {summarization.text}"

        return document