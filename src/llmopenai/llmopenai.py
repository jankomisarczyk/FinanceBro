import json
import logging
from dataclasses import dataclass, asdict
from typing import Any

import openai

logger = logging.getLogger(__name__)

@dataclass
class LLMResponse:
    content: str = None
    function_call: dict[str, Any] = None
    role: str = None

@dataclass
class Function:
    name: str
    description: str
    parameters: dict[str, Any]

@dataclass
class Message:
    role: str
    content: str


async def call_llm(
    messages: list[Message],
    model: str = "gpt-3.5-turbo-0613",
    function_call: str = "auto",
    functions: list[Function] = None
) -> LLMResponse:
    messages = [asdict(message) for message in messages]
    logger.debug(f"~~ LLM Request ~~\n{messages}")

    if functions:
        response = await openai.ChatCompletion.acreate(
            model=model,
            messages=messages,
            functions=[asdict(function) for function in functions],
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