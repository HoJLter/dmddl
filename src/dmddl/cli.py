import questionary
from config.settings import LLMSettings
from rich import print
from rich.syntax import Syntax
from rich.console import Console
from models.llm import openai_request
from models.prompt import prompt as base_prompt
import argparse
import sys


AVAILABLE_PROVIDERS = ["OpenAI"]
sys.tracebacklimit = 10 # it makes errors more user-friendly (turn off for dev)


def choose_provider(providers):
    selected = questionary.select("Choose your LLM provider:",
                                   choices=providers).ask()
    return selected


def ask_api_key():
    api_key = questionary.password("Enter your api key:").ask()
    return api_key


def make_test_query(provider, api_key):
    console = Console()
    with console.status("[bold blue]Making test query"):
        if provider == "OpenAI":
            try:
                response = openai_request("Hello! Its a test query :)", api_key)
                print(f"\n[green bold]{response} \nAll done! Your api key is correct!")
            except KeyError:
                print("Your api key is incorrect! Use -c (--config) to set another api key")


def make_query(provider, api_key, prompt):
    console = Console()
    with console.status("[bold blue]Making query. Wait for result..."):
        if provider == "OpenAI":
            response = openai_request(base_prompt+prompt, api_key)
            return response
        raise ValueError("LLM Provider not found")


def write_output_file(data):
    with open("output.txt", 'w') as file:
        file.write(data)


def set_parameters():
    settings = LLMSettings()

    llm_provider = choose_provider(AVAILABLE_PROVIDERS)
    api_key = ask_api_key()

    settings['DMDDL_CUR_PROVIDER'] = llm_provider
    settings['DMDDL_LLM_KEY'] = api_key


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", action="store_true")
    parser.add_argument("-s", "--source")

    return parser.parse_args()


def main():
    settings = LLMSettings()
    args = get_args()
    console = Console()

    llm_provider = settings['DMDDL_CUR_PROVIDER']
    api_key = settings['DMDDL_LLM_KEY']

    if not api_key or args.config:
        set_parameters()

    if args.source:
        with open(args.source, "r", encoding='utf-8') as file:
            user_prompt = file.read()
        syntax = Syntax(user_prompt, 'sql', line_numbers=True)
        console.print(syntax)

        confirmation = questionary.confirm("Do you wanna use this DDL script?").ask()

        if confirmation:
            response = make_query(provider=llm_provider,
                                  api_key=api_key,
                                  prompt=user_prompt)
            write_output_file(response)
            syntax = Syntax(response, 'sql', line_numbers=True)
            console.print(syntax)
            print("[green bold] Your DML script is ready! Check output.txt")


if __name__ == '__main__':
    main()
