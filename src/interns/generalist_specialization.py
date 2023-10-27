from src.interns.specialization import Specialization
from src.plugins.exit import Exit
from src.plugins.export_variable import ExportVariable
from src.plugins.write_file import WriteFile


class Generalist(Specialization):
    NAME = "Generalist Agent"
    DESCRIPTION = "Generalist Agent: Excels at general tasks such as writing to a file"
    PLUGINS = {
        "write_file": WriteFile,
        "export_variable": ExportVariable,
        "exit": Exit
    }