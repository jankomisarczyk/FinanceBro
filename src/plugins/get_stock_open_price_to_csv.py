from datetime import datetime

import yfinance

from src.interns.step import Execution
from src.llmopenai import Argument
from src.plugins.plugin import Plugin

PLUGIN_NAME = "get_stock_open_price_to_csv"
PLUGIN_DESCRIPTION = "Writes stock open price data for ticker symbol to a csv file. It gathers data for a provided time window."
ARGS_SCHEMA = {
    "ticker": Argument(type="string", description="Stock ticker symbol"),
    "filename": Argument(type="string", description="Name of csv file to which stock data will be written"),
    "date_from": Argument(type="string", description="Start date for data retrival in `YYYY-MM-DD` format"),
    "date_to": Argument(type="string", description="End date for data retrival in `YYYY-MM-DD` format"),
}
    

class GetStockOpenPriceToCsv(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["ticker", "filename"]
    categories = ["Financial analysis"]
    
    @staticmethod
    async def arun(ticker: str, filename: str = None, date_from: str = None, date_to: str = None) -> Execution:
        try:
            # if date_to or date_from not provided
            current_date = datetime.now()
            if not date_to:
                date_to = current_date.strftime("%Y-%m-%d")
            if not date_from:
                current_date = current_date.replace(year = current_date.year - 2)
                date_from = current_date.strftime("%Y-%m-%d")
            
            # just safety measure, if passed filename=None or not csv
            if not filename:
                filename = f"{ticker}_open_price.csv"
            else:
                if not filename[-4:] == ".csv":
                    filename += ".csv"
            
            stock =  yfinance.Ticker(ticker)
            dataframe = stock.history(period="1d", start=date_from, end=date_to)
            dataframe.index = dataframe.index.strftime("%Y-%m-%d")
            dataframe.to_csv(filename, encoding='utf-8', columns=["Open"])
            return Execution(
                observation=f"Stock Open data was successfully written to {filename}."
            )
        except Exception as e:
            return Execution(
                observation=f"Error on execution of {GetStockOpenPriceToCsv.name}: {e}"
            )
