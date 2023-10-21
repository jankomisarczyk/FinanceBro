from dataclasses import dataclass

@dataclass
class Step:
    intern_name: str = None
    plan: str = None
    decision: str = None
    execution: str = None