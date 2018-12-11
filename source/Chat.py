from socket import *  # library for sockets
from threading import Thread  # import Thread class

chat_port = 1234  # the server used port


class Client:
    client_socket = None

    def connect(self):
        try:
            # create client socket
            self.client_socket = socket(AF_INET, SOCK_STREAM)  # create socket for chatting
            self.client_socket.connect(('127.0.0.1', chat_port))  # connect with server for chatting
            return 1
        except ConnectionRefusedError:
            print("Connection refused")
            return 0

    # TODO implement sending exit message to the server and stop the stop socket
    def exiting(self):
        self.client_socket.send("#exit".encode())
        self.client_socket.close()

    """     
    TODO implement those methods :-
        * get help message from the server.
        * get connection with the server.
        * get reconnection with the server.
    """

    def send_msg(self, word):
        self.client_socket.sendall(word.encode())

    # TODO check if received a command or a message
    def receive_message_from_server(self):
        msg = str(self.client_socket.recv(1024).decode())

        if msg.startswith("$") & ("$" in msg[1:]):
            msg = list(msg[1:])
            index = msg.index("$")
            msg[index] = ":"
            msg = "".join(msg)
            return msg
        elif msg.startswith("#"):
            self.check_command(msg[:5])

    # TODO implement this method
    def check_command(self, msg):
        pass

    def request_members(self):
        self.send_msg('#request_client_members')


"""
    TODO :-
        * check client every 5 min
        * accept the header if start in $ or # as planned
        * comments on the code
"""


class Server:
    clients_list = []

    def send_to_all(self, msg):
        print('sending "' + msg + '" to ' + str(len(self.clients_list)) + ' clients')

        for client in self.clients_list:
            try:
                client_socket = client[1]
                client_socket.send(str(msg).encode())
                print('sent to ' + client[0])
            # TODO expect exception type
            except:
                print('Error in sending message to ' + client[0])
                continue

    def do_when_receive_client(self, client_socket, client_address):

        client_address = str(client_address)

        print(client_address + '> established new connection')

        client_socket.send(b'#user')
        username = client_socket.recv(1024).decode()
        print(client_address + '> username: ' + username)

        client_info = [username, client_socket]
        self.clients_list.append(client_info)
        try:
            client_socket.send(('$server$ Welcome ' + username + ', you can start chatting  ^_^').encode())

            while 1:
                msg = str(client_socket.recv(1024).decode())
                if msg == '':
                    print("bad")
                    continue
                elif msg.startswith('#'):
                    self.check_server_command(msg)
                    print(client_info[0] + '> exiting')
                    break
                else:
                    print(client_info[0] + '> sending ' + msg)
                    self.send_to_all("$" + client_info[0] + "$" + msg)

        except:
            print(client_info[0] + '> leaving for error')
        self.clients_list.remove(client_info)
        client_socket.close()

    def run(self):
        server_socket = socket(AF_INET, SOCK_STREAM)  # using TCP

        server_socket.bind(('', chat_port))  # open & listen to chat port
        server_socket.listen(1)

        print('The chat server is ready')

        while 1:
            client_socket, address = server_socket.accept()
            print(len(self.clients_list))
            Thread(group=None, target=self.do_when_receive_client, args=(client_socket, address)).start()

    def check_server_command(self, command):
        print('check_server_command')
