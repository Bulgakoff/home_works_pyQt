import json
from weakref import WeakKeyDictionary
import hmac
import os
from icecream import ic

from sockett import SocketClass
# from pj_class.sockett import SocketClass
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

# secret_key = b"our_secret_key"
# =====================дескриптор====
class ServerProp:
    def __init__(self, default) -> None:
        self._validate_value(default)
        self._default = default
        self._name = None



    def __get__(self, instance, owner):
        return getattr(instance, self._name, self._default)

    def __set__(self, instance, value):
        self._validate_value(value)
        setattr(instance, self._name, value)
        # setattr(instance,self.default,value)

    def __set_name__(self, owner, name):
        self._name = f'__{name}'

    @staticmethod
    def _validate_value(val):
        if not isinstance(val, int):
            raise TypeError(f'It is not got int, got {type(val)}!')
        if not 0 < val <= 65365:
            raise ValueError('Invalid port value')


class Server(SocketClass):
    def __init__(self):
        super(Server, self).__init__()
        self.HOST = ""
        self.users_sockets = []
        self.to_monitor = []
        self.secret_key = b"our_secret_key"

    port = ServerProp(10000)  # port == 10000

    def b_decode_str_foo(self, b_request_recvd):  # from b'' (json) to str
        return b_request_recvd.decode(self.ENCODDING)

    def str_loads_dict_foo(self, request_str):  # from str to  dict
        return json.loads(request_str)

    def py_dumps_str_foo(self, param_server):  # from py (dict) to str
        return json.dumps(param_server)

    def server_authenticate(self,connection, secret_key):
        """ Запрос аутентификаии клиента.
            сonnection - сетевое соединение (сокет);
            secret_key - ключ шифрования, известный клиенту и серверу
        """
        # 1. Создаётся случайное послание и отсылается клиентв
        message = os.urandom(32)
        connection.send(message)

        # 2. Вычисляется HMAC-функция от послания с использованием секретного ключа
        hash = hmac.new(secret_key, message,digestmod='sha256')
        digest = hash.digest()

        # 3. Пришедший ответ от клиента сравнивается с локальным результатом HMAC
        response = connection.recv(len(digest))
        return hmac.compare_digest(digest, response)

    def echo_handler(self,client_sock):
        """ Эхо-обработка.
            Проводит аутентификацию клиента и отсылает его же запрос обратно (эхо).
        """
        if not self.server_authenticate(client_sock, self.secret_key):
            client_sock.close()
            return
        while True:
            self.to_monitor.append(client_sock)  # передаем второй сокет (клиентский)

            self.users_sockets.append(client_sock)

            listen_accepted_user = threading.Thread(target=self.listen_socket,
                                                    args=(client_sock,))
            listen_accepted_user.start()
            # messages
            # messages
            # messages
            # listen_accepted_user.join() # blocking function. waiting ...
            print(self.users_sockets)
            # msg = client_sock.recv(8192)
            # if not msg:
            #     break
            # client_sock.sendall(msg)
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
                qwe = listened_sock.send('finished!!!'.encode(self.ENCODDING))
                print(f'прилетел quit {time.ctime()}')
                print(f'server send {qwe} байт  == "finished!!!"')

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

        print(f"Connected from: <<{address[0]}>>")
        self.echo_handler(user_socket)
        #
        # self.to_monitor.append(user_socket)  # передаем второй сокет (клиентский)
        #
        # self.users_sockets.append(user_socket)
        #
        # listen_accepted_user = threading.Thread(target=self.listen_socket,
        #                                         args=(user_socket,))
        # listen_accepted_user.start()
        # # messages
        # # messages
        # # messages
        # # listen_accepted_user.join() # blocking function. waiting ...
        # print(self.users_sockets)

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
