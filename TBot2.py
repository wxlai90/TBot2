from models.update import Update
from typing import Callable, List
import requests
import time
import parser
import logging


logging.basicConfig(filename='TBot2.log', level=logging.DEBUG)


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
        url = self.BASE_URL + 'getUpdates'
        logging.debug(f"[getUpdates] {url}")
        r = requests.get(url)
        
        update = parser.parse_updates(r.json())
        
        return update


    def handleUpdates(self, updates: List[Update]):
        ''' Handles the updates by traversing our dict in a opinionated prioritized sequence 
            1. Contains
            2. Command
            3. ... 

            And calling the respectively handler func if found.
        '''

        # TODO: mark update as handled when polling.

        for update in updates:
            if update.text in self.routes['contains']:
                fn = self.routes['contains'][update.text]
                fn(update)

    def markUpdateAsHandled(self, current_update_id: int):
        # TODO: to implement, add offset to current update id, and call update
        pass


    def ListenAndServe(self):
        while 1:
            time.sleep(1)
            updates = self.getUpdates()
            if updates:
                logging.debug(f"[updates] {updates}")
                self.handleUpdates(updates)