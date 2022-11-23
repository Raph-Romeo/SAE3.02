from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMenu, QDialog, QTabWidget, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import Qt
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore


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
        return self.__tabwidget.addTab(ServerTab(connection), name)


    def __actionQuitter(self):
        return QCoreApplication.exit(0)
    
    def alert(self, msg:str):
        self.__alert = QDialog()
        self.__alert.setText(msg)
        self.__alert.show()


class MainTab(QMainWindow):
    def __init__(self, window):
        super().__init__()
        widget = QWidget()
        self.__parent = window
        self.setCentralWidget(widget)
        self.__connect = connect
        grid = QGridLayout()
        widget.setLayout(grid)
        self.__connectbutton = QPushButton('Connect')
        self.__connectbutton.clicked.connect(self.__connect_to_serv)
        grid.addWidget(self.__connectbutton,0,0)
    
    def __connect_to_serv(self):
        self.__connect('127.0.0.1',5500,self.__parent)


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
        self.__cmdlabel.setStyleSheet("background-color:black;color:white;padding:5px;border-radius:5px;font-family:arial;font-size:12px;")
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
                #self.__connection.send(('$' + command).encode())
    
    def response(self, data):
        self.__cmdlabel.setText(self.__cmdlabel.text() + 'Server > ' + data + '\n')