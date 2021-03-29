import json
import socket


class SocketClass(socket.socket):
    def __init__(self):
        super(SocketClass, self).__init__(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

        self.BUFF = 2048
        self.ENCODDING = 'utf-8'
        self.PORT = 10000
        self.HOST = 'localhost'

    def send_data(self, data):
        """Если в класее наследнике не переопределится метод ,
         то выбросится исключение"""
        raise NotImplementedError()

    def listen_socket(self, listened_sock=None):
        raise NotImplementedError()

    def set_up(self):
        raise NotImplementedError()

