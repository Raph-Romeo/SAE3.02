import socket
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QHBoxLayout, QAbstractItemView, QHeaderView, QFileDialog
from PyQt5.QtGui import QCursor, QIcon
from PyQt5 import Qt
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import QtCore
from functools import partial


class TableListItem(QWidget):
    def __init__(self, parent, name, address):
        super().__init__()
        layout = QHBoxLayout()
        self.__parent = parent
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.__servername = QLabel(name)
        self.__address = QLabel(address)
        self.name = name
        self.address = address
        self.__connect = QPushButton()
        self.__connect.setIcon(QIcon('assets/img/connect.png'))
        self.__connect.setMaximumWidth(50)
        self.__connect.setStyleSheet('border-radius:5px;')
        self.__connect.clicked.connect(lambda: self.__parent.tableitemselect(connect_button=self))
        self.__delete = QPushButton()
        self.__delete.setIcon(QIcon('assets/img/trash.png'))
        self.__delete.setMaximumWidth(50)
        self.__delete.setStyleSheet('border-radius:5px;background:transparent')
        self.__delete.clicked.connect(lambda: self.__parent.delete_row(self))
        self.setStyleSheet("QLabel{padding:0;padding-left:10px;padding-right:10px;}QPushButton{margin-left:10px;}")
        self.setMinimumHeight(40)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        layout.addWidget(self.__connect)
        layout.addWidget(self.__servername)
        layout.addWidget(self.__address)
        layout.addWidget(self.__delete)


class FileHeader(QWidget):
    def __init__(self, parent, file_name):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.__parent = parent
        self.setLayout(layout)
        self.__file_name = QLabel('File : ' + file_name)
        self.__file_name.setProperty('FileName', True)
        self.__file_explorer_button = QPushButton(" Select CSV file")
        self.__file_explorer_button.setToolTip('Click to select CSV File')
        self.__file_explorer_button.setIcon(QIcon('assets/img/csv.png'))
        self.__file_explorer_button.setStyleSheet("""border-radius:2px;background:white;font-size:12px;font-family:verdana;color:#202225;padding:5px;margin:2px;margin-top:0px;padding-left:10px;padding-right:10px;""")
        self.__file_explorer_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.setAttribute(Qt.Qt.WA_StyledBackground, True)
        self.__file_explorer_button.clicked.connect(self.__parent.open_csv_file)
        self.__file_explorer_button.setFixedWidth(140)
        layout.addWidget(self.__file_name)
        layout.addWidget(self.__file_explorer_button)

    def setText(self, text:str) -> None:
        self.__file_name.setText(text)


