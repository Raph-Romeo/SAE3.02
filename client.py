import socket
import sys
import os
import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMenu, QDialog, QTabWidget, QVBoxLayout, QMessageBox, QDialogButtonBox
from PyQt5.QtGui import QIcon
from PyQt5 import Qt
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore


#________


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Client")
        self.resize(500, 300)
        self.setWindowIcon(QIcon("icon.png"))
        self.__tabwidget = QTabWidget()
        self.__tabwidget.addTab(MainTab(self), "Servers")
        vbox = QVBoxLayout()
        vbox.addWidget(self.__tabwidget)
        self.setLayout(vbox)
    
    def NewTab(self, name:str, connection):
        tab = ServerTab(connection)
        self.__tabwidget.addTab(tab, name)
        return tab


    def __actionQuitter(self):
        return QCoreApplication.exit(0)
    
    def alert(self, msg:str):
        self.__alert = QMessageBox.critical(
            self,
            'Error.',
            msg,
            buttons=QMessageBox.Retry | QMessageBox.No,
            defaultButton=QMessageBox.Retry,
        )

        if self.__alert == QMessageBox.Retry:
            print("Try again")
        elif self.__alert == QMessageBox.No:
            print("Cancel")

class MainTab(QMainWindow):
    def __init__(self, window):
        super().__init__()
        widget = QWidget()
        self.__parent = window
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.__connectbutton = QPushButton('Connect')
        self.__connectbutton.clicked.connect(self.__connect_to_serv)
        grid.addWidget(self.__connectbutton,0,0)
    
    def __connect_to_serv(self):
        ip = '127.0.0.1'
        port = 5500
        connect(ip,port,self.__parent)


class ServerTab(QMainWindow):
    def __init__(self, connection):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        self.__connection = connection
        widget.setLayout(grid)
        self.__cmdinput = QLineEdit('')
        self.__cmdinput.setPlaceholderText('Type command...')
        self.__cmdlabel = QLabel('Server > Connection with server was successful!\n')
        self.__cmdlabel.setWordWrap(True)
        self.__cmdbutton = QPushButton('Send')
        self.__cmdbutton.setFixedWidth(50)
        self.__cmdbutton.clicked.connect(self.__send_message)
        self.__cmdlabel.setStyleSheet("background-color:black;color:white;padding:5px;font-family:arial;font-size:12px;")
        self.__cmdlabel.setAlignment(Qt.Qt.AlignTop)
        grid.addWidget(self.__cmdlabel,0,0,1,2)
        grid.addWidget(self.__cmdinput,1,0)
        grid.addWidget(self.__cmdbutton,1,1)
        
    def __send_message(self):
        command = self.__cmdinput.text()
        if len(command) > 0:
            if command == 'clear':
                self.__cmdinput.setText('')
                self.__cmdlabel.setText('')
            else:
                self.__cmdinput.setText('')
                self.__cmdlabel.setText(self.__cmdlabel.text() + 'You > ' + command + '\n')
                self.__connection.send(('$' + command).encode())
    
    def response(self, data):
        self.__cmdlabel.setText(self.__cmdlabel.text() + 'Server > ' + data + '\n')


#________


def disconnect(id:str):
    sockets[id].close()


def listen(client, this_id:str):
    while True:
        if this_id in force_stopped_threads:
            sys.exit()
        try:
            data = client[0].recv(1024)
            if not data:
                pass
            else:
                clean = data.decode()
                print(data)
                client[1].response(clean)
        except:
            client[1].response('disconnected')
            client[0].close()
            sys.exit()


def connect(ip: str ,port: int, window):
    global sockets
    try:
        client_socket = socket.socket()
        client_socket.connect((ip,port)) # ERROR IS HERE. WE CANT CONNECT TO SERVER??
        if len(list(sockets)) > 0:
            id = str(int(list(sockets)[len(list(sockets)) - 1]) + 1)
        else:
            id = '0'
        tab = window.NewTab('Server ' + id, client_socket)
        t1 = threading.Thread(target=listen,args=[[client_socket, tab], id])
        t1.start()
        sockets[id] = [client_socket, tab]
    except:
        window.alert('Error while trying to connect to server! \nWould you like to try again? ')


def main():
    global window
    window.show()
    app.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sockets = {}
    force_stopped_threads = []
    main()
