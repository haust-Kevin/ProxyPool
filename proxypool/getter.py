import itertools
import random
import re
import time
from urllib.parse import urljoin

from lxml import etree

from dao.redis_dao import RedisClient
from utils import get_page

POOL_HIGH_THRESHOLD = 30000
BATCH_STORE_SIZE = 1000


class ProxyMetaClass(type):
    def __new__(mcs, name, bases, attrs):
        attrs['__CrawFunc__'] = [k for k in attrs.keys() if 'crawl_' in k]
        return type.__new__(mcs, name, bases, attrs)


class FreeProxyGetter(metaclass=ProxyMetaClass):
    def __init__(self):
        self.redis = RedisClient()

    def over_threshold(self):
        return self.redis.count() > POOL_HIGH_THRESHOLD

    def random_sleep(self):
        time.sleep(random.randint(3, 6))

    def proxy_gene(self):
        for crawl_func in self.__CrawFunc__:
            for proxy in eval('self.{}()'.format(crawl_func)):
                yield proxy

    def run(self):
        if not self.over_threshold():
            proxies_g = self.proxy_gene()
            for i in range(0, POOL_HIGH_THRESHOLD, BATCH_STORE_SIZE):
                proxies = list(itertools.islice(proxies_g, 0, BATCH_STORE_SIZE))
                if not proxies:
                    break
                self.redis.add_many(proxies)

    def crawl_xiladaili(self):
        """
        爬取西拉代理的免费代理
        :return: 免费代理生成器
        """
        url_pat_li = [
            'http://www.xiladaili.com/gaoni/{}/',
            'http://www.xiladaili.com/https/{}/',
        ]
        try:
            for url_pat in url_pat_li:
                for i in range(10):
                    html_ele = etree.HTML(get_page(url_pat.format(i + 1)))
                    self.random_sleep()
                    proxy_ele_li = html_ele.xpath('//table[@class="fl-table"]/tbody/tr')
                    for proxy_ele in proxy_ele_li:
                        if '高匿' in proxy_ele.xpath('./td[3]/text()')[0]:
                            yield proxy_ele.xpath('./td[1]/text()')[0]
        except Exception as e:
            print(e, '爬取西拉代理发生异常')

    def crawl_xiaohuandaili(self):
        """
        爬取小幻代理的免费代理
        :return: 免费代理生成器
        """
        init_url = 'https://ip.ihuan.me/today.html'
        try:
            html_ele = etree.HTML(get_page(init_url))
            re_pat = re.compile('\d+.\d+.\d+.\d+:\d+')
            for sub_url in html_ele.xpath('//div[@class="panel-body"]/div/a/@href')[0:1]:
                url = urljoin(init_url, sub_url)
                html_ele = etree.HTML(get_page(url))
                self.random_sleep()
                for item in html_ele.xpath('//div[@class="panel-body"]/p[@class="text-left"]/text()'):
                    ret = re_pat.search(item)
                    if ret:
                        yield ret.group()
        except Exception as e:
            print(e, '爬取小幻代理发生异常')


if __name__ == '__main__':
    FreeProxyGetter().run()
