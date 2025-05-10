import questionary
from config.settings import LLMSettings
from rich import print
from rich.syntax import Syntax
from rich.console import Console
from models.llm import openai_request
from models.prompt import prompt as base_prompt
import argparse


AVAILABLE_PROVIDERS = ["OpenAI"]


def choose_provider(providers):
    provider = questionary.select("Choose your LLM provider:",
                                   choices=providers).ask()
    if provider:
        return provider
    else:
        raise Exception("LLM Provider isn't found")


def ask_api_key():
    api_key = questionary.password("Enter your api key:").ask()
    if api_key:
        return api_key
    else:
        raise Exception("API key isn't provided")


def make_query(provider, api_key, prompt):
    console = Console()
    with console.status("[bold blue]Making query. Wait for result..."):
        if provider == "OpenAI":
            response = openai_request(base_prompt+prompt, api_key)
            return response

        raise Exception("LLM Provider not found")


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


    if not args.source and not args.config:
        print("[red bold]You must provide any arguments:\n"
              "-c (--config): opens settings menu\n"
              "-s (--source): specify the input file")


    if args.config:
        set_parameters()
    if args.source:
        with open(args.source, "r", encoding='utf-8') as file:
            user_prompt = file.read()
        syntax = Syntax(user_prompt, 'sql', line_numbers=True)
        print(f"\n[yellow bold]{args.source.upper()}\n", )
        console.print(syntax)
        confirmation = questionary.confirm("Do you want to use this DDL script to generate the insert?").ask()

        if confirmation:
            success, response = make_query(provider=llm_provider,
                                           api_key=api_key,
                                           prompt=user_prompt)
            write_output_file(response)
            syntax = Syntax(response, 'sql', line_numbers=True)
            print("\n\n[yellow bold]OUTPUT.TXT\n",)
            console.print(syntax)
            if success:
                print("[green bold] Your DML script is ready! Check output.txt")
            if not success:
                print("[red bold] Error has occurred... Check output.txt")


if __name__ == '__main__':
    main()
