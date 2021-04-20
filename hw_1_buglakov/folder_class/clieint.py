import json
from Sockett import SocketClass
import time
from threading import Thread
#
# BUFF = 2048
# ENCODDING = 'utf-8'
# HOST = "localhost"
# PORT = 1111
# запросы клиента:
quit = {
    'action': 'quit'
}
AUTH_CLIENT = {
    'action': 'authenticate',
    # 'action': 'dfgdfg',
    'time': time.ctime(),
    'user': {
        'account_name': 'C0deMaver1ck',
        'password': 'CorrectHorseBatterStaple'
    }
}
PRESENTS_MSG = {  # сообщение о присутствии — presence
    'action': 'presence',
    'time': time.ctime(),
    'type': 'status',
    'user': {
        'account_name': 'C0deMaver1ck',
        'status': 'Yep, I am here!'
    }
}

class Client(SocketClass):
    def __init__(self):
        super(Client, self).__init__()

    def set_up(self):
        self.connect((self.HOST, self.PORT))  # установка связи с сервером

        listen_thread = Thread(target=self.listen_socket)
        listen_thread.start()

        send_data_thread = Thread(target=self.send_data, args=(None,))
        send_data_thread.start()

# client_sock = socket.socket(socket.AF_INET,
#                             socket.SOCK_STREAM)



    def py_dumps_str_foo(self,param_user):
        return json.dumps(param_user)


    def listen_socket(self,listened_sock=None):
        while True:
            data = self.recv(self.BUFF)
            if not data:
                break
            data = data.decode(self.ENCODDING)

            print(data)



    def send_data(self, data):
        while True:
            time.sleep(2)
            self.send(self.py_dumps_str_foo(AUTH_CLIENT).encode(self.ENCODDING))
            break

        # listen_server()


if __name__ == '__main__':
   client=Client()
   client.set_up()
