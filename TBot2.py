from typing import Callable
import requests
import time


class TBot2:
    def __init__(self, token: str) -> None:
        self.token = token
        self.BASE_URL = f'https://api.telegram.org/bot{token}/'
        self.routes = {}

    def __addToRoutes(self, type: str, keyword: str, callbackFn: Callable) -> bool:
        if type not in self.routes:
            self.routes[type] = {}

        self.routes[type][keyword] = callbackFn

        return True

    def contains(self, text):
        def decorator(callbackFn):
            self.__addToRoutes("contains", text, callbackFn)
        return decorator

    def getUpdates(self):
        r = requests.get(self.BASE_URL + 'updates')

    def ListenAndServe(self):
        while 1:
            time.sleep(1)
            print('checking for updates')
