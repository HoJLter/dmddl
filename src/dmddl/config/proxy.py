import asyncio
from bs4 import BeautifulSoup
import aiohttp
import requests


def get_proxy_list():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxies = []
    table = soup.find('table')
    for row in table.tbody.find_all('tr'):
        cols = row.find_all('td')
        if cols[4].text == 'elite proxy' and cols[6].text == 'yes':
            proxies.append(f"http://{cols[0].text}:{cols[1].text}")

    return proxies


async def test_request(url, proxy, session):
    try:
        async with session.get(url, proxy=proxy, timeout=5) as response:
            return proxy
    except:
        pass


async def get_valid_proxies():
    proxies = get_proxy_list()
    url = "https://platform.openai.com"
    async with aiohttp.ClientSession() as session:
        tasks = [test_request(url, proxy, session) for proxy in proxies]
        good_proxies = [proxy for proxy in await asyncio.gather(*tasks) if proxy]
        return good_proxies
