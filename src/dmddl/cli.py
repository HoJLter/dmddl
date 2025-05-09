import argparse
import questionary
from config.config import LLMSettings

AVAILABLE_PROVIDERS = ["OpenAI", "Deepseek"]


def choose_provider(providers):
    selected = questionary.select("Choose your LLM provider:",
                                   choices=providers).ask()
    return selected


def ask_api_key():
    api_key = questionary.password("Enter your api key:").ask()
    return api_key


def set_parameters():
    settings = LLMSettings()

    llm_provider = choose_provider(AVAILABLE_PROVIDERS)
    api_key = ask_api_key()

    settings['DMDDL_CUR_PROVIDER'] = llm_provider
    settings['DMDDL_LLM_KEY'] = api_key


if __name__ == '__main__':
    set_parameters()
