import json
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
    "time": time.time(),
}


# =====================================
# =====================server====
class Server(SocketClass):
    def __init__(self):
        super(Server, self).__init__()

        self.HOST = ""
        self.users_sockets = []
        self.to_monitor = []

    def b_decode_str_foo(self, b_request_recvd):  # from b'' (json) to str
        return b_request_recvd.decode(self.ENCODDING)

    def str_loads_dict_foo(self, request_str):  # from str to  dict
        return json.loads(request_str)

    def py_dumps_str_foo(self, param_server):  # from py (dict) to str
        return json.dumps(param_server)

    # ================prepare=====================
    def set_up(self):
        self.to_monitor.append(self)
        self.bind((self.HOST, self.PORT))
        self.listen(5)
        print('server is listening....')
        self.main_loop()

    def send_data(self, data):
        for user_socket in self.users_sockets:
            user_socket.send(data)

    def listen_socket(self, listened_sock=None):
        """Принимает сообщения от клиента (слушает)
        затем отправка сообщений send_message()"""
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

            elif 'action' in request_dict and request_dict['action'] != 'authenticate':
                for var_response in LIST_AUTH:
                    if 'response' in var_response and var_response['response'] == '402':
                        msg = str(var_response['error'])
                        listened_sock.send(msg.encode(self.ENCODDING))
                print('ошибка auth')

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
