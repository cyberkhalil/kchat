from socket import *  # library for sockets
from threading import Thread  # import Thread class

chat_port = 1234  # the server used port

# TODO remove this
documentation = 'This is chatting program \n' \
                '       --help : to print this documentation again \n' \
                '       connect : to connect the chatting server \n' \
                '       exit : to exit and close chatting server connection \n' \
                '       reconnect : to reconnect the chatting server from other port'  # the documentation


# TODO make a reconnect method
class Client:
    client_socket = None

    """ Methods """

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
        print("Not implemented yet")

    """     
    TODO implement those methods :-
        * get help message from the server.
        * get connection with the server.
        * get reconnection with the server.
    """

    def send_msg(self, word):
        self.client_socket.sendall(("$" + word).encode())

    # TODO check if received a command or a message
    def receive_from_server(self):
        return self.client_socket.recv(1024).decode()

    def request_members(self):
        self.send_msg('#request_client_members')


# TODO check client every 5 min
# TODO accept the header if start in $ or # as planned
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

        client_socket.send(b'#request username')
        username = client_socket.recv(1024).decode()
        print(client_address + '> username: ' + username)

        client_info = [username, client_socket]
        self.clients_list.append(client_info)
        try:
            client_socket.send(('Server: Welcome ' + username + ', you can start chatting  ^_^').encode())

            while 1:
                msg = str(client_socket.recv(1024).decode())
                if msg == '':
                    continue
                elif msg.startswith('#'):
                    self.check_server_command()
                    print(client_address + '> exiting')
                    break
                else:
                    print(client_address + '> sending ' + msg)
                    self.send_to_all(msg)

        except:
            print(client_address + '> leaving')
            self.clients_list.remove(client_info)

    def run(self):
        server_socket = socket(AF_INET, SOCK_STREAM)  # using TCP

        # open & listen to chat port
        server_socket.bind(('', chat_port))
        server_socket.listen(1)

        print('The chat server is ready')

        while 1:
            client_socket, address = server_socket.accept()
            print(len(self.clients_list))
            Thread(group=None, target=self.do_when_receive_client, args=(client_socket, address)).start()

    def check_server_command(self):
        print('check_server_command')
