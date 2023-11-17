import re
from src.plugins.plugin import Plugin
from src.llmopenai import Argument
import requests
import os
from bs4 import BeautifulSoup
from src.plugins.templates import SUMMARIZATION_PROMPT_TEMPLATE
from src.llmopenai import call_llm, Message
from src.interns.step import Execution

PLUGIN_NAME = "find_ticker"
PLUGIN_DESCRIPTION = (
    "Returns stock ticker symbol given company name."
)
ARGS_SCHEMA = {
    "company_name": Argument(type="string", description="Name of the company for which to find the ticker.")
}
    

class FindTicker(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["company_name"]
    categories = ["Financial analysis"]
    
    @staticmethod
    async def arun(company_name: str) -> Execution:
        base_url = "https://www.alphavantage.co/query"
        function = "SYMBOL_SEARCH"
        params = {
        "function": function,
        "keywords": company_name,
        "apikey": os.getenv("ALPHAVANTAGE_API_KEY")
        }

        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            observation = FindTicker.getUSticker(data, company_name)
            return Execution(
                observation=observation
            )
        except Exception as e:
            return Execution(
                observation=f"Error on execution of {FindTicker.name}: {e}"
            )
    
    @staticmethod
    def getUSticker(data, company_name: str) -> str:
        if "bestMatches" in data and len(data["bestMatches"]) > 0:
            for match in data["bestMatches"]:
                if match["4. region"] == "United States":
                    return match["1. symbol"]
                else:
                    return f"No US ticker found for {company_name}."
            return data["bestMatches"][0]["1. symbol"]
        else:
            return f"No ticker found for {company_name}."