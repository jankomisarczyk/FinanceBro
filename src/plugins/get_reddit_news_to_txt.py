import os
import re

import praw
from selenium import webdriver
from selenium.webdriver.common.by import By

from src.interns.step import Execution
from src.llmopenai import Argument
from src.plugins.plugin import Plugin

PLUGIN_NAME = "get_reddit_news_to_txt"
PLUGIN_DESCRIPTION = "Checks if a company was mentioned in latest comments on the subreddit r/wallstreetbets. It saves the analysis to txt file."
ARGS_SCHEMA = {
    "company_name": Argument(type="string", description="Name of the company to be searched for in the comments on the subreddit r/wallstreetbets"),
    "ticker": Argument(type="string", description="Stock ticker symbol of the company"),
    "filename": Argument(type="string", description="Name of txt file to which the analysis will be written")
}

class GetRedditNewsToTxt(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["company_name", "ticker", "filename"]
    categories = ["Financial analysis"]
    
    @staticmethod
    async def arun(company_name:str, ticker: str, filename: str = None) -> Execution:
        try:
            url = 'https://www.reddit.com/r/wallstreetbets/search/?q=flair%3A%22Daily%20Discussion%22&restrict_sr=1&sort=new'
            driver = webdriver.Chrome()
            driver.get(url)
            link = driver.find_element(By.XPATH, '//*[@data-testid="post-title"]').get_attribute("href")
            driver.quit()
            reddit = praw.Reddit(
                client_id=os.getenv("REDDIT_CLIENT_ID"),
                client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                user_agent=os.getenv("REDDIT_USER_AGENT")
            )
            submission = reddit.submission(url=link)
            submission.comments.replace_more(limit=0)
            text_content = ""
            for comment in submission.comments.list():
                text_content += comment.body + "\n"
            text_content = GetRedditNewsToTxt.clean_content(text_content)
            # just safety measure, if passed filename=None or not txt
            if not filename:
                filename = f"{ticker}_reddit_news.txt"
            else:
                if not filename[-4:] == ".txt":
                    filename += ".txt"
            # Writing to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text_content)
            return Execution(
                observation=f"Reddit News Analysis for {company_name} was successfully written to {filename}."
            )
        except Exception as e:
            return Execution(
                observation=f"Error on execution of {GetRedditNewsToTxt.name}: {e}"
            )
    
    @staticmethod
    def clean_content(text: str) -> str:
        file_contents = text.replace('[deleted]', '')
        file_contents = file_contents.replace('[removed]', '')
        file_contents = re.sub(r'[^\x00-\x7F]+', '', file_contents)
        file_contents = re.sub(r'!\[img\]\([^)]+\)', '', file_contents)
        file_contents = re.sub(r'\[https?://[^\]]+\]\([^)]+\)', '', file_contents)
        file_contents = re.sub(r'https?://\S+', '', file_contents)

        return file_contents
