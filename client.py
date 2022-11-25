import socket
import sys
import os
import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMenu, QDialog, QTabWidget, QVBoxLayout, QMessageBox, QDialogButtonBox, QTableWidget, QTableView, QScrollArea, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QIcon
from PyQt5 import Qt
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore


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
        self.setStyleSheet('QScrollArea{border:none;border-bottom:1px solid #dadce0;}')
        self.verticalScrollBar().setStyleSheet(stylesheet)
        self.horizontalScrollBar().setStyleSheet(stylesheet)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.Qt.AlignTop)
        layout.addWidget(self.label)
 
    def setText(self, text):
        self.label.setText(text)
 
    def text(self):
        get_text = self.label.text()
        return get_text

stylesheet = """
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
        self.__tabwidget.addTab(MainTab(self), "Servers")
        vbox = QVBoxLayout()
        vbox.addWidget(self.__tabwidget)
        self.setLayout(vbox)
    
    def NewTab(self, name:str, connection):
        tab = ServerTab(connection, self)
        self.__tabwidget.addTab(tab, name)
        self.__tabwidget.setCurrentIndex(self.__tabwidget.count() - 1)
        return tab
    


    def __actionQuitter(self):
        return QCoreApplication.exit(0)
    
    def alert(self, msg:str,ip,port,window):
        self.__alert = QMessageBox.critical(
            self,
            'Error.',
            msg,
            buttons=QMessageBox.Retry | QMessageBox.No,
            defaultButton=QMessageBox.Retry,
        )
        if self.__alert == QMessageBox.Retry:
            connect(ip,port,window)
        else:
            pass
            
    
    def closeEvent(self, event):
        global force_stopped_threads
        for i in sockets:
            force_stopped_threads.append(i)
        event.accept()


class MainTab(QMainWindow):
    def __init__(self, window):
        super().__init__()
        widget = QWidget()
        self.__parent = window
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.__ipinput = QLineEdit()
        self.__ipinput.setPlaceholderText('IP')
        self.__portinput = QLineEdit()
        self.__portinput.setPlaceholderText('PORT')
        self.__connectbutton = QPushButton('Connect')
        self.__connectbutton.clicked.connect(self.__connect_to_serv)
        self.__table = self.__ip_list()
        
        grid.addWidget(self.__table,0,0,1,2)
        grid.addWidget(self.__ipinput,1,0)
        grid.addWidget(self.__portinput,1,1)
        grid.addWidget(self.__connectbutton,2,0,1,2)
    
    
    def __ip_list(self):
        tableWidget = QTableWidget();
        tableWidget.setColumnCount(2)
        with open('iplist.txt','r') as file:
            lines = file.readlines()
            tableWidget.setRowCount(len(lines))
            for i in range(len(lines)):
                data = lines[i].replace('\n','').split(',')
                tableWidget.setItem(i, 0, QTableWidgetItem(data[0]))
                tableWidget.setItem(i, 1, QTableWidgetItem(data[1]))
        tableWidget.horizontalHeader().setStretchLastSection(True)
        tableWidget.verticalHeader().setVisible(False)
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tableWidget.setHorizontalHeaderLabels(['Server name','Server address'])
        return tableWidget

    
    def __connect_to_serv(self):
        if len(self.__ipinput.text()) > 0 and len(self.__portinput.text()) > 0:
            ip = self.__ipinput.text()
            try:
                port = int(self.__portinput.text())
            except:
                return print('not a number')
            connect(ip,port,self.__parent)
        else:
            print('please fill all fields!')


class ServerTab(QMainWindow):
    def __init__(self, connection, parent):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        self.__connection = connection
        self.setStyleSheet('background-color:#19002c;color:white;')
        widget.setLayout(grid)
        self.__parent = parent
        self.__auth = False
        self.__cmdinput = QLineEdit('')
        self.__cmdinput.setPlaceholderText('Type command...')
        self.__cmdinput.setStyleSheet('padding:5px;border:none;')
        self.__cmdinput.editingFinished.connect(self.__send_message)
        self.__cmdbutton = QPushButton('SEND')
        self.__cmdbutton.setFixedWidth(50)
        self.__cmdlabel = ScrollLabel()
        self.__cmdbutton.setStyleSheet('background-color:white;padding:5px;border-radius:10px;color:#19002c;font-weight:400;font-family:arial;text-align:center;')
        self.__cmdbutton.clicked.connect(self.__send_message)
        self.__messagebox = QMessageBox()
        grid.addWidget(self.__cmdlabel,0,0,1,2)
        grid.addWidget(self.__cmdinput,1,0)
        grid.addWidget(self.__cmdbutton,1,1)
    
    
    def authentified(self):
        self.__auth = True
        self.__cmdlabel.setText('Established connection with ' + str(self.__connection.getsockname()[0]) + ':' + str(self.__connection.getsockname()[1]) + '\n')
    
    
    def __send_message(self):
        command = self.__cmdinput.text()
        if len(command) > 0:
            if self.__auth and (command.lower() == 'clear' or command.lower() == 'cls'):
                self.__cmdinput.setText('')
                self.__cmdlabel.setText('')
            else:
                try:
                    self.__cmdinput.setText('')
                    if self.__auth:
                        self.__cmdlabel.setText(self.__cmdlabel.text() + 'You > ' + command + '\n')
                        self.__connection.send(('$' + command).encode())
                    else:
                        self.__connection.send(command.encode())
                except:
                    self.__cmdlabel.setText(self.__cmdlabel.text() + 'Conection was lost. \n')
    
    
    def response(self, data):
        self.__cmdlabel.setText(self.__cmdlabel.text() + data + '\n')
        self.__cmdlabel.verticalScrollBar().setValue(self.__cmdlabel.verticalScrollBar().maximum())
    
    
    def __info_box(self, message):
        self.__messagebox.setIcon(QMessageBox.Information)
        self.__messagebox.setWindowTitle('Info')
        self.__messagebox.resize(500, 500)
        self.__messagebox.exec()
    
    
    def closeTab(self):
        #self.__info_box('Connection was closed.') NEED TO FIX THIS ISSUE (cannot create window because parent is in another thread) !!!
        self.deleteLater()


#________


def disconnect(id:str):
    sockets[id].close()


def listen(client, this_id:str):
    global force_stopped_threads
    auth = False
    while True:
        if this_id in force_stopped_threads:
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
                    client[1].authentified()
                if cleaned == 'closing socket':
                    force_stopped_threads.append(this_id)
        except:
            #client[1].closeTab()
            #client[0].close()
            pass


def connect(ip: str ,port: int, window):
    global sockets
    try:
        client_socket = socket.socket()
        client_socket.connect((ip,port))
        client_socket.setblocking(0)
        if len(list(sockets)) > 0:
            id = str(int(list(sockets)[len(list(sockets)) - 1]) + 1)
        else:
            id = '0'
        tab = window.NewTab('Server ' + id, client_socket)
        t1 = threading.Thread(target=listen,args=[[client_socket, tab], id])
        t1.start()
        sockets[id] = [client_socket, tab]
    except:
        window.alert('Error while trying to connect to server!\nWould you like to try again? ',ip,port,window)


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
