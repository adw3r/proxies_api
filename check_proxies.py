import asyncio

import aiohttp
import loguru
import requests
from aiohttp_socks import ProxyConnector

PROXIES = 'http://localhost:8182/proxies'
URL = 'http://ip-api.com/json/?fields=8217'
SEMAPHORE = asyncio.Semaphore(5000)
logger = loguru.logger


async def check_proxy(proxy: str) -> dict | None:
    connector = None
    if 'socks' in proxy:
        connector = ProxyConnector.from_url(proxy)
    try:
        async with SEMAPHORE:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(30), connector=connector) as session:
                async with session.get(URL, proxy=proxy) as response:
                    text = await response.text()
                    logger.error(f'{text} {proxy}')
                    json_response = await response.json()
                    ip = json_response.get('query')
                    if ip:
                        json_response['proxy'] = proxy
                        return json_response
    except Exception as error:
        # logger.error(error)
        pass


async def check_pool(pool):
    logger.info(pool)
    proxies = requests.get(f'{PROXIES}/{pool}',
                           params={'method': 'pool'}).text.strip().splitlines()
    cors = [asyncio.create_task(check_proxy(proxy)) for proxy in proxies]
    for res in asyncio.as_completed(cors):
        await_res = await res
        if await_res:
            logger.info(await_res)


async def check_pools():
    pools = requests.get(PROXIES).json().keys()
    logger.info(pools)
    for pool in pools:
        await check_pool(pool)


if __name__ == '__main__':
    asyncio.run(check_pool('gold'))
