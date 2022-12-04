from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMenu, QDialog, QTabWidget, QVBoxLayout, QMessageBox, QDialogButtonBox, QTableWidget, QTableView, QScrollArea, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QCursor
from PyQt5 import Qt
import socket
import time
import threading
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer


class ScrollLabel(QScrollArea):

    def __init__(self, parent, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)
        self.parent = parent
        layout = QGridLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel('')
        layout.setRowStretch(2, 1)
        self.setStyleSheet("""
    QScrollArea{border:none;background:#000}
    QScrollBar:vertical{background-color: rgb(12,12,12);width: 15px;margin: 15px 3px 15px 3px;border: 1px transparent #2A2929;border-radius: 4px;}
    QScrollBar::handle:vertical{background-color: #333;min-height: 5px;border-radius: 4px;}
    QScrollBar::sub-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on{height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on{height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
    QScrollBar:horizontal{background-color:rgb(43,45,50);width:15px;margin: 15px 3px 15px 3px;border: 1px transparent #2A2929;border-radius: 4px;}
    QScrollBar::handle:horizontal{background-color: #dadce0;min-height: 5px;border-radius: 4px;}
    QScrollBar::sub-line:horizontal{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:horizontal{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::sub-line:horizontal:hover,QScrollBar::sub-line:horizontal:on{height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on{height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal{background: none;opacity: 0%;height: 0px;width:0px;}
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal{background: none;opacity: 0%;height: 0px;width:0px;}
    QLabel{color:white;font-family:verdana;font-size:12px;border-bottom:none;background-color:transparent;padding:10px;padding-top:0px;padding-bottom:0px;}
    QLineEdit{border:none;margin-top:0px;background:#000;font-family:Verdana;color:white;font-size:12px;padding-bottom:10px;}
""")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.Qt.AlignTop)
        self.cmdinput = QLineEdit('')
        self.username = QLabel(self.parent.servername + ' >')
        self.username.setStyleSheet("color:white;font-family:verdana;font-size:12px;border-bottom:none;background-color:transparent;padding-left:10px;padding-bottom:10px;padding-right:0px;")
        self.cmdinput.setPlaceholderText('Type password . . .')
        self.cmdinput.returnPressed.connect(self.parent.send_message)
        self.cmdinput.setAlignment(Qt.Qt.AlignTop)
        self.cmdinput.setEchoMode(QLineEdit.Password)
        self.verticalScrollBar().rangeChanged.connect(self.__scroll_to_bottom)
        layout.addWidget(self.label, 0, 0, 1, 2)
        layout.addWidget(self.username, 1, 0)
        layout.addWidget(self.cmdinput, 1, 1)

    def __scroll_to_bottom(self):
        verScrollBar = self.verticalScrollBar()
        verScrollBar.setValue(verScrollBar.maximum())

    def focusinput(self):
        self.cmdinput.setFocusPolicy(Qt.Qt.StrongFocus)
        self.cmdinput.setFocus()

    def setText(self, text):
        self.label.setText(text)

    def addText(self, text):
        if self.label.text() != "":
            self.label.setText(self.text() + '\n' + text)
        else:
            self.label.setText(text)
            self.label.setHidden(False)

    def text(self):
        get_text = self.label.text()
        return get_text


