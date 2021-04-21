import json
from dataclasses import dataclass
from DataCl import *


# делает из  сообщения dataclass
class MsgParser:
    def __init__(self):
        pass

    def parse(self, parser_data_py):
        if "action" in parser_data_py:
            action = parser_data_py["action"]
            if action == "quit":
                return AnwQuit(action=parser_data_py['action'])

            elif action == "authenticate":
                return Authenticate(account_name=parser_data_py["user"]["account_name"],
                                    password=parser_data_py["user"]["password"])
            elif action == "presence":
                return Presence(account_name=parser_data_py["user"]["account_name"],
                                status=parser_data_py["user"]["status"])
            elif action == "probe!!!":
                return Probe(action=parser_data_py['action'])

        elif "response" in parser_data_py:
            response = parser_data_py["response"]
            if response == "200":
                return Responce(response=parser_data_py['response'],
                                alert=parser_data_py['alert'])
            elif response == "402":
                return ResponceError(response=parser_data_py['response'],
                                     error=parser_data_py['error'])