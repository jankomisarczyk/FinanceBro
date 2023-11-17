from src.interns.specialization import Specialization
from src.plugins.exit import Exit
from src.plugins.find_ticker import FindTicker


PLANNING_PROMPT_TEMPLATE = """As the AI Financial Analyst, your role is to strategize and plan the execution of tasks efficiently and effectively. Avoid redundancy, such as unnecessary immediate verification of actions.

# Functions
## The AI Financial Analyst can call only these functions:
{functions}.

Date format for `date_from` and `date_to` arguments is `YYYY-MM-DD`. Once the financial task has been completed, instruct the AI Financial Analyst to call the `exit` function.

# Task
## Your financial task, given by the human, is:
{task}

{history}
{variables}
{file_list}

# Instructions
##  Now, devise a concise and adaptable plan to guide the AI Financial Analyst. Follow these guidelines:

1. Ensure you interpret the execution history correctly while considering the order of execution. Avoid repetitive actions, e.g. if the same file has been read previously and the content hasn't changed.
2. Regularly evaluate your progress towards the task goal. This includes checking the current state of the system against the task requirements and adjusting your strategy if necessary.
3. If not specified in Task what stock prices to take, use close price.
4. If not specified in Task what data period to take into account, call `get_*` functions with time window for the last 2 years. Current date is {current_date}.
5. If the task goal is to analyze a company and without specified data, instruct the AI Financial Analyst to call at least `get_stock_close_price_to_csv`, `get_balance_sheet_to_csv` and `get_financial_news_to_txt`.
6. If an error occurs (like 'Could not analyze company data'), take a step back and analyze if it's an indicator of the next required action (like getting financial data first). Avoid getting stuck in loops by not repeating the action that caused the error without modifying the approach.
7. Recognize when the task has been successfully completed according to the defined goal and exit conditions. If the task has been completed, instruct the AI Financial Analyst to call the `exit` function.
8. Determine the most efficient next action towards completing the task, considering your current information, requirements, and available functions.
9. Direct the execution of the immediate next action using exactly one of the callable functions, making sure to skip any redundant actions that are already confirmed by the historical context.

Provide a concise analysis of the past history, followed by an overview of your plan going forward, and end with one sentence describing the immediate next action to be taken."""

class FinancialAnalyst(Specialization):
    NAME = "Financial Analyst Agent"
    DESCRIPTION = "Financial Analyst Agent: Specializes at getting and analyzing stock data, financial news, income statements, balance sheets, valuation measures and cash flow statements of companies."
    PLUGINS = {
        "find_ticker": FindTicker,
        "get_stock_close_price_to_csv"
        "get_stock_open_price_to_csv"
        "get_income_statement_to_csv"
        "get_balance_sheet_to_csv"
        "get_cash_flow_statement_to_csv"
        "get_valuation measures_to_csv"
        "get_financial_news_to_txt"
        "get_reddit_news_to_txt"
        "analyze_company_data"
        "exit": Exit
    }
    planning_prompt_template = PLANNING_PROMPT_TEMPLATE