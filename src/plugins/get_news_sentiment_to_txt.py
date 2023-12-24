import os

import requests

from src.interns.step import Execution
from src.llmopenai import Argument
from src.plugins.plugin import Plugin
from typing import List, Tuple

PLUGIN_NAME = "get_news_sentiment_to_txt"
PLUGIN_DESCRIPTION = "Gets latest news about company and averages their sentiment scores. It saves average sentiment score and news summaries to txt file."
ARGS_SCHEMA = {
    "ticker": Argument(type="string", description="Stock ticker symbol"),
    "filename": Argument(type="string", description="Name of txt file to which average sentiment score and news summaries will be written")
}

CONTENT = """{first_line}
The list of summarized articles:
{combined_summaries}"""
    

class GetNewsSentimentToTxt(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["ticker", "filename"]
    categories = ["Financial analysis"]
    
    @staticmethod
    async def arun(ticker: str, filename: str = None) -> Execution:
        base_url = "https://www.alphavantage.co/query"
        function = "NEWS_SENTIMENT"
        params = {
        "function": function,
        "tickers": ticker,
        "apikey": os.getenv("ALPHAVANTAGE_API_KEY")
        }

        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            avg, summary_table = GetNewsSentimentToTxt.calculate(data, ticker)
            definition = GetNewsSentimentToTxt.avgDef(avg)
            first_line = f"The average sentiment score for {ticker} stock is {avg:.3f} - {definition}."
            combined_summaries = "\n".join(summary_table)
            # just safety measure, if passed filename=None or not txt
            if not filename:
                filename = f"{ticker}_news_sentiment.txt"
            else:
                if not filename[-4:] == ".txt":
                    filename += ".txt"
            # Writing to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(CONTENT.format(first_line=first_line, combined_summaries=combined_summaries))
            
            return Execution(
                observation=f"News Sentiment for {ticker} was successfully written to {filename}.",
                info=f"Saved {filename}"
            )
        except Exception as e:
            return Execution(
                observation=f"Error on execution of {GetNewsSentimentToTxt.name}: {e}"
            )
    
    @staticmethod
    def calculate(data, ticker: str) -> Tuple[str, List[str]]:
        if "feed" in data and len(data["feed"]) > 0:
            avg = 0
            count = 0
            summaries = []
            for news in data["feed"]:
                summaries.append(f"- {news['summary']}")
                found = GetNewsSentimentToTxt.getTickerSentiment(news["ticker_sentiment"], ticker)
                if found != 333.:
                    count += 1
                    avg += found
            return avg/count, summaries
        else:
            return 0, []
    
    @staticmethod
    def getTickerSentiment(data, ticker: str) -> float:
        for sent in data:
            if sent["ticker"] == ticker:
                return float(sent["ticker_sentiment_score"])
        return 333.
    
    @staticmethod
    def avgDef(avg: float) -> str:
        if avg <= -0.35:
            return "Bearish"
        elif avg <= -0.15:
            return "Somewhat Bearish"
        elif avg < 0.15:
            return "Neutral"
        elif avg < 0.35:
            return "Somewhat Bullish"
        else:
            return "Bullish"
