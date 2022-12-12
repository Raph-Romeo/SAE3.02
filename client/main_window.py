from PyQt5.QtWidgets import QWidget, QMainWindow, QTabWidget, QGridLayout, QMessageBox
from PyQt5.QtGui import QIcon
from assets.main_tab import MainTab
from assets.server_tab import ServerTab
from assets.navbar import NavBar
from assets.connection_list import ConnectionList
from assets.add_connection import NewConnectionTab


class MainWindow(QMainWindow):
    def __init__(self, file_path):
        super().__init__()
        self.setWindowTitle("SuperShell")
        self.resize(720, 500)
        self.setStyleSheet("""
                QMainWindow{background: rgb(32,34,37)}
                QTabWidget::pane {border:0px;background:rgb(245, 245, 245);} 
                QTabBar::tab {background: rgb(10,10,10);border:none;padding:12px;color:#AAA;}
                QTabBar::tab:hover {background:rgb(10,10,10);color:white;}
                QTabBar::tab:selected {background:rgb(23,23,23);color:white;}
                """)
        grid = QGridLayout()
        widget = QWidget()
        widget.setLayout(grid)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)
        self.setCentralWidget(widget)
        self.setWindowIcon(QIcon("assets/img/icon.png"))
        self.__connections = []
        self.__tab_widget = QTabWidget()
        self.__main = MainTab(self, file_path)
        self.__new_connection = NewConnectionTab(self)
        self.__tab_widget.addTab(self.__main, "Home")
        self.__tab_widget.addTab(self.__new_connection, "New connection")
        self.__tab_widget.tabBar().hide()
        self.__tab_widget.setMinimumWidth(501)
        self.__tab_widget.currentChanged.connect(self.__tab_changed)
        self.__navbar = NavBar(self)
        self.__navbar.setFixedWidth(72)
        self.__connectionlist = ConnectionList(self)
        self.__connectionlist.setFixedWidth(234)
        grid.addWidget(self.__navbar, 0, 0)
        grid.addWidget(self.__connectionlist, 0, 1)
        grid.addWidget(self.__tab_widget, 0, 2)

    def NewTab(self, name: str, connection):
        tab = ServerTab(connection, self, name)
        self.__connections.append(tab)
        self.__tab_widget.addTab(tab, name)
        self.__tab_widget.setCurrentIndex(self.__tab_widget.count() - 1)
        self.__connectionlist.add_connection(tab)
        return tab

    def __tab_changed(self):
        tab = self.__tab_widget.currentWidget()
        self.__connectionlist.tab_changed(tab)

    def getTabIndex(self, tab):
        for i in range(self.__tab_widget.count()):
            if tab == self.__tab_widget.widget(i):
                return i

    def connections_remove(self, tab):
        self.__connections.remove(tab)
        self.__connectionlist.remove_connection(tab)

    def number_of_connections(self) -> int:
        return len(self.__connections)

    def tab_index(self, num: int):
        self.__tab_widget.setCurrentIndex(num)

    def renameTab(self, name: str):
        self.__tab_widget.setTabText(self.__tab_widget.currentIndex(), name)
        self.__connectionlist.rename(self.__tab_widget.currentWidget(), name)

    def alert(self, ip, port, name):
        self.__alert = QMessageBox.critical(self, 'Connection error', 'Error while trying to connect to server!\nWould you like to try again?', buttons=QMessageBox.Retry | QMessageBox.No, defaultButton=QMessageBox.Retry)
        if self.__alert == QMessageBox.Retry:
            self.__main.connection_Qthread(ip, port, name)
        else:
            pass

    def error(self, msg):
        QMessageBox.critical(self, 'error', msg, buttons=QMessageBox.Ok)

    def refresh(self):
        self.__connections = []

    def toggle_connection_list(self):
        if self.__connectionlist.isHidden():
            self.__connectionlist.setHidden(False)
        else:
            self.__connectionlist.setHidden(True)

    def closeEvent(self, event):
        for i in self.__connections:
            i.multi_exit()
        event.accept()

    def connection(self, ip, port, name=None):
        if name is None:
            name = ip + ':' + str(port)
        self.__main.connection_Qthread(ip, port, name)
