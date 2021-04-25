# import socket
from Socket import SocketCLass
import threading

# tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
class Server(SocketCLass):
    def __init__(self):
        super(Server, self).__init__()
        self.users_sockets = []


    def set_up(self):
        self.bind(("", self.PORT))
        self.listen(5)
        print('server is listening....')
        self.accept_sockets()

# tcpSerSock.bind(("", 1111))
# tcpSerSock.listen(5)

# users_sockets = []
# BUFF = 2048
# ENCODDING = 'utf-8'
# print('server is listening....')


    def send_data(self, data):
        for user_socket in self.users_sockets:
            user_socket.send(data)


    def listen_socket(self, listened_sock=None):
        print('listening user')
        while True:
            data = listened_sock.recv(self.BUFF)
            print(f'User sent {data.decode(self.ENCODDING)}')
            self.send_data(data)


    def accept_sockets(self):
        while True:
            print('Waiting for client...')
            # user_socket, address = tcpSerSock.accept()  # blocking function
            user_socket, address = self.accept()  # blocking function
            print(f'Connected from: <<{address[0]}>>')
            # users_sockets.append(user_socket)
            self.users_sockets.append(user_socket)
            # listen_accepted_user = threading.Thread(target=listen_user,
            listen_accepted_user = threading.Thread(target=self.listen_socket,
                                                    args=(user_socket,))
            listen_accepted_user.start()
            #messages
            #messages
            #messages
            # listen_accepted_user.join() # blocking function. waiting ...


if __name__ == '__main__':
    server = Server()
    server.set_up()
    # start_server()
