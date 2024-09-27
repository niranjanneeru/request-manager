import json

from app.cache import Cache


class ChatHistoryCache:
    def __init__(self):
        self.cache = Cache()

    def get_chat_history(self, key):
        chat_history = self.cache.get(key)
        if chat_history:
            chat_history = json.loads(chat_history)
        else:
            chat_history = []
        return chat_history

    def set_chat_history(self, key, chat_history):
        self.cache.set(key, json.dumps(chat_history))
