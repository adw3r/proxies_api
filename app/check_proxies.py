import asyncio

import aiohttp
import loguru
from aiohttp_socks import ProxyConnector

PROXIES = 'http://127.0.0.1:8182/proxies'
SEMAPHORE = asyncio.Semaphore(1000)
logger = loguru.logger


async def check_proxy(proxy: str) -> dict | None:
    connector = None
    if 'socks' in proxy:
        connector = ProxyConnector.from_url(proxy)
    try:
        async with SEMAPHORE:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(30), connector=connector) as session:
                async with session.get('http://ip-api.com/json/?fields=8217', proxy=proxy) as response:
                    text = await response.text()
                    json_response = await response.json()
                    ip = json_response.get('query')
                    json_response['proxy'] = proxy
                    if ip:
                        return json_response
    except Exception as error:
        logger.error(error)
        # logger.error(f'{text} {proxy}')


async def check_pool(pool):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{PROXIES}/{pool}', params={'method': 'pool'}) as response:
            proxies = str(await response.text()).strip().splitlines()
    logger.info(pool)
    cors = [asyncio.create_task(check_proxy(proxy)) for proxy in proxies]
    for res in asyncio.as_completed(cors):
        print(await res)


async def check_pools():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            pools = await response.json()
            logger.info(pools)
            for pool in pools:
                await check_pool(pool)


if __name__ == '__main__':
    asyncio.run(check_pool('gold'))
