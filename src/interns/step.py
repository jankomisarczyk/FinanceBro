from dataclasses import dataclass
from typing import Dict

@dataclass
class Decision:
    tool_name: str = None
    tool_args: Dict[str, str] = None

@dataclass
class Step:
    intern_name: str = None
    plan: str = None
    decision: Decision = None
    execution: str = None

