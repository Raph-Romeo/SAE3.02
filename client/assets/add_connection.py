from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QCursor, QIcon
from PyQt5 import QtCore
from PyQt5 import Qt


class NewConnectionTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setRowStretch(5, 1)
        self.__parent = parent
        self.setAttribute(Qt.Qt.WA_StyledBackground, True)
        self.setStyleSheet("""QWidget{background:rgb(32,34,37);font-family:verdana}QLineEdit{border:none;border-radius:2px;background:rgb(54,57,63);font-size:12px;padding:5px;font-family:verdana;color:#FFF;margin:1px;margin-top:0px;}
        QPushButton{border-radius:2px;background:rgb(54,57,63);font-size:12px;font-family:arial;color:white;padding:5px;margin:1px;margin-top:0px;padding-left:10px;padding-right:10px;}
        QLabel{font-size:12px;padding-left:20px;padding-bottom:5px;padding-top:10px;color:#FFF;font-weight:bold;font-family:verdana;border-top:2px solid rgb(43,45,50);}""")
        top_bar = QLabel('Connect')
        top_bar.setFixedHeight(51)
        top_bar.setAlignment(Qt.Qt.AlignCenter)
        top_bar.setStyleSheet('background:rgb(54,57,63);text-align:center;border-bottom:1px solid rgb(35,36,40);color:rgb(255,255,255);font-size:12px;font-weight:bold;')
        self.name_input = QLineEdit()
        self.name_input.returnPressed.connect(self.connect)
        self.name_input.setPlaceholderText('SERVER NAME')
        self.ip_input = QLineEdit()
        self.ip_input.returnPressed.connect(self.connect)
        self.ip_input.setPlaceholderText('ADDRESS')
        self.port_input = QLineEdit()
        self.port_input.returnPressed.connect(self.connect)
        self.port_input.setPlaceholderText('PORT')
        self.connect_button = QPushButton(' CONNECT')
        self.connect_button.setIcon(QIcon('assets/img/connect.png'))
        self.connect_button.clicked.connect(self.connect)
        self.connect_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        layout.addWidget(top_bar, 0, 0, alignment=Qt.Qt.AlignTop)
        layout.addWidget(self.name_input, 1, 0)
        layout.addWidget(self.ip_input, 2, 0)
        layout.addWidget(self.port_input, 3, 0)
        layout.addWidget(self.connect_button, 4, 0)
        self.setLayout(layout)

    def connect(self):
        ip = self.ip_input.text()
        port = self.port_input.text()
        name = self.name_input.text()
        if len(ip) > 0 and port.isdigit() and len(name) > 0:
            self.ip_input.setText('')
            self.port_input.setText('')
            self.name_input.setText('')
            self.__parent.connection(ip, int(port), name)
            self.__parent.tab_index(0)
        else:
            self.__parent.error('form is invalid!')
