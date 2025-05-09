import questionary
from config.config import LLMSettings
from rich import print
from rich.console import Console
from llm.llm import openai_request
from llm.prompt import prompt as base_prompt
import argparse

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


def make_query(provider, api_key, prompt):
    console = Console()
    with console.status("[bold blue]Making query. Wait for result...") as status:
        if provider == "OpenAI":
            response = openai_request(base_prompt+prompt, api_key)
            print(response)


def set_parameters():
    settings = LLMSettings()

    llm_provider = choose_provider(AVAILABLE_PROVIDERS)
    api_key = ask_api_key()

    settings['DMDDL_CUR_PROVIDER'] = llm_provider
    settings['DMDDL_LLM_KEY'] = api_key


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", action="store_true")
    parser.add_argument("-s", "--source", action="store_true")

    return parser.parse_args()


def main():
    settings = LLMSettings()
    args = get_args()

    llm_provider = settings['DMDDL_CUR_PROVIDER']
    api_key = settings['DMDDL_LLM_KEY']

    if not api_key or args.config:
        set_parameters()

    if args.source:
        print(args.source)

    print(args)

if __name__ == '__main__':
    main()
