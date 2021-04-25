# import socket
from threading import Thread
from Socket import SocketCLass


class Client(SocketCLass):
    def __init__(self):
        super(Client, self).__init__()

    def set_up(self):
        self.connect((self.LOCAL, self.PORT))
        # где подключаемся там и создаем потоки
        listen_Thread = Thread(target=self.listen_socket)
        listen_Thread.start()

        send_Thread = Thread(target=self.send_data, args=(None,))
        send_Thread.start()

    # BUFF = 2048
    # ENCODDING = 'utf-8'

    # client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # client_sock.connect(('localhost', 1111))  # установка связи с сервером

    def listen_socket(self, listened_sock=None):
        while True:
            # В клиенте слушает только сервер, потому только self
            data = self.recv(self.BUFF)
            print(data.decode(self.ENCODDING))


    def send_data(self, data):
        while True:
            self.send(input(':::').encode(self.ENCODDING))


if __name__ == '__main__':
    client = Client()
    client.set_up()
    # send_to_server()
