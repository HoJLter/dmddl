class LLMProvider:
    def __init__(self, api_key_url, description):
        self.api_key_url = api_key_url
        self.description = description

    def __str__(self):
        return (f"{self.description}\n"
                f"You can get your api key from {self.api_key_url}")


class OpenAI(LLMProvider):
    def make_request(self):
        pass


class Deepseek(LLMProvider):
    def make_request(self):
        pass