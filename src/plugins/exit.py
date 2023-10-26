import logging

from src.plugins.plugin import Plugin
from src.llmopenai import Argument
from src.interns.step import Execution

PLUGIN_NAME = "exit"
PLUGIN_DESCRIPTION = "Exits the program, signalling that all tasks have bene completed and all goals have been met."
ARGS_SCHEMA = {
    "success": Argument(type="boolean", description="Success"),
    "conclusion": Argument(type="string", description="Reflect on the task execution process.")
}

logger = logging.getLogger(__name__)


class Exit(Plugin):
    name = PLUGIN_NAME
    description = PLUGIN_DESCRIPTION
    args_schema = ARGS_SCHEMA
    categories = ["System"]

    async def arun(success: bool = True, conclusion: str = "") -> Execution:
        if success:
            logger.info("\n=== Task completed ===")
        else:
            logger.info("\n=== Task failed ===")

        logger.info(conclusion)

        return Execution(observation="Exited", complete=True)