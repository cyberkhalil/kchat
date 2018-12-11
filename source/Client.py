"""
    TODO :-
        * send message to specified client
        * press enter = click on send message button
        * implement methods in Client class using GUI
"""

########################################################################################################################
import sys
from threading import Thread

from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel

from Chat import Client

client = Client()


def request_username():
    username, ok_pressed = QtWidgets.QInputDialog.getText(QtWidgets.QInputDialog(), 'Connection',
                                                          'Enter your username:')
    if ok_pressed:
        if username != 'None':
            return username
        else:
            return 'Guest'
    else:
        return request_username()


def show_help():
    show_information_msg('Help',
                         'This is KChat application , You can use it to chat with any client when there is a chat '
                         'server')


def show_about():
    show_information_msg('About', 'KChat is a chatting program , you can use it to chat with any other one using the '
                                  'same program if there is a chat server both of you.')


def show_information_msg(title, information):
    QtWidgets.QMessageBox().information(QtWidgets.QWidget(), title, information)


def show_error(title, error_msg):
    QtWidgets.QMessageBox().critical(QtWidgets.QWidget(), title, error_msg)


def exit_clicked():
    sys.exit()


def window():
    def connect():
        print("Connecting")
        if client.connect():
            username = str(request_username())
            print(username)
            client.send_msg(username)
            msg_txt_edt.setEnabled(1)
            send_msg_btn.setEnabled(1)
            Thread(target=keep_receiving_from_server, args=[]).start()
        else:
            print("Connection failed")
            show_error("Connection failed", "Please check the server and try to connect again")

    def send_msg():
        print('sending message')
        client.send_msg(msg_txt_edt.text())
        msg_txt_edt.setText('')

    def keep_receiving_from_server():
        while 1:
            receive_from_server()

    def receive_from_server():
        msg = client.receive_message_from_server()
        print('msg received')
        messages_txt_edt.append(msg)

    app = QtWidgets.QApplication([])

    # Window properties
    w = QtWidgets.QWidget()
    w.setGeometry(100, 100, 500, 400)
    w.setFixedSize(500, 400)
    w.setWindowTitle('KChat')

    # Menu properties
    menu_bar = QtWidgets.QMenuBar(w)

    # Connection Menu
    connection_menu = menu_bar.addMenu('Connection')
    connect_action = connection_menu.addAction('Connect')
    connect_action.triggered.connect(connect)
    exit_action = connection_menu.addAction('Exit')
    exit_action.triggered.connect(exit_clicked)

    # Help Action
    help_action = menu_bar.addAction('Help')
    help_action.triggered.connect(show_help)

    # About Action
    about_action = menu_bar.addAction('About')
    about_action.triggered.connect(show_about)

    # Button properties
    send_msg_btn = QtWidgets.QPushButton(w)
    send_msg_btn.setText('Send')
    send_msg_btn.setFixedSize(100, 40)
    send_msg_btn.move(400, 360)
    send_msg_btn.clicked.connect(send_msg)
    send_msg_btn.setEnabled(0)

    # Edit Text properties
    msg_txt_edt = QtWidgets.QLineEdit(w)
    msg_txt_edt.move(0, 360)
    msg_txt_edt.setFixedSize(400, 40)
    msg_txt_edt.setEnabled(0)

    # messages text edit
    messages_txt_edt = QtWidgets.QTextEdit(w)
    messages_txt_edt.move(0, 30)
    messages_txt_edt.setFixedSize(400, 330)
    messages_txt_edt.setEnabled(0)

    # members label
    members_lbl = QtWidgets.QLabel(w)
    members_lbl.move(410, 30)
    members_lbl.setFixedSize(90, 20)
    members_lbl.setText('Members List')

    # members list view
    members_lst_view = QtWidgets.QListView(w)
    members_lst_view.move(400, 50)
    members_lst_view.setFixedSize(100, 300)

    members_model = QStandardItemModel(members_lst_view)
    # members_model.appendRow(QStandardItem('1'))
    members_lst_view.setModel(members_model)

    # To show the Window
    w.show()
    sys.exit(app.exec_())


window()
