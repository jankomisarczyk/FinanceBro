#!/usr/bin/env python

import argparse
import asyncio

from dotenv import load_dotenv
from src.config import Config
from src.financebro.financebro import FinanceBro


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

    config = Config()
    # mybe I will do DB connection for files
    financebro = FinanceBro(task=task, config=config)
    await financebro.setup()

    while step := await financebro.cycle():
        print("\n=== Cycle Output ===")
        print(step.model_dump(exclude_none=True))

def main():
    asyncio.run(start())

if __name__ == "__main__":
    main()