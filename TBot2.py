from services.api import Api
from models.update import Update
from typing import Callable, List
import requests
import time
import parser
import logging

logging.basicConfig(level=logging.INFO, handlers=[
                    logging.FileHandler("TBot2.log"), logging.StreamHandler()])


class TBot2:
    def __init__(self, token: str) -> None:
        self.token = token
        self.BASE_URL = f'https://api.telegram.org/bot{token}/'
        self.routes = {}
        self.lastUpdateId = None
        self.api = Api()

    def __addToRoutes(self, type: str, keyword: str, callbackFn: Callable) -> bool:
        if type not in self.routes:
            self.routes[type] = {}

        if keyword:
            self.routes[type][keyword] = callbackFn
        else:
            # catch_all etc.
            self.routes[type] = callbackFn

        return True

    def contains(self, text):
        def decorator(callbackFn):
            self.__addToRoutes("contains", text, callbackFn)
        return decorator

    def catch_all(self):
        def decorator(callbackFn):
            self.__addToRoutes("catch_all", None, callbackFn)
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

        for update in updates:
            handled = False

            self.lastUpdateId = update.update_id
            logging.info(f"Updated last update Id to: {update.update_id}")

            # construct prefix trie instead of iterating

            for keyword in self.routes['contains']:
                if keyword in update.text:
                    fn = self.routes['contains'][keyword]
                    resp = fn(update)
                    if resp:
                        self.sendMessage(resp, update.message.chat.id)
                    handled = True

            if not handled:
                if 'catch_all' in self.routes:
                    resp = self.routes['catch_all'](update)
                    self.sendMessage(resp, update.message.chat.id)

        self.markUpdateAsHandled()
        logging.info(
            f"Acknowledge updates with last seen id: {self.lastUpdateId}")

    def sendMessage(self, reply: str, chat_id: str) -> bool:
        url = self.BASE_URL + 'sendMessage'

        data = {
            "text": reply,
            "chat_id": chat_id
        }

        r = requests.post(url, data=data)

        result = r.status_code == 200

        logging.debug("sendMessage success: " + str(result))

        return result

    def markUpdateAsHandled(self):
        self.lastUpdateId += 1  # +1 of last seen update, will not affect next update
        url = self.BASE_URL + 'getUpdates'
        params = {
            'offset': self.lastUpdateId
        }

        r = requests.get(url, params=params)

        return r.status_code == 200

    def ListenAndServe(self):
        logging.info("Started Polling")
        while 1:
            time.sleep(1)
            updates = self.getUpdates()
            if updates:
                logging.debug(f"[updates] {updates}")
                self.handleUpdates(updates)
