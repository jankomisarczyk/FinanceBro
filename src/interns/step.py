from pydantic import BaseModel
from typing import Dict, Optional, Any

class Decision(BaseModel):
    tool_name: str = None
    tool_args: Dict[str, Any] = None

class Execution(BaseModel):
    info: Optional[str] = None
    observation: str
    complete: bool = False
    set_variables: Optional[Dict[str, str]] = None
    set_files: Optional[Dict[str, str]] = None

class Step(BaseModel):
    intern_name: str = None
    plan: str = None
    decision: Decision = None
    execution: Execution = None

