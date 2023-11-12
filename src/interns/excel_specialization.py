from src.interns.specialization import Specialization
from src.plugins.exit import Exit





class Excel(Specialization):
    NAME = "Excel Agent"
    DESCRIPTION = "Excel Agent: Specializes at creating excel files from csv, reading, modifying excel files and creating beautiful charts."
    PLUGINS = {
        
        "change_title"
        "change_title_color"
        "switch_columns"
        "read_excel"
        "csv_to_excel"
        "exit": Exit
    }
    planning_prompt_template = PLANNING_PROMPT_TEMPLATE