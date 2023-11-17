import json
import logging
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Literal
from pydantic import BaseModel
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

class Argument(BaseModel):
    type: str
    enum: Optional[List[Any]] = None
    description: Optional[str] = None

class Parameters(BaseModel):
    type: Literal["object"]
    properties: Dict[str, Argument]
    required: List[str]

class Function(BaseModel):
    name: str
    description: str
    parameters: Parameters

class Tool(BaseModel):
    type: Literal["function"]
    function: Function

class FunctionCall(BaseModel):
    name: str
    arguments: Optional[Dict[str, Any]] = None

class ToolCall(BaseModel):
    id: str
    type: Literal["function"]
    function: FunctionCall

class LLMResponse(BaseModel):
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    role: Literal["assistant"]

class Message(BaseModel):
    role: str
    content: str

async def call_llm(
    messages: List[Message],
    model: str = "gpt-3.5-turbo-0613",
    tool_choice: str = "auto",
    tools: List[Tool] = None
) -> LLMResponse:
    #TODO here I need to replace asdict with model_dump :D
    client = AsyncOpenAI()
    messages_list = [mess.model_dump() for mess in messages]
    logger.debug(f"~~ LLM Request ~~\n{messages}")

    if tools:
        response = await client.chat.completions.create(
            model=model,
            messages=messages_list,
            tools=[tool.model_dump(exclude_none=True) for tool in tools],
            tool_choice=tool_choice,
            top_p=0.1
        )
    else:
        response = await client.chat.completions.create(
            model=model,
            messages=messages_list,
            top_p=0.1
        )

    response_message = response.choices[0].message

    logger.debug(f"~~ LLM Response ~~\n{response_message}")
    logger.debug(response_message.model_dump())

    if response_message.tool_calls:
        return LLMResponse(
            content=response_message.content,
            role=response_message.role,
            tool_calls=[ToolCall(
                id=tool_call.id,
                type=tool_call.type,
                function=FunctionCall(
                    name=tool_call.function.name,
                    arguments=json.loads(tool_call.function.arguments)
                )
            ) for tool_call in response_message.tool_calls]
        )
    else:
        return LLMResponse(**response_message.model_dump())