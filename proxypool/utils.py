import requests
from fake_useragent import UserAgent


def get_page(url):
    headers = {
        'User-Agent': UserAgent().random
    }
    return requests.get(url, headers=headers).text


def actual_ip(proxy):
    url = 'http://httpbin.org/ip'
    proxies = {
        'http': proxy,
        'https': proxy
    }
    resp = requests.get(url, proxies=proxies)
    return resp.json()['origin']
