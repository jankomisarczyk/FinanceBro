import os
from datetime import date

import numpy_financial as npf
import pandas as pd
import xlwings as xw
import yahoo_fin.stock_info as si
import yfinance

from src.interns.step import Execution
from src.llmopenai import Argument
from src.plugins.plugin import Plugin

PLUGIN_NAME = "analyze_company"
PLUGIN_DESCRIPTION = "Analyzes the company given diffrent financial sources and formulate an investment thesis for it. Additionaly, it creates an Excel file with DCF, if `` and `` arguments are not None."
ARGS_SCHEMA = {
    "ticker": Argument(type="string", description="Stock ticker symbol"),
    "cash_flow_filename": Argument(type="string", description="Name of .csv file with cash flow statement"),
    "balance_sheet_filename": Argument(type="string", description="Name of .csv file with balance sheet"),
    "income_statement_filename": Argument(type="string", description="Name of .csv file with income statement"),
    "news_sentiment_filename": Argument(type="string", description="Name of .txt file with news sentiment"),
    "reddit_news_filename": Argument(type="string", description="Name of .txt file with reddit news")
}

DCF_CHUNK = """

#DCF
## We have calculated the intrinsic value of the {ticker} stock using DCF model and here are the insights:
The intrinsic value is {intrinsic_value} and current value is {current_value}, which suggests that we should {recommendation} the stock.
For more information, please see {file}"""

REDDIT_CHUNK = """

#REDDIT COMMENTS
## We have analyzed the latest comments of Daily Discussion on reddit and here are the insights:
{chunk}"""

NEWS_CHUNK = """

#LATEST ARTICLES
## We have analyzed 50 latest articles for their sentiment and here are the insights:
{chunk}"""


