from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QComboBox, QMenu, QDialog, QTabWidget, QVBoxLayout, QMessageBox, QDialogButtonBox, QTableWidget, QTableView, QScrollArea, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QCursor, QIcon
from PyQt5 import Qt
import socket
import time
import threading
import pyqtgraph as pg
from PyQt5 import QtCore


class Graph(QWidget):
    def __init__(self, name):
        super().__init__()
        self.setAttribute(Qt.Qt.WA_StyledBackground, True)
        self.setStyleSheet('background:#202225')
        self.graphWidget = pg.PlotWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        self.__type = name
        self.__display = QLabel(self.__type + ': --%')
        self.__display.setStyleSheet('color:white;font-family:verdana;background:#202225')
        self.__display.setAlignment(Qt.Qt.AlignCenter)
        layout.addWidget(self.__display)
        layout.addWidget(self.graphWidget)
        self.x = []
        self.y = []
        self.graphWidget.setBackground('#202225')
        pen = pg.mkPen(color=(255, 255, 255))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)

    def update_plot_data(self, data):
        self.__display.setText(self.__type + ': ' + str(data) + '%')
        if len(self.x) >= 25:
            self.x = self.x[1:]
        if len(self.x) == 0:
            self.x = [0]
        else:
            self.x.append(self.x[-1] + 1)
        if len(self.y) >= 25:
            self.y = self.y[1:]
        self.y.append(data)
        self.data_line.setData(self.x, self.y)

    def clear_plot(self):
        self.__display.setText(self.__type + ': --%')
        self.x = []
        self.y = []
        self.data_line.setData(self.x, self.y)



class ScrollLabel(QScrollArea):

    def __init__(self, parent, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)
        self.parent = parent
        layout = QGridLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setRowStretch(3, 2)
        layout.setSpacing(0)
        self.setStyleSheet("""
    *{background:rgb(32,34,37)}
    QScrollArea{border:none;border-top:1px solid rgb(43,45,50);}
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
    QLabel{color:white;font-family:Consolas;font-size:15px;border:none;background-color:transparent;padding:0px;padding-left:10px;padding-right:10px;padding-top:0px;}
    QLineEdit{border:none;margin:0px;padding:0px;font-family:Consolas;color:white;font-size:15px;padding-bottom:10px;padding-top:0px;}
""")
        self.label = QLabel('')
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.Qt.AlignTop)
        self.blankspace = QWidget()
        self.blankspace.setFixedHeight(10)
        self.username = QLabel(self.parent.servername + ' >')
        self.username.setStyleSheet("color:white;font-family:Consolas;font-size:15px;border-bottom:none;background-color:transparent;padding-left:10px;padding-bottom:10px;padding-right:0px;")
        self.cmdinput = QLineEdit('')
        self.cmdinput.setPlaceholderText('Type password ...')
        self.cmdinput.returnPressed.connect(self.parent.handle_input)
        self.cmdinput.setAlignment(Qt.Qt.AlignTop)
        self.cmdinput.setEchoMode(QLineEdit.Password)
        self.cmdinput.textChanged.connect(self.__highlight)
        self.cmdinput.isActiveWindow()
        self.cmdinput.setFocus()
        self.cmdinput.setFocusPolicy(Qt.Qt.StrongFocus)
        self.index = 0
        self.history = []
        self.verticalScrollBar().rangeChanged.connect(self.__scroll_to_bottom)
        layout.addWidget(self.blankspace, 0, 0, 1, 2)
        layout.addWidget(self.label, 1, 0, 1, 2)
        layout.addWidget(self.username, 2, 0)
        layout.addWidget(self.cmdinput, 2, 1)

    def __highlight(self):
        if self.parent.isAuthenticated():
            if self.cmdinput.text().lower().split(' ')[0].split(':')[0] in [
                'help', 'dos', 'powershell', 'linux', 'os', 'ram', 'cpu', 'name', 'ip', 'ping', 'logs',
                'exec', 'clear', 'kill', 'disconnect', 'reset', 'leave', 'quit', 'exit', 'cls', 'rename'
            ]:
                self.cmdinput.setStyleSheet('color:white')
            else:
                self.cmdinput.setStyleSheet('color:#999')
        else:
            self.cmdinput.setStyleSheet('color:white')

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Qt.Key_Up:
            if len(self.history) > self.index:
                self.index += 1
                self.cmdinput.setText(self.history[len(self.history) - self.index])
        elif event.key() == Qt.Qt.Key_Down:
            if self.index > 1:
                self.index -= 1
                self.cmdinput.setText(self.history[len(self.history) - self.index])
        '''else:
            if not self.cmdinput.hasFocus():
                if event.key() == Qt.Qt.Key_Backspace:
                    self.cmdinput.setText(self.cmdinput.text()[0:len(self.cmdinput.text())-1])
                elif event.key() == Qt.Qt.Key_Return:
                    self.parent.handle_input()
                elif event.text() in """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^"',.<>?:{};`~+=_-%^&*() /\\[]|""":
                    self.cmdinput.setText(self.cmdinput.text() + event.text())'''

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

    def clearinput(self):
        self.index = 0
        self.cmdinput.setText('')


