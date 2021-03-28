import json
from weakref import WeakKeyDictionary

from Sockett import SocketClass
import threading
import time
from select import select

# BUFF = 2048
# ENCODDING = 'utf-8'
# HOST = ""
# PORT = 1111
# Ответы сервераa

LIST_AUTH = [
    {
        "response": '200',
        "alert": "OK!"
    },
    {
        "response": '402',
        "error": "ERROR!"
    },
]
PROBE = {
    "action": "probe!!!",
}

# =====================================
"""Реализовать дескриптор для класса серверного сокета,
 а в нем — проверку номера порта. Это должно быть целое число (>=0).
  Значение порта по умолчанию равняется 7777. Дескриптор надо создать 
  в отдельном классе. Его экземпляр добавить в пределах класса серверного сокета.
   Номер порта передается в экземпляр дескриптора при запуске сервера.
"""


# =====================дискриптор====
class ServerProp:
    def __init__(self, name, type_name, default=None):
        print("__init__")
        self.name = "_" + name
        self.type = type_name
        self.default = default if default else type_name()

    def __get__(self, instance, cls):
        print("__get__")
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        print("__set__")
        if not (1111 <= value <= 8888):
            raise ValueError("port должен быть от 1111 до 8888")
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        print("__delete__")
        raise AttributeError("Невозможно удалить атрибут")


class Server(SocketClass):
    def __init__(self):
        super(Server, self).__init__()
        self.HOST = ""
        self.users_sockets = []
        self.to_monitor = []

    port = ServerProp('port', int, 10000)

    def b_decode_str_foo(self, b_request_recvd):  # from b'' (json) to str
        return b_request_recvd.decode(self.ENCODDING)

    def str_loads_dict_foo(self, request_str):  # from str to  dict
        return json.loads(request_str)

    def py_dumps_str_foo(self, param_server):  # from py (dict) to str
        return json.dumps(param_server)

    # ================prepare=====================
    def set_up(self):
        self.to_monitor.append(self)
        self.bind((self.HOST, self.port))
        self.listen(5)
        print('server is listening....')
        self.main_loop()

    def send_data(self, data):
        for user_socket in self.users_sockets:
            user_socket.send(data)

    def listen_socket(self, listened_sock=None):
        """Принимает сообщения от клиента (слушает)
        затем отправка сообщений send_message()"""
        time.sleep(2)
        print('listening user')
        request = listened_sock.recv(self.BUFF)
        if request:
            request_str = self.b_decode_str_foo(request)
            request_dict = self.str_loads_dict_foo(request_str)

            if 'action' in request_dict and request_dict['action'] == 'authenticate':
                for var_response in LIST_AUTH:
                    if 'response' in var_response and var_response['response'] == '200':
                        msg = str(var_response['alert'])
                        listened_sock.send(msg.encode(self.ENCODDING))
                        print(f'server send {msg}')

            elif 'action' in request_dict and request_dict['action'] == 'presence':
                msg = self.py_dumps_str_foo(PROBE).encode(self.ENCODDING)
                listened_sock.send(msg)
                print('прилетел presence')
                print(f'server send {msg.decode(self.ENCODDING)}')

            elif 'action' in request_dict and request_dict['action'] == 'quit':
                qwe = listened_sock.send('finish'.encode(self.ENCODDING))
                print(f'прилетел quit {time.ctime()}')
                print(f'server send {qwe} --"finish"')

            elif 'action' in request_dict and request_dict['action'] != 'authenticate':
                for var_response in LIST_AUTH:
                    if 'response' in var_response and var_response['response'] == '402':
                        msg = str(var_response['error'])
                        listened_sock.send(msg.encode(self.ENCODDING))
                        print('ошибка auth')
                        print(f'server send {msg}')

            print(f'User sent {request_dict["action"]}')
            self.send_data(request)
        # user_sock.close()

    def accept_sockets(self, tcpSerSock=None):
        print('Waiting for client...')
        user_socket, address = self.accept()  # blocking function

        print(f'Connected from: <<{address[0]}>>')

        self.to_monitor.append(user_socket)  # передаем второй сокет (клиентский)

        self.users_sockets.append(user_socket)

        listen_accepted_user = threading.Thread(target=self.listen_socket,
                                                args=(user_socket,))
        listen_accepted_user.start()
        # messages
        # messages
        # messages
        # listen_accepted_user.join() # blocking function. waiting ...
        print(self.users_sockets)

    def main_loop(self):
        while True:
            ready_to_read, _, _ = select(self.to_monitor, [], [])
            for sock in ready_to_read:
                if sock is self:
                    self.accept_sockets(sock)
                else:
                    self.listen_socket(sock)  # send_message()


if __name__ == '__main__':
    server = Server()
    server.set_up()
    # server.port=1111
