from pathlib import Path
import json



class UserConfig:
    """Represents dmddl config object. Uses singleton pattern"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance


    def __init__(self):
        expected_conf_path = Path.home() / "dmddl.json"
        # if not expected_conf_path.exists():
        with open(expected_conf_path, "w") as file:
            __conf_structure = {
                "api-keys":{
                    "OpenAI": "",
                    "Deepseek": ""
                },
                "in_use_model": ""
            }
            json.dump(__conf_structure, file)
        self.conf_path = expected_conf_path


    @property
    def content(self) -> dict:
        with open(self.conf_path, "r") as file:
            content = json.load(file)
            return content


    @content.setter
    def content(self, new_content):
        for key in self.content:
            print(key)
        with open(self.conf_path, "w") as file:
            json.dump(new_content, file, indent=4)






config = UserConfig()
config.content = {"test": "test"}
print(config.content)