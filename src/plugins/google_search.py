import os

from langchain.utilities.google_serper import GoogleSerperAPIWrapper
from src.plugins.plugin import Plugin
from src.llmopenai import Argument
from src.interns.step import Execution

PLUGIN_NAME = "google_search"
PLUGIN_DESCRIPTION = (
    "Search Google for websites matching a given query. Useful for when you need to answer questions "
    "about current events."
)
ARGS_SCHEMA = {
    "query": Argument(type="string", description="The query string")
}


class GoogleSearch(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["query"]
    categories = ["Web"]

    @staticmethod
    async def arun(query: str) -> Execution:
        if not os.environ.get("SERPER_API_KEY"):
            return f"Google Search is not supported as the SERPER_API_KEY environment variable is not set"
        
        try:
            query_results = await GoogleSerperAPIWrapper().aresults(query)
            formatted_results = GoogleSearch.format_results(query_results.get("organic", []))
            return Execution(
                observation=formatted_results
            )
        except Exception as e:
            return Execution(
                observation=f"Error on execution of {GoogleSearch.name}: {e}"
            )

    @staticmethod
    def format_results(results: list[dict[str, str]]) -> str:
        formatted_results = []
        for result in results:
            formatted_results.append(f"{result.get('link')}: {result.get('snippet')}")

        return f"Your search results are: {' | '.join(formatted_results)}"