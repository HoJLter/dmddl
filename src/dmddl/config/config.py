from typing import Literal, Dict

from openai import api_key
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from random import randint
from dmddl.llm import OpenAI, Deepseek


ALLOWED_MODELS = ["Deepseek", "OpenAI"]


class ApiKeysDict(dict):
    def __setitem__(self, key, value):
        if key in ALLOWED_MODELS:
            return super().__setitem__(key, value)
        else:
            raise ValueError("LLM Provider not found")


class LLMConfig(BaseSettings):
    llm_in_use:str | None
    api_keys: ApiKeysDict = Field(default_factory=ApiKeysDict)


config = LLMConfig(llm_in_use="Deepseek")
config.api_keys['Deepseek'] = "sdwafczawdca"
print(config.llm_in_use)