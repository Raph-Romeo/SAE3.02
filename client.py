import socket
import sys
import os
import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMenu, QDialog, QTabWidget, QVBoxLayout, QMessageBox, QDialogButtonBox, QTableWidget, QTableView, QScrollArea, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QIcon, QCursor
from PyQt5 import Qt
from PyQt5.QtCore import QCoreApplication, QObject, QThread, pyqtSignal
from PyQt5 import QtCore
from functools import partial

#________

class ScrollLabel(QScrollArea):
 
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)
        layout = QVBoxLayout(content)
        self.label = QLabel(content)
        self.label.setStyleSheet("color:white;font-family:verdana;font-size:12px;border-bottom:none;")
        self.setStyleSheet(stylesheet)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.Qt.AlignTop)
        #self.label.setTextInteractionFlags()
        layout.addWidget(self.label)

    def setText(self, text):
        self.label.setText(text)

    def text(self):
        get_text = self.label.text()
        return get_text

stylesheet = """
    QScrollArea{border:none;border-bottom:1px solid #dadce0;}
    
    QScrollBar:vertical{background-color: #2A2949;width: 15px;margin: 15px 3px 15px 3px;border: 1px transparent #2A2929;border-radius: 4px;}
    QScrollBar::handle:vertical{background-color: #dadce0;min-height: 5px;border-radius: 4px;}
    QScrollBar::sub-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on{height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on{height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
    
    QScrollBar:horizontal{background-color: #2A2949;width: 15px;margin: 15px 3px 15px 3px;border: 1px transparent #2A2929;border-radius: 4px;}
    QScrollBar::handle:horizontal{background-color: #dadce0;min-height: 5px;border-radius: 4px;}
    QScrollBar::sub-line:horizontal{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:horizontal{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::sub-line:horizontal:hover,QScrollBar::sub-line:horizontal:on{height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on{height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal{background: none;opacity: 0%;height: 0px;width:0px;}
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal{background: none;opacity: 0%;height: 0px;width:0px;}
"""



class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Client")
        self.resize(720,500)
        self.setWindowIcon(QIcon("icon.png"))
        self.__tabwidget = QTabWidget()
        self.__tabwidget.setStyleSheet("""QTabWidget::pane {border:0px;border-top: 1px solid lightgray;top:-1px;background: rgb(245, 245, 245);; } 
QTabBar::tab {background: rgb(230, 230, 230); border: 1px solid lightgray; padding: 15px;} 
QTabBar::tab:selected { background: rgb(245, 245, 245);}""")
        self.__main = MainTab(self)
        self.__tabwidget.addTab(self.__main, "Servers")
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.__tabwidget)
        self.setLayout(vbox)
    
    def NewTab(self, name:str, connection):
        tab = ServerTab(connection, self, name)
        self.__tabwidget.addTab(tab, name)
        self.__tabwidget.setCurrentIndex(self.__tabwidget.count() - 1)
        return tab
    
    
    def renameTab(self, name:str):
        self.__tabwidget.setTabText(self.__tabwidget.currentIndex(),name)


    def __actionQuitter(self):
        return QCoreApplication.exit(0)


    def alert(self, msg:str,ip,port,name):
        self.__alert = QMessageBox.critical(
            self,
            'Error.',
            msg,
            buttons=QMessageBox.Retry | QMessageBox.No,
            defaultButton=QMessageBox.Retry,
        )
        if self.__alert == QMessageBox.Retry:
            self.__main.connection_Qthread(ip, port, name)
        else:
            pass


    def closeEvent(self, event):
        global force_stopped_threads
        for i in sockets:
            force_stopped_threads.append(i)
        event.accept()


class Attemptconnection(QObject):
    finished = pyqtSignal(list)
    
    def success(self,data):
        self.finished.emit([True,data])
    
    def error(self,data):
        self.finished.emit([False,data])

    def run(self,ip, port, tabname):
        connect(ip, port, self, tabname)


