import asyncio

import aiohttp

TIMEOUT = 15


async def _test_signal_proxy(proxy):
    """
    异步检测单个代理是否有效
    :param proxy: 待检测的代理
    :return: 是否有效
    """
    url = 'http://httpbin.org/ip'
    coon = aiohttp.TCPConnector(verify_ssl=False)
    async with aiohttp.ClientSession(connector=coon) as session:
        full_proxy = 'http://' + proxy
        try:
            async with session.get(url, proxy=full_proxy, timeout=TIMEOUT)as resp:
                json_data = await resp.json()
                return json_data['origin'] == proxy.split(':')[0]
        except:
            return False


def proxy_filter(proxies):
    """
    从一个代理列表中过滤出可用的代理
    :param proxies: 待筛选的代理列表
    :return: 可用的代理
    """
    loop = asyncio.get_event_loop()
    fatures = [loop.create_task(_test_signal_proxy(proxy)) for proxy in proxies]
    loop.run_until_complete(asyncio.wait(fatures))
    test_result = [future.result() for future in fatures]
    return [proxies[i] for i in range(len(proxies)) if test_result[i]]
