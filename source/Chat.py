from socket import *  # library for sockets
from threading import Thread  # import Thread class


class ChatProtocol:
    chat_port = 1234  # the server used port
    connect_command = "#conn"
    username_command = "#user"
    users_list_command = "#ulst"
    help_command = "help"
    exit_command = "#exit"
    connect_command_b = connect_command.encode()
    username_command_b = username_command.encode()
    users_list_command_b = users_list_command.encode()
    help_command_b = help_command.encode()
    exit_command_b = exit_command.encode()


class Client:
    username = None
    client_socket = None
    isAlive = False

    def connect(self):
        try:
            # create client socket
            self.client_socket = socket(AF_INET, SOCK_STREAM)  # create socket for chatting
            self.client_socket.connect(('127.0.0.1', ChatProtocol.chat_port))  # connect with server for chatting
            self.client_socket.send(ChatProtocol.connect_command_b)
            self.isAlive = True
            return 1
        except ConnectionRefusedError:
            print("Connection refused")
            return 0

    # TODO implement sending exit message to the server and stop the stop socket
    def exit(self):
        self.client_socket.send(ChatProtocol.exit_command_b)
        self.client_socket.close()
        self.isAlive = False

    """     
    TODO implement those methods :-
        * get help message from the server.
        * get connection with the server.
        * get reconnection with the server.
    """

    def send_msg(self, word):
        self.client_socket.sendall(word.encode())

    # TODO check if received a command or a message
    def receive_from_server(self):
        msg = str(self.client_socket.recv(1024).decode())

        if msg.startswith("$") & ("$" in msg[1:]):
            msg = list(msg[1:])
            index = msg.index("$")
            msg[index] = ":"
            msg = "".join(msg)
            return msg
        elif msg.startswith("#"):
            if msg == ChatProtocol.exit_command_b:
                self.exit()
            elif msg == ChatProtocol.username_command_b:
                self.send_username()

        return self.receive_from_server()

    def request_members(self):
        self.send_msg('#request_client_members')

    def send_username(self):
        self.client_socket.sendall(ChatProtocol.username_command_b + self.username.encode())


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

        client_address = str(client_address)  # the need for address is just as string

        # If didn't receive connect command from client then return and stop the thread
        if not client_socket.recv(1024) == ChatProtocol.connect_command_b:
            print("Client " + client_address + " didn't send connect command")
            return

        print(client_address + '> established new connection')

        client_socket.send(ChatProtocol.username_command_b)  # request username
        username = str(client_socket.recv(1024).decode())
        if not username.startswith("#user"):
            print("Client " + client_address + " didn't get username from " + client_address)
            return
        username = username[5:].strip()
        print(client_address + '> username: ' + username)

        client_info = [username, client_socket]
        self.clients_list.append(client_info)
        try:
            client_socket.send(("$server$ Welcome " + username + ", you can start chatting  ^_^").encode())
            while 1:
                msg = client_socket.recv(1024).decode()
                if msg == "":
                    break

                elif msg.startswith("#"):
                    if msg == "#exit":
                        break
                    else:
                        print("not valid command :" + msg)
                else:
                    print(client_info[0] + "> sending " + msg)
                    self.send_to_all("$" + client_info[0] + "$ " + msg)
        except:
            print(client_info[0] + "> has error")

        print(client_info[0] + "> exiting")
        self.clients_list.remove(client_info)
        client_socket.close()

    def run(self):
        server_socket = socket(AF_INET, SOCK_STREAM)  # using TCP

        server_socket.bind(('', ChatProtocol.chat_port))  # open & listen to chat port
        server_socket.listen(1)

        print("The chat server is ready")

        while 1:
            client_socket, address = server_socket.accept()
            Thread(group=None, target=self.do_when_receive_client, args=(client_socket, address)).start()
