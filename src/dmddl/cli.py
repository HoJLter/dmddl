import argparse
from time import sleep
import requests
import questionary
from config.config import LLMSettings
from rich import print
from rich.console import Console
from llm.llm import openai_request


AVAILABLE_PROVIDERS = ["OpenAI", "Deepseek"]


def choose_provider(providers):
    selected = questionary.select("Choose your LLM provider:",
                                   choices=providers).ask()
    return selected


def ask_api_key():
    api_key = questionary.password("Enter your api key:").ask()
    return api_key


def make_test_query(provider, api_key):
    console = Console()
    with console.status("[bold blue]Making test query") as status:
        if provider == "OpenAI":
            try:
                response = openai_request("Hello! Its a test query :)", api_key)
                print(f"\n[green bold]{response} \nAll done! Your api key is correct!")
            except:
                print("Your api key is incorrect! Use -c (--config) to set another api key")


def set_parameters():
    settings = LLMSettings()

    llm_provider = choose_provider(AVAILABLE_PROVIDERS)
    api_key = ask_api_key()

    settings['DMDDL_CUR_PROVIDER'] = llm_provider
    settings['DMDDL_LLM_KEY'] = api_key


def main():
    settings = LLMSettings()

    llm_provider = settings['DMDDL_CUR_PROVIDER']
    api_key = settings['DMDDL_LLM_KEY']

    make_test_query(llm_provider, api_key)


if __name__ == '__main__':
    main()
