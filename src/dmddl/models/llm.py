from http.client import RemoteDisconnected

import requests
from requests.exceptions import ProxyError
from rich import print

def openai_request(prompt, api_key, console, proxies = None):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    url = "https://api.openai.com/v1/chat/completions"
    data = {
        'model': 'gpt-4o-mini',
        'messages':[
            {
                'role': 'developer',
                'content': prompt
             }
        ]
    }

    with console.status("[bold blue]Making query. Wait for result..."):
        if proxies:
            for proxy in proxies:
                try:
                    req_proxies = {
                        "https": proxy
                    }
                    print(f"[blue bold]Using proxy: {proxy}")
                    response = requests.post(url=url, headers=headers, json=data, proxies = req_proxies)
                    if response.status_code == 200:
                        break
                except:
                    print(f"\n[red bold]Proxy error... Trying next proxy")
        else:
            response = requests.post(url=url, headers=headers, json=data)


    if response.status_code == 200:
        return True, response.json()['choices'][0]['message']['content']

    elif response.status_code == 401:
        return False, ("Your api key is incorrect. \n"
                       "Use -c (--config) to configurate app and set new API key.")

    else:
        return False, response.json()['error']['message']


