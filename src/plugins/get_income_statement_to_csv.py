import yfinance

from src.interns.step import Execution
from src.llmopenai import Argument
from src.plugins.plugin import Plugin

PLUGIN_NAME = "get_income_statement_to_csv"
PLUGIN_DESCRIPTION = "Writes stock open price data for ticker symbol to a csv file. It gathers data for a provided time window."
ARGS_SCHEMA = {
    "ticker": Argument(type="string", description="Stock ticker symbol"),
    "filename": Argument(type="string", description="Name of csv file to which stock data will be written")
}
    

class GetIncomeStatementToCsv(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["ticker", "filename"]
    categories = ["Financial analysis"]
    
    @staticmethod
    async def arun(ticker: str, filename: str = None) -> Execution:
        try:
            # just safety measure, if passed filename=None or not csv
            if not filename:
                filename = f"{ticker}_income_statement.csv"
            else:
                if not filename[-4:] == ".csv":
                    filename += ".csv"
            
            stock =  yfinance.Ticker(ticker)
            dataframe = stock.income_stmt.transpose()
            dataframe.index.name = "Date"
            # TODO what columns do I really need for analysis columns=["EBITDA" ....]
            dataframe.to_csv(filename, encoding='utf-8')
            return Execution(
                observation=f"Income Statement was successfully written to {filename}."
            )
        except Exception as e:
            return Execution(
                observation=f"Error on execution of {GetIncomeStatementToCsv.name}: {e}"
            )
