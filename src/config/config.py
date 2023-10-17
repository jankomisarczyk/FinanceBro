import logging
import os
from typing import ClassVar

import coloredlogs
import openai
from pydantic_settings import BaseSettings

DEFAULT_DECOMPOSER_MODEL = "gpt-4"
DEFAULT_PLANNER_MODEL = "gpt-4"
DEFAULT_DECIDER_MODEL = "gpt-4"
LOG_FORMAT = (
    "%(levelname)s %(asctime)s.%(msecs)03d %(filename)s:%(lineno)d- %(message)s"
)


class Config(BaseSettings):

    log_level: str
    openai_api_key: str
    decomposer_model: str = DEFAULT_DECOMPOSER_MODEL
    planner_model: str = DEFAULT_PLANNER_MODEL
    decider_model: str = DEFAULT_DECIDER_MODEL
    process_timeout: int = 30
    workspace_path: str = "workspace"

    _global_config: ClassVar["Config"] = None

    def __init__(self, **kwargs) -> "Config":
        super().__init__(**kwargs)
        self.setup_logging()
        openai.api_key = self.openai_api_key

    def setup_logging(self) -> logging.Logger:
        os.makedirs("logs", exist_ok=True)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)

        file_handler = logging.FileHandler("logs/debug.log")
        file_handler.setLevel("DEBUG")
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

        logging.basicConfig(
            level=self.log_level,
            format=LOG_FORMAT,
            datefmt="%H:%M:%S",
            handlers=[
                console_handler,
                file_handler,
            ],
        )
        print("doing loggoinh")
        coloredlogs.install(
            level=self.log_level,
            fmt=LOG_FORMAT,
            datefmt="%H:%M:%S",
        )

    @classmethod
    def set_global_config(cls, config_obj: "Config" = None) -> "Config":
        """
        Optionally set a global config object that can be used anywhere (You can still attach a separate instance to
        each Body)
        """
        cls._global_config = config_obj or cls()
        return cls._global_config

    @classmethod
    def global_config(cls) -> "Config":
        return cls._global_config or cls.set_global_config()