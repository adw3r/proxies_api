import asyncio

import aiohttp
import requests
import loguru

URL = 'http://ip-api.com/json/?fields=8217'

logger = loguru.logger
semaphore = asyncio.Semaphore(5000)


async def check_proxy(proxy: str) -> dict | None:
    try:
        async with semaphore:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(30)) as session:
                async with session.get(URL, proxy=proxy) as response:
                    json_response = await response.json()
                    ip = json_response.get('query')
                    if ip:
                        json_response['proxy'] = proxy
                        return json_response
    except Exception as error:
        logger.error(error)
        return None


async def main():
    urls = ['http://localhost:8182/proxies/parsed?method=pool','http://localhost:8182/proxies/west?method=pool']
    for url in urls:
        proxies = requests.get(url).text.strip().splitlines()
        cors = [asyncio.create_task(check_proxy(proxy)) for proxy in proxies]
        for res in asyncio.as_completed(cors):
            await_res = await res
            if await_res:
                logger.info(await_res)


if __name__ == '__main__':
    asyncio.run(main())
