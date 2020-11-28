import socket
import time
from multiprocessing import Process

from api import app
from getter import FreeProxyGetter

TESTER_CYCLE = 60 * 10
GETTER_CYCLE = 60 * 10

TESTER_ENABLE = True
GETTER_ENABLE = True
API_ENABLE = True


class Scheduler:
    def __init__(self):
        pass

    def schedule_getter(self, cycle=GETTER_CYCLE):
        getter = FreeProxyGetter()
        while True:
            getter.run()
            time.sleep(cycle)

    def schedule_tester(self, cycle=TESTER_CYCLE):
        getter = FreeProxyGetter()
        while True:
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        app.run(socket.gethostbyname(socket.gethostname()), 8000)

    def run(self):
        if GETTER_ENABLE:
            Process(target=self.schedule_getter).start()
        if TESTER_ENABLE:
            Process(target=self.schedule_tester).start()
        if API_ENABLE:
            Process(target=self.schedule_api).start()


def main():
    Scheduler().run()


if __name__ == '__main__':
    main()