class ServerTab(QMainWindow):
    def __init__(self, connection, parent, servername):
        super().__init__()
        widget = QWidget()
        grid = QGridLayout()
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(grid)
        self.setStyleSheet("""
        *{background:rgb(54,57,63);color:white;padding:0;margin:0}
        QPushButton{background-color:transparent;padding:5px;border:none;color:#727272;font-weight:100;font-family:arial;text-align:center;font-size:20px;font-weight:bold;}
        QPushButton[exit="true"]:hover{background-color:#F02020;color:#FFF}
        QPushButton[graph="true"]{background:rgb(66,70,77);color:rgb(195,195,195);border-radius:10%;margin:5px;font-size:12px;}
        QPushButton[graph="true"]:hover{color:white}
        QPushButton[active="true"]{background:rgb(66,252,77);color:rgb(54,57,63)}
        QToolTip{background-color: black; color: white; border: black solid 1px;padding:2px;border-radius:5%;}
        QLabel{color:white;margin-left:5px;font-size:15px;font-family:Consolas}
        QLabel[toplabel="true"]{color:rgb(249,249,249);font-size:12px;font-family:verdana;padding-left:10px;}
        """)
        self.__stop = False
        self.setCentralWidget(widget)
        self.__connection = connection
        self.__parent = parent
        self.__auth = False
        self.servername = servername
        self.__titlelabel = QLabel(servername)
        self.__titlelabel.setToolTip(self.__connection.getpeername()[0] + ':' + str(self.__connection.getpeername()[1]))
        self.__titlelabel.setProperty("toplabel", True)

        self.__ramgraphsub = False
        self.__ramgraph = Graph('RAM')
        self.__ramgraph.setHidden(True)
        self.__ramgraphbutton = QPushButton('RAM')
        self.__ramgraphbutton.setIcon(QIcon('assets/graph.png'))
        self.__ramgraphbutton.setFixedWidth(70)
        self.__ramgraphbutton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__ramgraphbutton.setToolTip('Toggle RAM graph')
        self.__ramgraphbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.__ramgraphbutton.setProperty("graph", True)
        self.__ramgraphbutton.setDisabled(True)
        self.__ramgraphbutton.clicked.connect(self.__subscribe_ram)

        self.__cpugraphsub = False
        self.__cpugraph = Graph('CPU')
        self.__cpugraph.setHidden(True)
        self.__cpugraphbutton = QPushButton('CPU')
        self.__cpugraphbutton.setIcon(QIcon('assets/graph.png'))
        self.__cpugraphbutton.setFixedWidth(70)
        self.__cpugraphbutton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__cpugraphbutton.setToolTip('Toggle CPU graph')
        self.__cpugraphbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.__cpugraphbutton.setProperty("graph", True)
        self.__cpugraphbutton.setDisabled(True)
        self.__cpugraphbutton.clicked.connect(self.__subscribe_cpu)

        custom_layout = QHBoxLayout()
        custom_layout.addWidget(self.__ramgraph)
        custom_layout.addWidget(self.__cpugraph)
        custom_layout.setContentsMargins(0, 0, 0, 0)
        custom_layout.setSpacing(0)
        self.__graph_hold = QWidget()
        self.__graph_hold.setLayout(custom_layout)
        self.__graph_hold.setHidden(True)

        self.__exitbutton = QPushButton()
        self.__exitbutton.setFixedWidth(50)
        self.__exitbutton.setProperty("exit", True)
        self.__exitbutton.setFixedHeight(50)
        self.__exitbutton.setIcon(QIcon('assets/close_bright.png'))
        self.__exitbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.__exitbutton.clicked.connect(self.exit)
        self.__exitbutton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__exitbutton.setToolTip('disconnect')
        self.cmdline = ScrollLabel(parent=self)
        self.__thread = threading.Thread(target=self.__listen)
        self.__thread.start()
        grid.addWidget(self.__titlelabel, 0, 0, 1, 4)
        grid.addWidget(self.__ramgraphbutton, 0, 1)
        grid.addWidget(self.__cpugraphbutton, 0, 2)
        grid.addWidget(self.__exitbutton, 0, 3)
        grid.addWidget(self.cmdline, 1, 0, 1, 4)
        grid.addWidget(self.__graph_hold, 2, 0, 1, 4)
        self.cmdline.focusinput()

    def authenticated(self, state: bool = True):
        if state:
            self.__auth = True
            self.cmdline.cmdinput.setPlaceholderText('Type command ...')
            self.cmdline.cmdinput.setEchoMode(QLineEdit.Normal)
            self.clear()
            self.__cpugraphbutton.setDisabled(False)
            self.__ramgraphbutton.setDisabled(False)
            self.cmdline.addText('Established connection with ' + str(self.__connection.getpeername()[0]) + ':' + str(self.__connection.getpeername()[1]))
        else:
            self.__auth = False
            self.__cpugraphbutton.setDisabled(True)
            self.__ramgraphbutton.setDisabled(True)
            self.cmdline.cmdinput.setPlaceholderText('Type password ...')
            self.cmdline.cmdinput.setEchoMode(QLineEdit.Password)

    def force_stop(self):
        try:
            self.__connection.send('exit'.encode())
        except:
            pass
        self.__connection.close()
        self.__stop = True
        self.closeTab()

    def handle_input(self, command=None):
        if command is None:
            command = self.cmdline.cmdinput.text()
        if len(command) > 0:
            self.cmdline.clearinput()
            if not self.__auth:
                self.send(command)
            else:
                self.cmdline.addText(self.servername + ' > ' + command)
                if len(self.cmdline.history) == 0 or self.cmdline.history[len(self.cmdline.history) - 1] != command:
                    self.cmdline.history.append(command)
                if (command.lower() == 'clear' or command.lower() == 'cls'):
                    self.clear()
                elif command.lower().split(' ')[0] == 'rename':
                    if len(command.split(' ')) > 1:
                        self.servername = command.split(' ', 1)[1]
                        self.__titlelabel.setText(self.servername)
                        self.__parent.renameTab(self.servername)
                        self.cmdline.username.setText(self.servername + ' >')
                        self.cmdline.addText(f'Changed name to {self.servername}')
                    else:
                        self.cmdline.addText('Usage: RENAME <NAME>')
                else:
                    self.send(command)

    def address(self):
        return str(self.__connection.getpeername()[0]) + ':' + str(self.__connection.getpeername()[1])

    def send(self, msg):
        try:
            self.__connection.send(msg.encode())
        except:
            self.cmdline.addText('Conection was lost.')

    def __subscribe_cpu(self):
        if self.__cpugraphsub:
            self.__connection.send('<sub_cpu_false>'.encode())
            self.__cpugraphsub = False
            self.__cpugraph.clear_plot()
            self.__cpugraph.setHidden(True)
            if not self.__ramgraphsub:
                self.__graph_hold.setHidden(True)
        else:
            self.__connection.send('<sub_cpu_true>'.encode())
            self.__cpugraphsub = True
            self.__cpugraph.setHidden(False)
            self.__graph_hold.setHidden(False)

    def __subscribe_ram(self):
        if self.__ramgraphsub:
            self.__connection.send('<sub_ram_false>'.encode())
            self.__ramgraphsub = False
            self.__ramgraph.clear_plot()
            self.__ramgraph.setHidden(True)
            if not self.__cpugraphsub:
                self.__graph_hold.setHidden(True)
        else:
            self.__connection.send('<sub_ram_true>'.encode())
            self.__ramgraphsub = True
            self.__ramgraph.setHidden(False)
            self.__graph_hold.setHidden(False)

    def response(self, data):
        if not self.__auth and data == 'OK':
            return self.authenticated(True)
        if data == 'closing socket':
            self.__stop = True
            self.closeTab()
        elif data == 'resetting':
            address = self.__connection.getpeername()
            self.__connection.close()
            self.clear()
            self.cmdline.addText('trying to reconnect ...')
            self.__connection = self.attempt_reconnect(address)
            if self.__connection is None:
                self.closeTab()
            else:
                self.authenticated(False)
                if self.__cpugraphsub:
                    self.__cpugraphsub = False
                    self.__cpugraph.setHidden(True)
                    self.__cpugraph.clear_plot()
                if self.__ramgraph:
                    self.__ramgraphsub = False
                    self.__ramgraph.setHidden(True)
                    self.__ramgraph.clear_plot()
        else:
            self.cmdline.addText(data)

    def clear(self):
        self.cmdline.setText('')
        self.cmdline.label.setHidden(True)

    def closeTab(self):
        self.__parent.connections_remove(self)
        self.deleteLater()

    def multi_exit(self):
        try:
            self.__connection.send('exit'.encode())
        except:
            try:
                self.__connection.close()
            except:
                pass
        self.__stop = True
        self.deleteLater()

    def exit(self):
        try:
            self.__connection.send('exit'.encode())
        except:
            try:
                self.__connection.close()
            except:
                pass
        self.__stop = True
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

    def __is_graph_data(self, data) -> bool:
        if data[0:5] == '<CPU|':
            cpu_percent = float(data.split('|')[1])
            self.__cpugraph.update_plot_data(cpu_percent)
            return True
        elif data[0:5] == '<RAM|':
            ram_percent = float(data.split('|')[1])
            self.__ramgraph.update_plot_data(ram_percent)
            return True
        return False

    def __listen(self):
        while not self.__stop:
            try:
                data = self.__connection.recv(2048)
                if not data:
                    pass
                else:
                    cleaned = data.decode()
                    if not self.__is_graph_data(cleaned):
                        self.response(cleaned)
            except:
                pass

    def isAuthenticated(self) -> bool:
        return self.__auth