class MainTab(QWidget):
    def __init__(self, window, file_name):
        super().__init__()
        self.__parent = window
        self.__grid = QGridLayout()
        self.setObjectName("body")
        self.__grid.setSpacing(0)
        top_bar = QLabel('SuperShell')
        top_bar.setFixedHeight(51)
        top_bar.setAlignment(Qt.Qt.AlignCenter)
        top_bar.setStyleSheet('background:rgb(54,57,63);text-align:center;border-bottom:1px solid rgb(35,36,40);color:rgb(255,255,255);font-size:12px;font-weight:bold;')
        self.setAttribute(Qt.Qt.WA_StyledBackground, True)
        self.__grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.__grid)
        self.__nameinput = QLineEdit()
        self.__nameinput.setPlaceholderText('SERVER NAME')
        self.__ipinput = QLineEdit()
        self.__ipinput.setPlaceholderText('ADDRESS')
        self.__portinput = QLineEdit()
        self.__portinput.setPlaceholderText('PORT')
        self.__addbutton = QPushButton()
        self.__addbutton.setIcon(QIcon('assets/img/add.png'))
        self.__addbutton.clicked.connect(self.__add_table_row)
        self.__addbutton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__addbutton.setToolTip('Confirm')
        self.__inputlabel = QLabel('Add server to list:')
        self.__filename = file_name
        self.__file_header = FileHeader(self, file_name)
        self.__table = self.__maketable()
        self.setStyleSheet("""
        QWidget#body{background:rgb(54,57,63)} 
        QHeaderView::section{background:rgb(54,57,63);border:0px solid;color:white;font-family:verdana;font-size:12px;font-weight:bold} 
        QTableWidget::item{border:0px;border-bottom:1px solid rgb(56,60,67);}
        QTableWidget::item:hover{background:rgb(74,77,83)}
        QTableWidget::item:selected{background:rgb(74,77,83)}
        QTableWidget{gridline-color:transparent;color:#FFF;font-family:Verdana;font-size:12px;border:0px transparent;background:rgb(32,34,37)} 
        QHeaderView::section{border-top:0px;border-left:0px;border-bottom: 1px solid rgb(43,45,50);padding-left:4px;padding-top:13px;padding-bottom:14px;}
        QTableCornerButton::section{border-top:0px solid #D8D8D8;border-left:0px solid #D8D8D8;border-bottom: 2px solid rgb(43,45,50);}
        QLineEdit{border:none;border-radius:2px;background:#202225;font-size:12px;padding:5px;font-family:verdana;color:#FFF;margin:2px;margin-top:0px;}
        QPushButton{border-radius:2px;background:#202225;font-size:12px;font-family:arial;color:#FFF;padding:5px;margin:2px;margin-top:0px;padding-left:10px;padding-right:10px;}
        QLabel{font-size:12px;padding-left:10px;padding-bottom:5px;padding-top:10px;color:#FFF;font-family:verdana;}
        QScrollBar:vertical{background-color: rgb(34,37,43);width: 15px;margin: 15px 3px 15px 3px;border: 1px transparent;border-radius: 4px;}
        QScrollBar::handle:vertical{background-color: #dadce0;min-height: 5px;border-radius: 4px;}
        QScrollBar::sub-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
        QScrollBar::add-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
        QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on{height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
        QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on{height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
        QLabel[FileName="true"]{font-family:verdana;font-size:12px;padding:10px;color:white}
        """)
        self.__grid.addWidget(top_bar, 0, 0, 1, 4)
        self.__grid.addWidget(self.__file_header, 1, 0, 1, 4)
        self.__grid.addWidget(self.__table, 2, 0, 1, 4)
        self.__grid.addWidget(self.__inputlabel, 3, 0, 1, 4)
        self.__grid.addWidget(self.__nameinput, 4, 0)
        self.__grid.addWidget(self.__ipinput, 4, 1)
        self.__grid.addWidget(self.__portinput, 4, 2)
        self.__grid.addWidget(self.__addbutton, 4, 3)

    def __maketable(self):
        tableWidget = QTableWidget()
        tableWidget.setRowCount(0)
        tableWidget.setColumnCount(1)
        try:
            with open(self.__filename, 'r') as file:
                lines = file.readlines()
                for i in range(len(lines)):
                    data = lines[i].replace('\n', '').split(',')
                    if self.line_is_valid(data):
                        row = tableWidget.rowCount()
                        tableWidget.setRowCount(row+1)
                        tableWidget.setCellWidget(row, 0, TableListItem(self, data[0], data[1]))
                    else:
                        pass
        except:
            with open(self.__filename, 'w') as file:
                file.write('')
        tableWidget.horizontalHeader().setStretchLastSection(True)
        tableWidget.verticalHeader().setVisible(False)
        tableWidget.horizontalHeader().setVisible(False)
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        tableWidget.doubleClicked.connect(self.tableitemselect)
        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tableWidget.resizeRowsToContents()
        return tableWidget

    def line_is_valid(self, elems) -> bool:
        if len(elems) == 2:
            if len(elems[0]) > 0 and len(elems[1].split(':')) == 2:
                if elems[1].split(':')[1].isdigit():
                    return True
        return False

    def open_csv_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open datafile', 'c:\\', "CSV or TXT files (*.txt *.csv)")
        if fname != '':
            self.__filename = fname
            try:
                self.__table.setRowCount(0)
                with open(self.__filename, 'r') as file:
                    lines = file.readlines()
                    for i in range(len(lines)):
                        data = lines[i].replace('\n', '').split(',')
                        if self.line_is_valid(data):
                            row = self.__table.rowCount()
                            self.__table.setRowCount(row + 1)
                            self.__table.setCellWidget(row, 0, TableListItem(self, data[0], data[1]))
                        else:
                            pass
            except:
                with open(self.__filename, 'w') as file:
                    file.write('')
            self.__file_header.setText('File : ' + fname)
            self.__table.resizeRowsToContents()

    def tableitemselect(self, item=None, connect_button=None):
        if item is not None:
            data = self.__table.cellWidget(item.row(), 0).address
            name = self.__table.cellWidget(item.row(), 0).name
        else:
            data = connect_button.address
            name = connect_button.name
        ip = data.split(':')[0]
        port = data.split(':')[1]
        if port.isdigit() and len(ip) > 0 and len(name) > 0:
            port = int(port)
            self.connection_Qthread(ip, port, name)
        else:
            self.__parent.error('Connection from is invalid')

    def delete_row(self, item):
        for row in range(self.__table.rowCount()):
            if item == self.__table.cellWidget(row, 0):
                self.__table.removeRow(row)
                try:
                    with open(self.__filename, 'r') as file:
                        lines = file.readlines()
                        lines.pop(row)
                        string = ''
                        for line in lines:
                            string += line
                    with open(self.__filename, "w") as file:
                        file.write(string)
                    break
                except:
                    self.__parent.error('File not found')

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
            self.__table.setCellWidget(row, 0, TableListItem(self, name, address))
            self.__table.resizeRowsToContents()
            try:
                with open(self.__filename, 'r') as file:
                    lines = file.readlines()
                    if len(lines) > 0:
                        last = lines[len(lines) - 1]
                        if last[len(last) - 1:len(last)] == '\n':
                            skip_to_next_line = False
                        else:
                            skip_to_next_line = True
                    else:
                        skip_to_next_line = False
                with open(self.__filename, 'a') as file:
                    if skip_to_next_line:
                        file.write('\n' + name + ',' + address)
                    else:
                        file.write(name + ',' + address)
            except:
                self.__parent.error('File not found')
        else:
            self.__parent.error('Form is invalid')

    def __display_message(self, message: str):
        self.__display_message_label = QLabel(message)
        self.__display_message_label.setStyleSheet('background:rgba(34,34,34,0.5);font-size:20px;font-family:verdana;color:white;')
        self.__display_message_label.setAlignment(Qt.Qt.AlignCenter)
        self.__grid.addWidget(self.__display_message_label, 0, 0, 4, 4)


    def __result(self, n):
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