class MainTab(QMainWindow):
    def __init__(self, window):
        super().__init__()
        widget = QWidget()
        self.__parent = window
        self.setCentralWidget(widget)
        self.__grid = QGridLayout()
        self.__grid.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(self.__grid)
        self.__nameinput = QLineEdit()
        self.__nameinput.setPlaceholderText('Server name')
        self.__ipinput = QLineEdit()
        self.__ipinput.setPlaceholderText('IP')
        self.__portinput = QLineEdit()
        self.__portinput.setPlaceholderText('PORT')
        self.__addbutton = QPushButton('+')
        self.__addbutton.clicked.connect(self.__add_table_row)
        self.__addbutton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__addbutton.setToolTip('Confirm')
        self.__inputlabel = QLabel('Add server to list')
        self.__table = self.__ip_list()
        self.setStyleSheet("""
        QMainWindow{background:rgb(43,45,50)} 
        QHeaderView::section{background:rgb(43,45,50);border:0px solid;padding:5px;color:white;font-family:verdana;font-size:12px;font-weight:bold} 
        QTableWidget::item{border:0px;padding: 5px;border-bottom:1px solid rgb(66,70,77);margin:1px;} 
        QTableWidget{gridline-color:transparent;color:#FFF;font-family:Verdana;font-size:12px;border:0px transparent;background:rgb(54,57,63)} 
        QTableWidget::item:hover{background: rgb(66,70,77);color: #FFF;font-weight:999;border-radius:5px;} 
        QTableWidget::item:selected {background: rgb(66,70,77);color: #FFF;font-weight:999;border-radius:5px;} 
        QHeaderView::section{border-top:0px;border-left:0px;border-bottom: 2px solid rgb(43,45,50);padding:4px;}
        QTableCornerButton::section{border-top:0px solid #D8D8D8;border-left:0px solid #D8D8D8;border-bottom: 2px solid rgb(43,45,50);}
        QLineEdit{border:none;border-radius:5px;background:#202225;font-size:12px;padding:5px;font-family:arial;color:#FFF;margin:3px;margin-top:0px}
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
        self.__table.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__grid.addWidget(self.__table,0,0,1,4)
        self.__grid.addWidget(self.__inputlabel,1,0,1,4)
        self.__grid.addWidget(self.__nameinput,2,0)
        self.__grid.addWidget(self.__ipinput,2,1)
        self.__grid.addWidget(self.__portinput,2,2)
        self.__grid.addWidget(self.__addbutton,2,3)
    
    
    def __ip_list(self):
        tableWidget = QTableWidget();
        tableWidget.setColumnCount(2)
        try:
            with open('iplist.txt','r') as file:
                lines = file.readlines()
                tableWidget.setRowCount(len(lines))
                for i in range(len(lines)):
                    data = lines[i].replace('\n','').split(',')
                    tableWidget.setItem(i, 0, QTableWidgetItem(data[0]))
                    tableWidget.setItem(i, 1, QTableWidgetItem(data[1]))
        except:
            with open('iplist.txt','w') as file:
                file.write('')
            tableWidget.setRowCount(0)
        tableWidget.horizontalHeader().setStretchLastSection(True)
        tableWidget.verticalHeader().setVisible(False)
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        tableWidget.setFocusPolicy(QtCore.Qt.NoFocus) 
        tableWidget.doubleClicked.connect(self.__tableitemselect)
        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tableWidget.setHorizontalHeaderLabels(['Server name','Server address'])
        return tableWidget
    
    
    def __display_message(self, message:str):
        self.__display_message_label = QLabel(message)
        self.__display_message_label.setStyleSheet('background:rgba(34,34,34,0.5);font-size:20px;font-family:verdana;color:white;')
        self.__display_message_label.setAlignment(Qt.Qt.AlignCenter)
        self.__grid.addWidget(self.__display_message_label,0,0,2,4)
    
    
    def __tableitemselect(self,item):
        ip = self.__table.item(item.row(),1).text().split(':')[0]
        port = self.__table.item(item.row(),1).text().split(':')[1]
        try:
            port = int(port)
        except:
            print('not a number!')
        else:
            name = self.__table.item(item.row(),0).text()
            if name == '':
                name = None
            self.connection_Qthread(ip,port,name)
    
    
    def __add_table_row(self):
        ip = self.__ipinput.text()
        port = self.__portinput.text()
        name = self.__nameinput.text()
        try:
            int(port)
        except:
            print('not a number!')
        else:
            self.__ipinput.setText('')
            self.__portinput.setText('')
            self.__nameinput.setText('')
            address = ip + ':' + port
            row = self.__table.rowCount()
            self.__table.setRowCount(self.__table.rowCount() + 1)
            self.__table.setItem(row, 0, QTableWidgetItem(name))
            self.__table.setItem(row, 1, QTableWidgetItem(address))
            with open('iplist.txt','a') as file:
                file.write('\n' + name + ',' + address)

    
    def __result(self,n):
        global sockets
        state = n[0]
        data = n[1]
        if state:
            socket = data[0]
            connection_id = data[1]
            connection_name = data[2]
            if connection_name is None:
                tab = self.__parent.NewTab('Server ' + connection_id, socket)
            else:
                tab = self.__parent.NewTab(connection_name, socket)
            t1 = threading.Thread(target=listen,args=[[socket, tab], connection_id])
            t1.start()
            sockets[connection_id] = [socket, tab]
        else:
            ip = data[0]
            port = data[1]
            name = data[2]
            self.__parent.alert('Error while trying to connect to server!\nWould you like to try again? ',ip,port,name)
    
    
    def connection_Qthread(self, ip, port, tabname=None):
        self.__display_message('Attempting to connect to ' + str(ip) + ':' + str(port) + '...')
        self.thread = QThread()
        self.worker = Attemptconnection()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(partial(self.worker.run,ip, port, tabname))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.__result)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.__display_message_label.deleteLater)
        self.thread.start()


class ServerTab(QMainWindow):
    def __init__(self, connection, parent, servername):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        self.__connection = connection
        self.setStyleSheet('background-color:#19002c;color:white;padding:0;margin:0')
        widget.setLayout(grid)
        self.__parent = parent
        self.__auth = False
        self.__servername = servername
        self.__cmdinput = QLineEdit('')
        self.__cmdinput.setPlaceholderText('Type password . . .')
        self.__cmdinput.setStyleSheet('border:none;margin:5px;margin-top:0px')
        self.__cmdinput.editingFinished.connect(self.__send_message)
        self.__cmdinput.setEchoMode(QLineEdit.Password)
        titlelabel = QLabel('Connection: ' + str(self.__connection.getpeername()[0]) + ':' + str(self.__connection.getpeername()[1]))
        titlelabel.setStyleSheet('color:white;margin-left:5px;font-size:12px;font-family:verdana;')
        self.__exitbutton = QPushButton('𐌢')
        self.__exitbutton.setStyleSheet('QPushButton{background-color:transparent;padding:5px;border-radius:0px;color:#FFF;font-weight:100;font-family:arial;text-align:center;font-size:16px;}QPushButton:hover{background-color:#F02020;}QToolTip { background-color: black; color: white; border: black solid 1px}')
        self.__exitbutton.clicked.connect(self.__exit)
        self.__exitbutton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__exitbutton.setToolTip('Disconnect from server')
        self.__cmdlabel = ScrollLabel()
        self.__cmdbutton = QPushButton('→')
        self.__cmdbutton.setFixedWidth(50)
        self.__cmdbutton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__cmdbutton.setToolTip('Confirm')
        self.__cmdbutton.setStyleSheet('QPushButton{border-radius:10px;margin:5px;margin-top:0;background-color:transparent;padding:5px;color:#FFF;font-weight:100;text-align:center;font-size:16px}QPushButton:hover{background-color:#FFF;color:black}QToolTip { background-color: black; color: white; border: black solid 1px}')
        self.__cmdbutton.clicked.connect(self.__send_message)
        grid.addWidget(titlelabel,0,0,1,2)
        grid.addWidget(self.__exitbutton,0,1)
        grid.addWidget(self.__cmdlabel,1,0,1,2)
        grid.addWidget(self.__cmdinput,2,0)
        grid.addWidget(self.__cmdbutton,2,1)
    
    
    def authenticated(self):
        self.__auth = True
        self.__cmdinput.setPlaceholderText('Type command . . .')
        self.__cmdinput.setEchoMode(QLineEdit.Normal)
        self.__cmdlabel.setText('Established connection with ' + str(self.__connection.getpeername()[0]) + ':' + str(self.__connection.getpeername()[1]) + '\n')
    
    
    def __scroll_to_bottom(self):
        verScrollBar = self.__cmdlabel.verticalScrollBar()
        verScrollBar.setValue(verScrollBar.maximum())
    
    
    def __send_message(self):
        command = self.__cmdinput.text()
        if len(command) > 0:
            if self.__auth and (command.lower() == 'clear' or command.lower() == 'cls'):
                self.__cmdinput.setText('')
                self.__cmdlabel.setText('')
            elif self.__auth and command.lower().split(' ')[0] == 'rename':
                self.__cmdlabel.setText(self.__cmdlabel.text() + self.__servername + ' > ' + command + '\n')
                self.__servername = command.split(' ', 1)[1]
                self.__parent.renameTab(self.__servername)
                self.__cmdlabel.setText(self.__cmdlabel.text() + f'Changed name to {self.__servername}\n')
                self.__cmdinput.setText('')
            else:
                try:
                    self.__cmdinput.setText('')
                    if self.__auth:
                        self.__cmdlabel.setText(self.__cmdlabel.text() + self.__servername + ' > ' + command + '\n')
                        self.__connection.send(('$' + command).encode())
                    else:
                        self.__connection.send(command.encode())
                except:
                    self.__cmdlabel.setText(self.__cmdlabel.text() + 'Conection was lost. \n')
            self.__scroll_to_bottom()
    
    
    def response(self, data):
        self.__cmdlabel.setText(self.__cmdlabel.text() + data + '\n')
        self.__cmdlabel.verticalScrollBar().setValue(self.__cmdlabel.verticalScrollBar().maximum())
        self.__scroll_to_bottom()
    
    
    def closeTab(self):
        self.deleteLater()
    
    
    def __exit(self):
        self.__connection.close()
        self.deleteLater()


#________


def disconnect(id:str):
    sockets[id].close()


def listen(client, connection_id:str):
    global force_stopped_threads
    auth = False
    while True:
        if connection_id in force_stopped_threads:
            client[1].closeTab()
            client[0].close()
            sys.exit()
        try:
            data = client[0].recv(1024)
            if not data:
                pass
            else:
                cleaned = data.decode()
                client[1].response(cleaned)
                if not auth and cleaned == 'OK':
                    auth = True
                    client[1].authenticated()
                if cleaned == 'closing socket':
                    force_stopped_threads.append(connection_id)
        except:
            pass


def connect(ip: str ,port: int, worker, name=None):
    try:
        client_socket = socket.socket()
        client_socket.connect((ip,port))
        client_socket.setblocking(0)
        if len(list(sockets)) > 0:
            connection_id = str(int(list(sockets)[len(list(sockets)) - 1]) + 1)
        else:
            connection_id = '0'
        worker.success([client_socket,connection_id,name])
    except:
        worker.error([ip,port,name])


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
