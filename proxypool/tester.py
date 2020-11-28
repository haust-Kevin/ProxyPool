from dao.redis_dao import RedisClient
from filter import proxy_filter

BATCH_TEST_SIZE = 1000


class ProxyTester:
    def __init__(self):
        self.redis = RedisClient()

    def run(self):
        all_proxies = self.redis.all()
        print('tested\t{}'.format(len(all_proxies)))
        for i in range(0, len(all_proxies), BATCH_TEST_SIZE):
            stop = i + BATCH_TEST_SIZE if i + BATCH_TEST_SIZE <= len(all_proxies) else None
            testd_proxies = all_proxies[i:stop]
            valid_proxies = proxy_filter(testd_proxies)
            invalid_proxies = list(set(testd_proxies) - set(valid_proxies))
            if invalid_proxies:
                print('invalid\t{}'.format(len(invalid_proxies)))
                self.redis.decrease_many(invalid_proxies)
            if valid_proxies:
                print('valid\t{}'.format(len(valid_proxies)))
                self.redis.maximize_many(valid_proxies)


if __name__ == '__main__':
    ProxyTester().run()
