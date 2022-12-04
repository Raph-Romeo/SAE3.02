import socket
from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMenu, QDialog, QTabWidget, QVBoxLayout, QMessageBox, QDialogButtonBox, QTableWidget, QTableView, QScrollArea, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QCursor
from PyQt5 import Qt
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import QtCore
from functools import partial


class MainTab(QMainWindow):
    def __init__(self, window, file_name):
        super().__init__()
        widget = QWidget()
        self.__parent = window
        self.setCentralWidget(widget)
        self.__grid = QGridLayout()
        self.__grid.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(self.__grid)
        self.__nameinput = QLineEdit()
        self.__nameinput.setPlaceholderText('SERVER NAME')
        self.__ipinput = QLineEdit()
        self.__ipinput.setPlaceholderText('ADDRESS')
        self.__portinput = QLineEdit()
        self.__portinput.setPlaceholderText('PORT')
        self.__addbutton = QPushButton('+')
        self.__addbutton.clicked.connect(self.__add_table_row)
        self.__addbutton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__addbutton.setToolTip('Confirm')
        self.__inputlabel = QLabel('Add server to list')
        self.__filename = file_name
        self.__table = self.__maketable()
        self.setStyleSheet("""
        QMainWindow{background:rgb(43,45,50)} 
        QHeaderView::section{background:rgb(43,45,50);border:0px solid;padding:5px;color:white;font-family:verdana;font-size:12px;font-weight:bold} 
        QTableWidget::item{border:0px;padding: 5px;border-bottom:1px solid rgb(66,70,77);margin:1px;} 
        QTableWidget{gridline-color:transparent;color:#FFF;font-family:Verdana;font-size:12px;border:0px transparent;background:rgb(54,57,63)} 
        QTableWidget::item:hover{background: rgb(66,70,77);color: #FFF;font-weight:999;border-radius:5px;} 
        QTableWidget::item:selected {background: rgb(66,70,77);color: #FFF;font-weight:999;border-radius:5px;} 
        QHeaderView::section{border-top:0px;border-left:0px;border-bottom: 2px solid rgb(43,45,50);padding:4px;}
        QTableCornerButton::section{border-top:0px solid #D8D8D8;border-left:0px solid #D8D8D8;border-bottom: 2px solid rgb(43,45,50);}
        QLineEdit{border:none;border-radius:5px;background:#202225;font-size:12px;padding:5px;font-family:verdana;color:#FFF;margin:3px;margin-top:0px}
        QPushButton{border-radius:5px;background:#202225;font-size:12px;font-family:arial;color:#FFF;padding:5px;margin:3px;margin-top:0px;padding-left:10px;padding-right:10px;}
        QLabel{font-size:12px;padding-left:20px;padding-bottom:5px;padding-top:10px;color:#FFF;font-weight:bold;font-family:verdana;border-top:2px solid rgb(43,45,50);}
        QScrollBar:vertical{background-color: rgb(34,37,43);width: 15px;margin: 15px 3px 15px 3px;border: 1px transparent;border-radius: 4px;}
        QScrollBar::handle:vertical{background-color: #dadce0;min-height: 5px;border-radius: 4px;}
        QScrollBar::sub-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
        QScrollBar::add-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
        QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on{height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
        QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on{height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
        """)
        self.__grid.addWidget(self.__table, 0, 0, 1, 4)
        self.__grid.addWidget(self.__inputlabel, 1, 0, 1, 4)
        self.__grid.addWidget(self.__nameinput, 2, 0)
        self.__grid.addWidget(self.__ipinput, 2, 1)
        self.__grid.addWidget(self.__portinput, 2, 2)
        self.__grid.addWidget(self.__addbutton, 2, 3)

    def __maketable(self):
        tableWidget = QTableWidget()
        tableWidget.setRowCount(0)
        tableWidget.setColumnCount(2)
        try:
            with open(self.__filename, 'r') as file:
                lines = file.readlines()
                for i in range(len(lines)):
                    data = lines[i].replace('\n', '').split(',')
                    if self.line_is_valid(data):
                        row = tableWidget.rowCount()
                        tableWidget.setRowCount(row+1)
                        tableWidget.setItem(row, 0, QTableWidgetItem(data[0]))
                        tableWidget.setItem(row, 1, QTableWidgetItem(data[1]))
                    else:
                        pass
        except:
            with open(self.__filename, 'w') as file:
                file.write('')
        tableWidget.horizontalHeader().setStretchLastSection(True)
        tableWidget.verticalHeader().setVisible(False)
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        tableWidget.doubleClicked.connect(self.__tableitemselect)
        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tableWidget.setHorizontalHeaderLabels(['Server name', 'Server address'])
        tableWidget.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        return tableWidget

    def line_is_valid(self, elems) -> bool:
        if len(elems) == 2:
            if len(elems[0]) > 0 and len(elems[1].split(':')) == 2:
                if elems[1].split(':')[1].isdigit():
                    return True
        return False

    def __tableitemselect(self, item):
        ip = self.__table.item(item.row(), 1).text().split(':')[0]
        port = self.__table.item(item.row(), 1).text().split(':')[1]
        name = self.__table.item(item.row(), 0).text()
        if port.isdigit() and len(ip) > 0 and len(name) > 0:
            port = int(port)
            self.connection_Qthread(ip, port, name)
        else:
            self.__parent.error('Connection details are invalid!')

    def __add_table_row(self):
        ip = self.__ipinput.text()
        port = self.__portinput.text()
        name = self.__nameinput.text()
        if port.isdigit() and len(ip) > 0 and len(name) > 0:
            self.__ipinput.setText('')
            self.__portinput.setText('')
            self.__nameinput.setText('')
            address = ip + ':' + port
            row = self.__table.rowCount()
            self.__table.setRowCount(self.__table.rowCount() + 1)
            self.__table.setItem(row, 0, QTableWidgetItem(name))
            self.__table.setItem(row, 1, QTableWidgetItem(address))
            with open(self.__filename, 'a') as file:
                file.write(name + ',' + address + '\n')
        else:
            self.__parent.error('Form is invalid!')

    def __display_message(self, message: str):
        self.__display_message_label = QLabel(message)
        self.__display_message_label.setStyleSheet('background:rgba(34,34,34,0.5);font-size:20px;font-family:verdana;color:white;')
        self.__display_message_label.setAlignment(Qt.Qt.AlignCenter)
        self.__grid.addWidget(self.__display_message_label, 0, 0, 2, 4)


    def __result(self, n):
        global sockets
        state = n[0]
        data = n[1]
        if state:
            connection = data[0]
            name = data[1]
            self.__parent.NewTab(name, connection)
        else:
            ip = data[0]
            port = data[1]
            name = data[2]
            self.__parent.alert(ip, port, name)

    def connection_Qthread(self, ip, port, tabname=None):
        self.__display_message('Attempting to connect to ' + str(ip) + ':' + str(port) + '...')
        self.thread = QThread()
        self.worker = Attemptconnection()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(partial(self.worker.run, ip, port, tabname))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.__result)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.__display_message_label.deleteLater)
        self.thread.start()

class Attemptconnection(QObject):
    finished = pyqtSignal(list)

    def success(self, data):
        self.finished.emit([True, data])

    def error(self, data):
        self.finished.emit([False, data])

    def run(self, ip, port, name):
        try:
            connection = socket.socket()
            connection.connect((ip, port))
            connection.setblocking(False)
            self.success([connection, name])
        except:
            self.error([ip, port, name])
