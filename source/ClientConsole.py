# TODO client who sent the message

########################################################################################################################
import sys
from threading import Thread

from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel

from Chat import Client

print('type --help to see the documentation')  # printing helping tip

client = Client()


def request_username():
    username, ok_pressed = QtWidgets.QInputDialog.getText(QtWidgets.QWidget(), 'Connection', 'Enter your username:')
    if ok_pressed:
        if username != 'None':
            return username
        else:
            return 'Guest'
    else:
        username = request_username()


def show_help():
    QtWidgets.QMessageBox().information(QtWidgets.QWidget(), 'Help', 'This is KChat application , You can user it '
                                                                     'to chat with any client when there is a chat '
                                                                     'server')


def show_about():
    QtWidgets.QMessageBox().information(QtWidgets.QWidget(), 'About', 'About')


def window():
    def connect():
        print('Connect')
        client.connect()
        username = str(request_username())
        print(username)
        client.check_and_send(username)
        msg_txt_edt.setEnabled(1)
        send_msg_btn.setEnabled(1)
        Thread(target=keep_receiving_from_server, args=[]).start()

    def send_msg():
        print('sending message')
        client.check_and_send(msg_txt_edt.text())
        msg_txt_edt.setText('')

    def keep_receiving_from_server():
        while 1:
            receive_from_server()

    def receive_from_server():
        msg = client.receive_from_server()
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
    exit_action.triggered.connect(app.exit)

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
