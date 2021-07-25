from models.message import Message
from models.sender import Sender
from models.update import Update
from models.chat import Chat


def parse_updates(updates: dict) -> dict:
    # check for no new updates
    if len(updates['result']) == 0:
        return None
    
    results = []
    
    for entry in updates['result']:
        update = Update()
        m = Message()
        s = Sender()
        c = Chat()

        msg = entry['message']

        _from = msg['from']
        _chat = msg['chat']

        s.id = _from['id']
        s.is_bot = _from['is_bot']
        s.first_name = _from['first_name']
        s.username = _from['username']

        c.id = _chat['id']
        c.first_name = _chat['first_name']
        c.username = _chat['username']
        c.type = _chat['type']

        m.sender = s
        m.chat = c

        update.message = m
        update.text = msg['text']
        update.date = msg['date']
        update.update_id = entry['update_id']
        results.append(update)

    return results