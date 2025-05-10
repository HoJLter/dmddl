import dotenv
import os
from pathlib import Path

def get_dotenv_path():
    env_path = dotenv.find_dotenv()

    if not env_path:
        env_dir = "config"
        env_path = os.path.join(env_dir, ".env")
        os.makedirs(env_dir, exist_ok=True)
        Path(env_path).touch(exist_ok=True)
    return env_path


ENV_PATH = get_dotenv_path()

class LLMSettings:
    """
    Class that represents .env models settings (Singleton)
    """
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(LLMSettings, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if len(dotenv.dotenv_values(ENV_PATH))<2:
            dotenv.set_key(ENV_PATH, "DMDDL_CUR_PROVIDER", "")
            dotenv.set_key(ENV_PATH, "DMDDL_LLM_KEY", "")

    def __setitem__(self, key, value):
        dotenv.set_key(ENV_PATH, key, value)

    def __getitem__(self, item):
        return dotenv.get_key(ENV_PATH, key_to_get=item)

    def __str__(self):
        lines = []
        for key, item in dotenv.dotenv_values().items():
            lines.append(" = ".join([key, item]))

        content = "\n".join(lines)
        return content

