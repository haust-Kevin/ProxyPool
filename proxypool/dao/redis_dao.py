from random import choice

import redis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWD = 'password'
REDIS_DB = 0

REDIS_PROXY_KEY = 'proxies'
MAX_SCORE = 10
INITIAL_SCORE = 3


class PoolEmptyError(BaseException):
    def __str__(self):
        return '代理池中无可用代理，请过一段时间再继续获取'


class RedisClient:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWD, db=REDIS_DB):
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=db, decode_responses=True)

    def add(self, proxy):
        """ 添加新代理，并赋予初始分数 """
        return self.add_many([proxy])

    def add_many(self, proxies):
        """ 添加多个代理，并赋予初始分数 """
        return self.db.zadd(REDIS_PROXY_KEY, dict(zip(proxies, [INITIAL_SCORE] * len(proxies))), nx=True)

    def decrease(self, proxy):
        """ 将代理的分数减一 """
        score = self.db.zscore(REDIS_PROXY_KEY, proxy)
        if score:
            return self.db.zincrby(REDIS_PROXY_KEY, -1, proxy)
        else:
            return self.db.srem(REDIS_PROXY_KEY, proxy)

    def decrease_many(self, proxies):
        """ 将多个代理的分数减一 """
        for proxy in proxies:
            self.decrease(proxy)

    def maximize(self, proxy):
        """ 将代理的分数置为最大 """
        return self.db.zadd(REDIS_PROXY_KEY, {proxy: MAX_SCORE}, xx=True)

    def maximize_many(self, proxies):
        """ 将多个代理分数置为最大 """
        return self.db.zadd(REDIS_PROXY_KEY, dict(zip(proxies, [MAX_SCORE] * len(proxies))), xx=True)

    def random(self):
        """ 随即取出一个可用代理 """
        ret = self.db.zrangebyscore(REDIS_PROXY_KEY, MAX_SCORE, MAX_SCORE)
        if len(ret) == 0:
            ret = self.db.zrevrange(REDIS_PROXY_KEY, 0, 100)
        if len(ret) == 0:
            return None
        return choice(ret)

    def count(self):
        """ 获取代理的数量 """
        return self.db.zcard(REDIS_PROXY_KEY)

    def all(self):
        """ 获取所有的代理 """
        return self.db.zrangebyscore(REDIS_PROXY_KEY, 0, MAX_SCORE)
