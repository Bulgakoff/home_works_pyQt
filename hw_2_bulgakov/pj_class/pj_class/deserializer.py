import json


class Deserializer:
    def __init__(self, loads=json.loads,
                 encodding='utf-8'):
        self._loads = loads
        self._encodding = encodding


    def b_decode_str_foo(self, b_request_recvd):  # from b'' (json) to str
        return b_request_recvd.decode(self._encodding)

    def str_loads_dict_foo(self, request_str):  # from str to  dict
        return self._loads(request_str)