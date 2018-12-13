from socket import *  # library for sockets
from threading import Thread  # import Thread class


class KChatProtocol:
    chat_port = 1234  # the server used port
    connect_command = "#conn"  # used in the first time to ensure from the connection.
    username_command = "#user"  # used to change the username of a client.
    users_list_command = "#ulst"  # used to request users names who connected to same server.
    help_command = "#help"  # used to show the manual help page for the kchat.
    exit_command = "#exit"  # used to close the connection and exit.
    help_docs = "Welcome to KChat protocol docs \n    The commands starts with '#' symbol " \
                "and the messages starts with '$' symbol \n         commands list :- \n     #conn : This " \
                "command is used to connect to the server.\n     #user : This command is used to set a new " \
                "username.\n     #ulst : This command is used to see the other users connected to the server.\n" \
                "     #help : This command is used to see this docs.\n     #exit : This command is used to exit" \
                "the connection from server.\n    " \
                "Messages starts with '$' symbol, To send a message to all just put $your_message .\n" \
                ""  # the help documents for the Kchat protocol.

    connect_command_b = connect_command.encode()  # the connect_command encoded
    username_command_b = username_command.encode()  # the username_command encoded
    users_list_command_b = users_list_command.encode()  # the users_list_command encoded
    help_command_b = help_command.encode()  # the help_command encoded
    exit_command_b = exit_command.encode()  # the exit_command encoded
    help_docs_b = help_docs.encode()  # the help_docs encoded


class Client:
    """Client class is an implementation for KChat protocol in the client side, using socket and TCP connection"""

    username = None  # the username of the client
    client_socket = None  # the socket we use to communicate with the server
    isAlive = False  # the state of the connection with the server

    def connect(self):
        try:
            # create client socket
            self.client_socket = socket(AF_INET, SOCK_STREAM)  # create socket for chatting
            self.client_socket.connect(('127.0.0.1', KChatProtocol.chat_port))  # connect with server for chatting
            self.client_socket.send(KChatProtocol.connect_command_b)
            self.isAlive = True
            return 1
        except ConnectionRefusedError:
            print("Connection refused")
            return 0

    # TODO implement sending exit message to the server and stop the stop socket
    def exit(self):
        if not self.isAlive:
            print("Socket isn't alive so you can't send exit message using exit()")
            return
        self.client_socket.send(KChatProtocol.exit_command_b)
        self.client_socket.close()
        self.isAlive = False

    """     
    TODO implement those methods :-
        * get help message from the server.
        * get connection with the server.
        * get reconnection with the server.
    """

    def send_msg(self, word):
        if not self.isAlive:
            print("Socket isn't alive so you can't send_msg(" + word + ")")
            return
        self.client_socket.sendall(("$" + word).encode())

    # TODO check if received a command or a message
    def receive_from_server(self):

        if not self.isAlive:
            print("Socket isn't alive so you can't receive_from_server()")
            return
        try:
            msg = self.client_socket.recv(1024).decode()
        except:
            print("Error in receiving from server")
            self.isAlive = False
            return

        if msg.startswith("$") & ("$" in msg[1:]):
            msg = list(msg[1:-1])
            index = msg.index("$")
            msg[index] = ":"
            msg = "".join(msg)
            return msg
        elif msg.startswith("#"):
            if msg == KChatProtocol.exit_command_b:
                self.exit()
            elif msg == KChatProtocol.username_command_b:
                self.send_username()

        return self.receive_from_server()

    def request_members(self):
        if not self.isAlive:
            print("Socket isn't alive so you can't request_members()")
            return
        self.client_socket.sendall(KChatProtocol.users_list_command_b)

    def send_username(self):
        if not self.isAlive:
            print("Socket isn't alive so you can't send_username()")
            return
        self.client_socket.sendall(KChatProtocol.username_command_b + self.username.encode())


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
                client_socket.send(str(msg + "\n").encode())
                print('sent to ' + client[0])
            # TODO expect exception type
            except:
                print('Error in sending message to ' + client[0])
                continue

    def do_when_receive_client(self, client_socket, client_address):

        client_address = str(client_address)  # the need for address is just as string

        # If didn't receive connect command from client then return and stop the thread
        client_msg = client_socket.recv(1024).decode().strip()
        while not client_msg == KChatProtocol.connect_command:
            print("Client " + client_address + " didn't send connect command")
            client_msg = client_socket.recv(1024).decode().strip()

        print(client_address + '> established new connection')

        client_socket.send(KChatProtocol.username_command_b + "\n".encode())  # request username
        client_msg = client_socket.recv(1024).decode().strip()
        while not client_msg.startswith("#user"):
            print("Client " + client_address + " didn't get username from " + client_address)
            client_msg = client_socket.recv(1024).decode().strip()

        username = client_msg[5:].strip()
        print(client_address + '> username: ' + client_msg)

        client_info = [username, client_socket]
        self.clients_list.append(client_info)
        try:
            client_socket.send(("$server$ Welcome " + username + ", you can start chatting  ^_^\n").encode())
            while 1:
                msg = client_socket.recv(1024).decode()
                if msg.startswith("#"):
                    msg = msg.strip()
                    if msg == KChatProtocol.exit_command:
                        break
                    elif msg == KChatProtocol.help_command:
                        client_socket.send(KChatProtocol.help_docs_b + "\n".encode())
                    elif msg.startswith(KChatProtocol.username_command):
                        username = msg[5:].strip()
                        print(client_address + '> changing his username to ' + username)
                        self.clients_list.remove(client_info)
                        client_info[0] = username
                        self.clients_list.append(client_info)
                    else:
                        print('not valid command "' + msg + '"')
                elif msg.startswith("$"):
                    # TODO accept messages for specified client
                    msg = msg[1:]
                    print(client_info[0] + "> sending " + msg)
                    self.send_to_all("$" + client_info[0] + "$ " + msg)
                else:
                    if msg == "":  # telnet sends a lot of these..
                        continue
                    else:
                        print('weird message from ' + username + ' "' + msg + '"')
        except:
            print(client_info[0] + "> has error")

        print(client_info[0] + "> exiting")
        self.clients_list.remove(client_info)
        client_socket.close()

    def run(self):
        server_socket = socket(AF_INET, SOCK_STREAM)  # using TCP

        server_socket.bind(('', KChatProtocol.chat_port))  # open & listen to chat port
        server_socket.listen(1)

        print("The chat server is ready")

        while 1:
            client_socket, address = server_socket.accept()
            Thread(group=None, target=self.do_when_receive_client, args=(client_socket, address)).start()
