import requests
from rich import print

def openai_request(prompt, api_key, proxies = None):
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

    if proxies:
        for proxy in proxies:
            try:
                print(f"[yellow bold]Using proxy: {proxy}")
                req_proxies = {
                    "https": proxy
                }
                response = requests.post(url=url, headers=headers, json=data, proxies = req_proxies)
                if response.status_code == 200:
                    break
            except:
                pass

    else:
        response = requests.post(url=url, headers=headers, json=data)


    if response.status_code == 200:
        return True, response.json()['choices'][0]['message']['content']

    elif response.status_code == 401:
        return False, ("Your api key is incorrect. \n"
                       "Use -c (--config) to configurate app and set new API key.")

    else:
        return False, response.json()['error']['message']


