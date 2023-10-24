import json
import logging
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
import openai

logger = logging.getLogger(__name__)

class Argument(BaseModel):
    type: str
    enum: Optional[List[Any]] = None
    description: str
#.model_dump(exclude_none=True)

class Parameters(BaseModel):
    type: str = "object"
    properties: Dict[str, Argument]
    required: List[str]

class Function(BaseModel):
    name: str
    description: str
    parameters: Parameters


@dataclass
class LLMResponse:
    content: str = None
    function_call: Dict[str, Any] = None
    role: str = None

@dataclass
class Message:
    role: str
    content: str


async def call_llm(
    messages: List[Message],
    model: str = "gpt-3.5-turbo-0613",
    function_call: str = "auto",
    functions: List[Function] = None
) -> LLMResponse:
    #TODO here I need to replace asdict with model_dump :D
    messages = [asdict(message) for message in messages]
    logger.debug(f"~~ LLM Request ~~\n{messages}")

    if functions:
        response = await openai.ChatCompletion.acreate(
            model=model,
            messages=messages,
            functions
            # functions=[asdict(function) for function in functions],
            top_p=0.1,
            function_call=function_call
        )
    else:
        response = await openai.ChatCompletion.acreate(
            model=model,
            messages=messages,
            top_p=0.1
        )

    response_message = response["choices"][0]["message"]

    logger.debug(f"~~ LLM Response ~~\n{response_message}")
    logger.debug(json.dumps(response_message))
    return LLMResponse(**response_message)