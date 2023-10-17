#!/usr/bin/env python

import argparse
import asyncio

from dotenv import load_dotenv
from src.config import Config
from src.financebro import FinanceBro


def parse_args():
    parser = argparse.ArgumentParser(description="FinanceBro CLI tool")

    parser.add_argument(
        "-t",
        "--task",
        help="Run a specific task, wrapped in quotes",
    )

    return parser.parse_args()


async def start():
    load_dotenv()
    parsed_args = parse_args()
    if parsed_args.task:
        task = parsed_args.task
    else:
        print("What would you like me to do?")
        print("> ", end="")
        task = input()
    print(task)

    config = Config.global_config()
    # mybe I will do DB connection for files
    financebro = FinanceBro(task=task, config=config)
    # body = Body(task=task, config=config)
    # await body.setup()
    # while output := await body.cycle():
    #     if output.observation:
    #         print("\n=== Cycle Output ===")
    #         print(output.observation.response)


def main():
    asyncio.run(start())

if __name__ == "__main__":
    main()