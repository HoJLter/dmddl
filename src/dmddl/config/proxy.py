import asyncio
from bs4 import BeautifulSoup
import aiohttp
import requests
from rich.console import Console


def get_proxy_list():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxies = []
    table = soup.find('table')
    for row in table.tbody.find_all('tr'):
        cols = row.find_all('td')
        if (cols[4].text == 'elite proxy' or cols[4].text == 'anonymous') and cols[6].text == 'yes':
            proxies.append(f"http://{cols[0].text}:{cols[1].text}")
    return proxies


async def is_valid_proxy(url, proxy, session):
    try:
        async with session.get(url, proxy=proxy, timeout=5):
            return proxy

    except (aiohttp.ClientError, ConnectionResetError, asyncio.TimeoutError):
        return None


async def get_valid_proxies(console: Console):
    proxies = get_proxy_list()
    url = "https://api.openai.com/v1/chat/completions"
    valid_proxies = []

    with console.status("[blue bold]Checking proxies...") as status:
        async with aiohttp.ClientSession() as session:
            tasks = [is_valid_proxy(url, proxy, session) for proxy in proxies]
            for i, task in enumerate(asyncio.as_completed(tasks), 1):
                proxy = await task
                if proxy:
                    valid_proxies.append(proxy)
                    console.print(f"[green bold]✅ Valid proxy:   {proxy}")
                else:
                    console.print(f"[red bold]❌ Invalid proxy: {proxies[i - 1]}")
                status.update(f"[blue bold]Checked {i}/{len(proxies)} proxies | Valid: {len(valid_proxies)}")

    return valid_proxies