class AnalyzeCompany(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    required = ["ticker"]
    categories = ["Financial analysis"]
    
    @staticmethod
    async def arun(ticker: str,
                   cash_flow_filename: str = None,
                   balance_sheet_filename: str = None,
                   income_statement_filename: str = None,
                   news_sentiment_filename: str = None,
                   reddit_news_filename: str = None) -> Execution:
        all_insights = f"We have analyzed various sources to get deeper understanding about the stock {ticker}."
        #1 DCF excel
        try:
            if cash_flow_filename and balance_sheet_filename and income_statement_filename:
                # data
                MKT_RETURN = float(os.getenv("MKT_RETURN"))
                PERP_GROWTH_RATE = float(os.getenv("PERP_GROWTH_RATE"))
                stock =  yfinance.Ticker(ticker)
                stock_info = stock.info
                tnx = yfinance.Ticker(os.getenv("BOND_TICKER"))
                cash_flow_df = pd.read_csv(cash_flow_filename, encoding='utf-8', header=0, index_col = 0)
                balance_sheet_df = pd.read_csv(balance_sheet_filename, encoding='utf-8', header=0, index_col = 0)
                income_stmt_df = pd.read_csv(income_statement_filename, encoding='utf-8', header=0, index_col = 0)
                # calculation
                interest_expense = AnalyzeCompany.get_val(income_stmt_df.loc['Interest Expense'])
                income_tax = AnalyzeCompany.get_val(income_stmt_df.loc['Tax Provision'])
                income_before_tax = AnalyzeCompany.get_val(income_stmt_df.loc['Pretax Income'])
                current_debt = AnalyzeCompany.get_val(balance_sheet_df.loc['Current Debt'])
                long_term_debt = AnalyzeCompany.get_val(balance_sheet_df.loc['Long Term Debt'])
                total_debt = current_debt + long_term_debt
                cost_of_debt = interest_expense / total_debt
                effective_tax_rate = income_tax / income_before_tax
                risk_free_rate = tnx.info['regularMarketDayHigh']/100
                beta = stock_info['beta']
                market_cap = stock_info['marketCap']
                total = total_debt + market_cap
                weight_of_debt = total_debt / total
                weight_of_equity = market_cap / total
                # template
                template = xw.Book(r'../excel/WACC_DCF_template.xlsx')
                wacc = template.sheets["WACC"]
                wacc["D6"].value = weight_of_debt
                wacc["D7"].value = weight_of_equity
                wacc["D11"].value = risk_free_rate
                wacc["D12"].value = MKT_RETURN
                wacc["D13"].value = beta
                wacc["D17"].value = cost_of_debt
                wacc["D18"].value = effective_tax_rate
                wacc["D22"].value = date.today()
                wacc["F6"].value = stock_info['shortName']
                wacc["G6"].value = interest_expense
                wacc["H6"].value = income_tax
                wacc["I6"].value = income_before_tax
                wacc["J6"].value = current_debt
                wacc["K6"].value = long_term_debt
                wacc["L6"].value = total_debt
                wacc["M6"].value = market_cap
                wacc["N6"].value = total
                wacc["D:D"].columns.autofit()

                WACC_RATE = wacc["D21"].value
                growth_est_df = si.get_analysts_info(ticker)['Growth Estimates']
                growth_str = growth_est_df[growth_est_df['Growth Estimates'] == 'Next 5 Years (per annum)'][ticker].iloc[0]
                growth_rate = round(float(growth_str.rstrip('%')) / 100.0, 4)

                free_cash_flow = cash_flow_df.loc['Free Cash Flow'][0]
                ffcf = []
                ffcf.append(free_cash_flow * (1 + growth_rate))
                for i in range(1, 5):
                    ffcf.append(ffcf[i-1] * (1 + growth_rate))
                terminal_value = ffcf[-1] * (1 + PERP_GROWTH_RATE)/(WACC_RATE - PERP_GROWTH_RATE)

                dcf = template.sheets["DCF"]
                dcf["D4"].value = WACC_RATE
                dcf["D5"].value = growth_rate
                dcf["H8"].value = date.today().year
                dcf["H9"].value = free_cash_flow
                dcf["I9"].value = ffcf
                dcf["M10"].value = terminal_value

                ffcf[-1] = ffcf[-1] + terminal_value
                enterprise_value = npf.npv(WACC_RATE, [0] + ffcf)
                dcf["M11"].value = enterprise_value

                cash_and_equivalents = AnalyzeCompany.get_val(balance_sheet_df.loc['Cash And Cash Equivalents'])
                equity_value = enterprise_value + cash_and_equivalents - total_debt

                dcf["D8"].value = cash_and_equivalents
                dcf["D9"].value = current_debt
                dcf["D10"].value = long_term_debt
                dcf["D11"].value = equity_value
                shares_outstanding = stock_info['sharesOutstanding']
                current_value = stock_info['currentPrice']
                intrinsic_value = equity_value / shares_outstanding

                dcf["D14"].value = shares_outstanding
                dcf["D16"].value = intrinsic_value
                dcf["D17"].value = current_value
                recommendation = "BUY" if intrinsic_value > current_value else "SELL"
                dcf["D18"].value = recommendation
                dcf["D19"].value = date.today()
                dcf["D:D"].columns.autofit()
                dcf["H:M"].columns.autofit()
                file_excel = f"{ticker}_WACC_DCF.xlsx"
                template.save(file_excel)
                # I don't want to close it - because I want to leave it to the user
                all_insights += DCF_CHUNK.format(ticker=ticker, 
                                                 intrinsic_value=intrinsic_value, 
                                                 current_value=current_value, 
                                                 recommendation=recommendation,
                                                 file=file_excel)

            if reddit_news_filename:
                with open(reddit_news_filename, 'r') as f:
                    all_insights += REDDIT_CHUNK.format(chunk=f.read())

            if news_sentiment_filename:
                with open(news_sentiment_filename, 'r') as f:
                    all_insights += NEWS_CHUNK.format(chunk=f.read())
            
            filename = f"{ticker}_analyze_company.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(all_insights)
            return Execution(
                observation=f"Successfully analyzed the company. The insights were written to {filename} and the DCF model was saved to {file_excel}",
                info=f"All insights saved in {filename}<br>DCF saved in {file_excel}"
            )
        except Exception as e:
            return Execution(
                observation=f"Could not analyze company data. Error on execution of {AnalyzeCompany.name}: {e}"
            )
    
    @staticmethod
    def get_val(series: pd.Series):
        return series[series.first_valid_index()]