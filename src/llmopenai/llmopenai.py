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

class Parameters(BaseModel):
    type: str = "object"
    properties: Dict[str, Argument]
    required: List[str]

class Function(BaseModel):
    name: str
    description: str
    parameters: Parameters

class FunctionCall(BaseModel):
    name: str
    arguments: Optional[Dict[str, str]] = None

class LLMResponse(BaseModel):
    content: Optional[str] = None
    function_call: Optional[FunctionCall] = None
    role: str

class Message(BaseModel):
    role: str
    content: str

async def call_llm(
    messages: List[Message],
    model: str = "gpt-3.5-turbo-0613",
    function_call: str = "auto",
    functions: List[Function] = None
) -> LLMResponse:
    #TODO here I need to replace asdict with model_dump :D
    messages_list = [mess.model_dump() for mess in messages]
    logger.debug(f"~~ LLM Request ~~\n{messages}")

    if functions:
        response = await openai.ChatCompletion.acreate(
            model=model,
            messages=messages_list,
            functions=[func.model_dump(exclude_none=True) for func in functions],
            top_p=0.1,
            function_call=function_call
        )
    else:
        response = await openai.ChatCompletion.acreate(
            model=model,
            messages=messages_list,
            top_p=0.1
        )

    response_message = response["choices"][0]["message"]

    logger.debug(f"~~ LLM Response ~~\n{response_message}")
    logger.debug(json.dumps(response_message))

    if "function_call" in response_message:
        args = response_message["function_call"]["arguments"]
        return LLMResponse(
            content=response_message["content"],
            role=response_message["role"],
            function_call=FunctionCall(
                name=response_message["function_call"]["name"],
                arguments=json.loads(args)
            )
        )
    else:
        return LLMResponse(**response_message)