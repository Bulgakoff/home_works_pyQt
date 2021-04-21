from DataCl import *
from message_processor import MessageProcessor

class MessageHandler:
    def __init__(self):
        self._message_processor = MessageHandler()

    def on_msg(self, msg):
        if isinstance(msg, Responce):
            self._message_processor.on_auth_response(msg)
        elif isinstance(msg, Authenticate):
            self._message_processor.on_auth(msg)
        elif isinstance(msg, Probe):
            self.on_probe(msg)


