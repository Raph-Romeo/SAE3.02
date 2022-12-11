from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QToolButton, QLabel, QLineEdit, QPushButton, QComboBox, QMenu, QDialog, QTabWidget, QVBoxLayout, QMessageBox, QDialogButtonBox, QTableWidget, QTableView, QScrollArea, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QCursor, QIcon
from PyQt5 import Qt
import socket
import time
import threading
from PyQt5 import QtCore


class NavBar(QScrollArea):

    def __init__(self, parent, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)
        self.__parent = parent
        self.setStyleSheet('background:transparent;border:none;color:white;font-family:verdana;font-weight:bold;')
        layout = QGridLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setRowStretch(3, 2)
        self.home = QToolButton()
        self.home.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)
        self.home.setIcon(QIcon('assets/home.png'))
        self.home.setStyleSheet('QToolButton{padding-top:20px;}')
        self.home.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.home.setToolTip('Home')
        self.home.setFocusPolicy(QtCore.Qt.NoFocus)
        self.home.setFixedWidth(70)
        self.home.setFixedHeight(60)
        self.home.setText('HOME')
        self.home.clicked.connect(lambda: self.__parent.tab_index(0))

        self.connectbutton = QToolButton()
        self.connectbutton.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)
        self.connectbutton.setIcon(QIcon('assets/connect.png'))
        self.connectbutton.setStyleSheet('QToolButton{padding-top:20px;}')
        self.connectbutton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.connectbutton.setToolTip('Connect')
        self.connectbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.connectbutton.setFixedWidth(70)
        self.connectbutton.setFixedHeight(60)
        self.connectbutton.setText('CONNECT')
        self.connectbutton.clicked.connect(lambda: self.__parent.tab_index(1))

        self.sidebar = QToolButton()
        self.sidebar.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)
        self.sidebar.setIcon(QIcon('assets/menu_toggle.png'))
        self.sidebar.setStyleSheet('QToolButton{padding-top:20px;}')
        self.sidebar.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.sidebar.setToolTip('Show side panel')
        self.sidebar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sidebar.setFixedWidth(70)
        self.sidebar.setFixedHeight(60)
        self.sidebar.setText('PANEL')
        self.sidebar.clicked.connect(self.__parent.toggle_connection_list)

        layout.addWidget(self.home, 1, 0, alignment=Qt.Qt.AlignTop)
        layout.addWidget(self.connectbutton, 2, 0, alignment=Qt.Qt.AlignTop)
        layout.addWidget(self.sidebar, 0, 0, alignment=Qt.Qt.AlignTop)
