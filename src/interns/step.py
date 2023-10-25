from pydantic import BaseModel
from typing import Dict

class Decision(BaseModel):
    tool_name: str = None
    tool_args: Dict[str, str] = None

class Step(BaseModel):
    intern_name: str = None
    plan: str = None
    decision: Decision = None
    execution: str = None

