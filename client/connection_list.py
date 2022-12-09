from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout,  QTableWidget, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QCursor, QIcon, QPixmap
from PyQt5 import Qt
from PyQt5 import QtCore


class connection_table_item(QWidget):
    def __init__(self, parent, name, addr):
        super().__init__()
        self.__parent = parent
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        layout = QHBoxLayout()
        self.__addr = addr
        self.__image = QLabel()
        self.__image.setPixmap(QPixmap('assets/connection.png'))
        self.__image.setFixedWidth(30)
        self.__image.setFixedHeight(20)
        self.__image.setStyleSheet('padding:0;margin-left:10')
        self.__image.setScaledContents(True)
        self.__name = QLabel(name + '\n' + self.__addr)
        self.__is_selected = False
        self.__name.setStyleSheet('border:none;margin-left:0px;margin:5px;background:transparent;font-size:12px;color:rgb(195,195,195);font-family:verdana')
        layout.addWidget(self.__image)
        layout.addWidget(self.__name)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

    def rename(self, name):
        self.__name.setText(name + '\n' + self.__addr)

    def selected(self, state: bool):
        if state and not self.__is_selected:
            self.__name.setStyleSheet('border:none;margin-left:0px;margin:5px;background:transparent;font-size:12px;color:white;font-family:verdana')
            self.__is_selected = True
        elif self.__is_selected:
            self.__name.setStyleSheet('border:none;margin-left:0px;margin:5px;background:transparent;font-size:12px;color:rgb(195,195,195);font-family:verdana')
            self.__is_selected = False

class connections_title(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.__parent = parent
        layout = QHBoxLayout()
        self.__label = QLabel('Connections')
        self.setStyleSheet('padding-top:10px;')
        self.__label.setStyleSheet('border:none;margin:5px;background:transparent;font-size:12px;color:rgb(195,195,195)')
        self.__add_button = QPushButton()
        self.__add_button.setIcon(QIcon('assets/add.png'))
        self.__add_button.setStyleSheet('QPushButton{border:none;font-size:12px;font-weight:bold;}QToolTip{background-color: black; color: white; border: black solid 1px;padding:2px;border-radius:5%;}')
        self.__add_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__add_button.setToolTip('Add connection')
        self.__add_button.clicked.connect(self.__parent.add_connection_button)
        self.__add_button.setFixedWidth(16)
        self.__add_button.setFocusPolicy(QtCore.Qt.NoFocus)
        layout.addWidget(self.__label)
        layout.addWidget(self.__add_button)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)


