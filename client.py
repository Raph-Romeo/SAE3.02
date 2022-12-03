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
import time
from functools import partial

#________

class ScrollLabel(QScrollArea):
 
    def __init__(self,parent,*args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)
        self.parent = parent
        layout = QGridLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel('')
        layout.setRowStretch(2, 1)
        self.label.setStyleSheet("color:white;font-family:verdana;font-size:12px;border-bottom:none;background-color:transparent;padding:10px;padding-top:0px;padding-bottom:0px;")
        self.setStyleSheet(stylesheet)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.Qt.AlignTop)
        #self.label.setTextInteractionFlags()
        self.cmdinput = QLineEdit('')
        self.username = QLabel(self.parent.servername + ' >')
        self.username.setStyleSheet("color:white;font-family:verdana;font-size:12px;border-bottom:none;background-color:transparent;padding-left:10px;padding-bottom:10px;")
        self.cmdinput.setPlaceholderText('Type password . . .')
        self.cmdinput.setStyleSheet('border:none;margin-top:0px;background:#000;font-family:Verdana;color:white;font-size:12px;padding-bottom:10px;')
        self.cmdinput.editingFinished.connect(self.parent.send_message)
        self.cmdinput.setAlignment(Qt.Qt.AlignTop)
        self.cmdinput.setEchoMode(QLineEdit.Password)
        self.verticalScrollBar().rangeChanged.connect(self.__scroll_to_bottom)
        layout.addWidget(self.label,0,0,1,2)
        layout.addWidget(self.username,1,0)
        layout.addWidget(self.cmdinput,1,1)
    
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

stylesheet = """
    QScrollArea{border:none;background:#000}
    
    QScrollBar:vertical{background-color: rgb(43,45,50);width: 15px;margin: 15px 3px 15px 3px;border: 1px transparent #2A2929;border-radius: 4px;}
    QScrollBar::handle:vertical{background-color: #dadce0;min-height: 5px;border-radius: 4px;}
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
"""



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Client")
        self.resize(720,500)
        self.setWindowIcon(QIcon("icon.png"))
        self.__tabwidget = QTabWidget()
        self.__tabwidget.setStyleSheet("""QTabWidget::pane {border:0px;background: rgb(245, 245, 245);; } 
QTabBar::tab {background: rgb(36,38,41);border:none;padding:15px;color:#AAA;}
QTabBar::tab:hover {background:rgb(43,45,50);color:white;}
QTabBar::tab:selected {background:rgb(43,45,50);color:white;}""")
        self.__main = MainTab(self)
        self.setStyleSheet('QMainWindow{background:rgb(31,33,36)}')
        self.__tabwidget.addTab(self.__main, "Home")
        vbox = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.__tabwidget)
    
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
        self.setStyleSheet('background:rgb(0,0,0);color:white;padding:0;margin:0')
        widget.setLayout(grid)
        self.__parent = parent
        self.__auth = False
        self.servername = servername
        titlelabel = QLabel('Connection: ' + str(self.__connection.getpeername()[0]) + ':' + str(self.__connection.getpeername()[1]))
        titlelabel.setStyleSheet('color:white;margin-left:5px;font-size:12px;font-family:verdana;font-weight:bold')
        self.__exitbutton = QPushButton('𐌢')
        self.__exitbutton.setFixedWidth(50)
        self.__exitbutton.setStyleSheet('QPushButton{background-color:transparent;padding:5px;border-radius:0px;color:#FFF;font-weight:100;font-family:arial;text-align:center;font-size:16px;}QPushButton:hover{background-color:#F02020;}QToolTip { background-color: black; color: white; border: black solid 1px}')
        self.__exitbutton.clicked.connect(self.__exit)
        self.__exitbutton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__exitbutton.setToolTip('Disconnect from server')
        self.cmdline = ScrollLabel(parent=self)
        grid.addWidget(titlelabel,0,0,1,2)
        grid.addWidget(self.__exitbutton,0,1)
        grid.addWidget(self.cmdline,1,0,1,2)
        self.cmdline.focusinput()
    
    
    def authenticated(self,state:bool=True):
        if state:
            self.__auth = True
            self.cmdline.cmdinput.setPlaceholderText('Type command . . .')
            self.cmdline.cmdinput.setEchoMode(QLineEdit.Normal)
            self.clear()
            self.cmdline.addText('Established connection with ' + str(self.__connection.getpeername()[0]) + ':' + str(self.__connection.getpeername()[1]))
        else:
            self.__auth = False
            self.cmdline.cmdinput.setPlaceholderText('Type password . . .')
            self.cmdline.cmdinput.setEchoMode(QLineEdit.Password)
    
    
    def new_connection(self,socket):
        self.__connection = socket
    
    '''
    def graph(self):
        while self.show_grap:
            #time.sleep(5)
            #show the graph element
            #self.__connection.send('<cpu_graph_percent>'.encode()) <-- this would return to the client a value of <int:cpupercent>
    
    def print_graph(self,x,y):
        ###THIS FUNCTION WILL BE EXECUTED FROM THE LISTEN SERVER THREAD.
        #maximum of 50 values on display at once with a delay of 5 seconds each.
        
    '''
    
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
                    if self.__auth:
                        self.cmdline.addText(self.servername + ' >  ' + command)
                        self.__connection.send((command).encode())
                    else:
                        self.__connection.send(command.encode())
                except:
                    self.cmdline.addText('Conection was lost.')
    
    
    def response(self, data):
        self.cmdline.addText(data)
    
    def clear(self):
        self.cmdline.setText('')
        self.cmdline.label.setHidden(True)
    
    def closeTab(self):
        self.deleteLater()
    
    
    def __exit(self):
        try:
            self.__connection.send('exit'.encode())
        except:
            self.__connection.close()
            self.closeTab()


#________


def disconnect(id:str):
    sockets[id].close()


def attempt_reconnect(address):
    for i in range(0,5):
        client_socket = socket.socket()
        time.sleep(1)
        try:
            client_socket.connect((address[0],address[1]))
            client_socket.setblocking(0)
            client_socket.send('<testing_connection>'.encode())
            return client_socket
        except:
            pass
    return None


def listen(client, connection_id:str):
    global force_stopped_threads
    auth = False
    while True:
        if connection_id in force_stopped_threads:
            client[1].closeTab()
            client[0].close()
            sys.exit()
        try:
            data = client[0].recv(2048)
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
                elif cleaned == 'resetting':
                    address = client[0].getpeername()
                    client[0].close()
                    auth = False
                    client[1].clear()
                    client[1].response('reconnecting...')
                    client[0] = attempt_reconnect(address)
                    if client[0] != None:
                        client[1].new_connection(client[0])
                        client[1].authenticated(False)
                    else:
                        client[1].response('Failed to reconnect.')
                        client[1].closeTab()
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
