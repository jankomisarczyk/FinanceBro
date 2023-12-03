import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

from src.interns.step import Execution
from src.llmopenai import Argument
from src.plugins.plugin import Plugin

PLUGIN_NAME = "search_econ_literature"
PLUGIN_DESCRIPTION = (
    "Search the largest bibliographic database dedicated to Economics matching a given query and save documents as .pdf files."
)
ARGS_SCHEMA = {
    "query": Argument(type="string", description="The query string")
}


class SearchEconLiterature(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["query"]
    categories = ["Economics"]

    @staticmethod
    async def arun(query: str) -> Execution:
        try:
            query_param = query.replace(" ", "+")
            url = f"https://ideas.repec.org/cgi-bin/htsearch?q={query_param}"
            driver = webdriver.Chrome()
            driver.get(url)
            link = driver.find_element(By.XPATH, '//*[@class="list-group-item downfree"]')
            href = link.find_element(By.TAG_NAME, 'a').get_attribute("href")
            driver.get(href + "#download")
            value = driver.find_element(By.XPATH, '//input[@type="radio" and @name="url"]').get_attribute("value")
            driver.quit()
            response = requests.get(value)
            pdf_name = query.replace(" ", "_") + "_1.pdf"
            with open(pdf_name, 'wb') as pdf_file:
                pdf_file.write(response.content)
            
            return Execution(
                observation=f"Successfully found a relevant document and saved it under name: {pdf_name}.",
                set_files={pdf_name: f"Economic document about {query}. Saved by the Economic Analyst Agent"}
            )
        except Exception as e:
            return Execution(
                observation=f"Error on execution of {SearchEconLiterature.name}: Please try diffrent query string."
            )

    # @staticmethod
    # def extended_search(results: list[dict[str, str]]) -> str:
    #     if extended:
    #         results = []
    #    "extended": Argument(type="boolean", description="Whether to extend the search to other items")
    #     else:
    #     query = "economic growth".replace(" ", "+")
    #     url = f"https://ideas.repec.org/cgi-bin/htsearch?q={query}"
    #     driver = webdriver.Chrome()
    #     driver2 = webdriver.Chrome()
    #     driver.get(url)
    #     links = driver.find_elements(By.XPATH, '//*[@class="list-group-item downfree"]')
    #     for i in links:
    #         href = i.find_element(By.TAG_NAME, 'a').get_attribute("href")
    #         print(href)
    #         driver2.get(href + "#download")
    #         print(driver2.find_element(By.XPATH, '//input[@type="radio" and @name="url"]').get_attribute("value"))
    #     driver.quit()
    #     driver2.quit()

    #     return f"Your search results are: {' | '.join(formatted_results)}"