class ConnectionList(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        widget = QWidget()
        grid = QGridLayout(widget)
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(widget)
        self.__parent = parent
        self.setStyleSheet("""
        QMainWindow{background:rgb(47,49,54)}
        """)
        top_bar = QLabel('Connection list')
        top_bar.setFixedHeight(51)
        top_bar.setAlignment(Qt.Qt.AlignCenter)
        top_bar.setStyleSheet('background:rgb(47,49,54);text-align:center;border-bottom:1px solid rgb(35,36,40);color:rgb(255,255,255);font-size:12px;font-weight:bold;')
        self.__send_to_all = QLineEdit()
        self.__connections = []
        self.__send_to_all.setPlaceholderText('Type to send to all ...')
        self.__send_to_all.setDisabled(True)
        self.__send_to_all.returnPressed.connect(self.__send)
        self.__send_to_all.setStyleSheet('QLineEdit{border:none;padding:12px;color:white;margin:8px;background:rgb(66,70,77);border-radius:8%;}QLineEdit:disabled{color:rgb(195,195,195);}')
        self.__close_all = QPushButton('  Disconnect from all')
        self.__close_all.setIcon(QIcon('assets/close.png'))
        self.__close_all.setFocusPolicy(QtCore.Qt.NoFocus)
        self.__close_all.setStyleSheet('QPushButton{border:none;padding:12px;margin:5px;background:transparent;font-size:12px;font-family:verdana;color:rgb(195,195,195);text-align: left;}QPushButton:hover{color:white;}')
        self.__close_all.clicked.connect(self.__disconnect_from_all)
        self.__close_all.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__connections_title = connections_title(self)
        self.__connections_title.setFixedWidth(100)
        self.__connection_list = self.__maketable()
        grid.setRowStretch(4, 1)
        grid.addWidget(top_bar, 0, 0, alignment=Qt.Qt.AlignTop)
        grid.addWidget(self.__send_to_all, 1, 0, alignment=Qt.Qt.AlignTop)
        grid.addWidget(self.__close_all, 2, 0, alignment=Qt.Qt.AlignTop)
        grid.addWidget(self.__connections_title, 3, 0, alignment=Qt.Qt.AlignTop)
        grid.addWidget(self.__connection_list, 4, 0)

    def __maketable(self):
        tableWidget = QTableWidget()
        tableWidget.setRowCount(0)
        tableWidget.setColumnCount(1)
        tableWidget.horizontalHeader().setStretchLastSection(True)
        tableWidget.verticalHeader().setVisible(False)
        tableWidget.horizontalHeader().setVisible(False)
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        tableWidget.clicked.connect(self.__tableitemselect)
        tableWidget.setStyleSheet("""
        QTableWidget::item{border:0px;border-bottom:1px solid rgb(56,60,67);margin-left:5px;margin-right:5px;} 
        QTableWidget{gridline-color:transparent;color:#FFF;font-family:Verdana;font-size:12px;border:0px transparent;background:rgb(47,49,54)} 
        QTableWidget::item:hover{background: rgb(66,70,77);border-radius:5px;}
        QTableWidget::item:selected {background: rgb(66,70,77);border-radius:5px;} 
        QHeaderView::section{border-top:0px;border-left:0px;border-bottom: 1px solid rgb(43,45,50);padding-left:4px;padding-top:13px;padding-bottom:14px;}
        QTableCornerButton::section{border-top:0px solid #D8D8D8;border-left:0px solid #D8D8D8;border-bottom: 2px solid rgb(43,45,50);}
        QLineEdit{border:none;border-radius:5px;background:#202225;font-size:12px;padding:5px;font-family:verdana;color:#FFF;margin:3px;margin-top:0px}
        QScrollBar:vertical{background-color: transparent;width: 15px;margin: 15px 3px 15px 3px;border: 1px transparent;border-radius: 4px;}
        QScrollBar::handle:vertical{background-color: rgb(32,34,37);min-height: 5px;border-radius: 4px;}
        QScrollBar::sub-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
        QScrollBar::add-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
        QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on{height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
        QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on{height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
        QLabel{color:white;padding-left:10px;}
        """)
        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tableWidget.setHorizontalHeaderLabels(['Server name', 'Server address'])
        return tableWidget

    def clear_connections(self):
        self.__connections = []
        self.__connection_list.setRowCount(0)
        self.__connection_list.resizeRowsToContents()
        self.send_to_all_toggle()

    def add_connection(self, connection):
        row = self.__connection_list.rowCount()
        self.__connection_list.setRowCount(self.__connection_list.rowCount() + 1)
        item = connection_table_item(self, connection.servername, connection.address())
        item.selected(True)
        self.__connection_list.setCellWidget(row, 0, item)
        self.__connection_list.resizeRowsToContents()
        self.__connections.append(connection)
        item.setFocus()
        self.send_to_all_toggle()

    def remove_connection(self, connection):
        index = self.__connections.index(connection)
        self.__connections.remove(connection)
        self.__connection_list.removeRow(index)
        self.send_to_all_toggle()

    def send_to_all_toggle(self):
        if len(self.__connections) > 0:
            self.__send_to_all.setDisabled(False)
        else:
            self.__send_to_all.setDisabled(True)

    def __tableitemselect(self, item):
        tab = self.__connections[item.row()]
        self.__parent.tab_index(self.__parent.getTabIndex(tab))

    def add_connection_button(self):
        self.__parent.tab_index(1)

    def tab_changed(self, tab):
        row = None
        for i in range(self.__connection_list.rowCount()):
            widget = self.__connection_list.cellWidget(i, 0)
            widget.selected(False)
        for i in range(len(self.__connections)):
            if self.__connections[i] == tab:
                row = i
        if row is not None:
            widget = self.__connection_list.cellWidget(row, 0)
            widget.selected(True)
            self.__parent.tab_index(self.__parent.getTabIndex(tab))

    def __disconnect_from_all(self):
        for i in self.__connections:
            i.multi_exit()
        self.__parent.refresh()
        self.clear_connections()

    def rename(self, tab, name):
        row = None
        for i in range(len(self.__connections)):
            if tab == self.__connections[i]:
                row = i
        if row is None:
            return
        item = self.__connection_list.cellWidget(row, 0)
        item.rename(name)

    def __send(self):
        command = self.__send_to_all.text()
        for i in self.__connections:
            i.handle_input(command)
        self.__send_to_all.setText('')