class ServerTab(QMainWindow):
    def __init__(self, connection, parent, servername):
        super().__init__()
        widget = QWidget()
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(grid)
        self.setStyleSheet("""
        *{background:rgb(0,0,0);color:white;padding:0;margin:0}
        QPushButton{background-color:transparent;padding:5px;border-radius:0px;color:#727272;font-weight:100;font-family:arial;text-align:center;font-size:16px}
        QPushButton:hover{background-color:#F02020;color:#FFF}
        QPushButton[hidetab="true"]:hover{background-color:#505050}
        QToolTip{background-color: black; color: white; border: black solid 1px}
        QLabel{color:white;margin-left:5px;font-size:12px;font-family:verdana}
        QLabel[toplabel="true"]{color:#727272;font-size:9px;padding-left:10px;text-decoration:underline}
        """)
        self.__stop = False
        self.setCentralWidget(widget)
        self.__connection = connection
        self.__parent = parent
        self.__auth = False
        self.servername = servername
        titlelabel = QLabel(f'Connection: {self.__connection.getpeername()[0]}:{self.__connection.getpeername()[1]}')
        titlelabel.setProperty("toplabel", True)
        self.__hidetabbutton = QPushButton('🡡')
        self.__hidetabbutton.setFixedWidth(50)
        self.__hidetabbutton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__hidetabbutton.setToolTip('hide tab bar')
        self.__hidetabbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.__hidetabbutton.setProperty("hidetab", True)
        self.__hidetabbutton.clicked.connect(self.__hideTab)
        self.__exitbutton = QPushButton('𐌢')
        self.__exitbutton.setFixedWidth(50)
        self.__exitbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.__exitbutton.clicked.connect(self.__exit)
        self.__exitbutton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__exitbutton.setToolTip('disconnect')
        self.cmdline = ScrollLabel(parent=self)
        self.__thread = threading.Thread(target=self.__listen)
        self.__thread.start()
        grid.addWidget(titlelabel, 0, 0, 1, 3)
        grid.addWidget(self.__hidetabbutton, 0, 1)
        grid.addWidget(self.__exitbutton, 0, 2)
        grid.addWidget(self.cmdline, 1, 0, 1, 3)
        self.cmdline.focusinput()

    def __hideTab(self):
        if self.__parent.hideTab():
            self.__parent.hideTab(True)
            self.__hidetabbutton.setText('🡡')
            self.__hidetabbutton.setToolTip('hide tab bar')
        else:
            self.__hidetabbutton.setText('🡣')
            self.__hidetabbutton.setToolTip('show tab bar')
            self.__parent.hideTab(False)

    def authenticated(self, state: bool = True):
        if state:
            self.__auth = True
            self.cmdline.cmdinput.setPlaceholderText('Type command . . .')
            self.cmdline.cmdinput.setEchoMode(QLineEdit.Normal)
            self.clear()
            self.cmdline.addText('Established connection with ' + str(self.__connection.getpeername()[0]) + ':' + str(
                self.__connection.getpeername()[1]))
        else:
            self.__auth = False
            self.cmdline.cmdinput.setPlaceholderText('Type password . . .')
            self.cmdline.cmdinput.setEchoMode(QLineEdit.Password)

    def force_stop(self):
        try:
            self.__connection.send('exit'.encode())
        except:
            pass
        self.__connection.close()
        self.__stop = True
        self.closeTab()

    def send_message(self):
        command = self.cmdline.cmdinput.text()
        if len(command) > 0:
            if self.__auth and (command.lower() == 'clear' or command.lower() == 'cls'):
                self.cmdline.cmdinput.setText('')
                self.clear()
            elif self.__auth and command.lower().split(' ')[0] == 'rename':
                self.cmdline.addText(self.servername + ' > ' + command)
                self.servername = command.split(' ', 1)[1]
                self.__parent.renameTab(self.servername)
                self.cmdline.username.setText(self.servername + ' >')
                self.cmdline.addText(f'Changed name to {self.servername}')
                self.cmdline.cmdinput.setText('')
            else:
                try:
                    self.cmdline.cmdinput.setText('')
                    self.__connection.send((command).encode())
                    if self.__auth:
                        self.cmdline.addText(self.servername + ' >  ' + command)
                except:
                    self.cmdline.addText('Conection was lost.')

    def response(self, data):
        self.cmdline.addText(data)

    def clear(self):
        self.cmdline.setText('')
        self.cmdline.label.setHidden(True)

    def closeTab(self):
        self.__parent.connections_remove(self)
        if self.__parent.number_of_connections() == 0:
            self.__parent.hideTab(False)
        self.deleteLater()

    def __exit(self):
        try:
            self.__connection.send('exit'.encode())
        except:
            self.__connection.close()
            self.closeTab()

    def attempt_reconnect(self, address):
        for i in range(0, 5):
            client_socket = socket.socket()
            time.sleep(1)
            try:
                client_socket.connect((address[0], address[1]))
                client_socket.setblocking(False)
                client_socket.send('<testing_connection>'.encode())
                return client_socket
            except:
                pass
        return None

    def __listen(self):
        while not self.__stop:
            try:
                data = self.__connection.recv(2048)
                if not data:
                    pass
                else:
                    cleaned = data.decode()
                    self.response(cleaned)
                    if not self.__auth and cleaned == 'OK':
                        self.authenticated(True)
                    if cleaned == 'closing socket':
                        self.__stop = True
                        self.closeTab()
                    elif cleaned == 'resetting':
                        address = self.__connection.getpeername()
                        self.__connection.close()
                        self.authenticated(False)
                        self.clear()
                        self.response('reconnecting...')
                        self.__connection = self.attempt_reconnect(address)
                        if self.__connection is None:
                            self.closeTab()
            except:
                pass
