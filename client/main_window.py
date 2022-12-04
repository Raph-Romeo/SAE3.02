from PyQt5.QtWidgets import QWidget, QMainWindow, QTabWidget, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from main_tab import MainTab
from server_tab import ServerTab


class MainWindow(QMainWindow):
    def __init__(self, file_path):
        super().__init__()
        self.setWindowTitle("SuperShell")
        self.resize(720, 500)
        self.setStyleSheet("""
                QMainWindow{background: rgb(10,10,10)}
                QTabWidget::pane {border:0px;background:rgb(245, 245, 245);} 
                QTabBar::tab {background: rgb(10,10,10);border:none;padding:12px;color:#AAA;}
                QTabBar::tab:hover {background:rgb(10,10,10);color:white;}
                QTabBar::tab:selected {background:rgb(23,23,23);color:white;}
                """)
        vbox = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(vbox)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(widget)
        self.setWindowIcon(QIcon("icon.png"))
        self.__connections = []
        self.__tab_widget = QTabWidget()
        self.__main = MainTab(self, file_path)
        self.__tabbarhidden = True
        self.__tab_widget.addTab(self.__main, "Home")
        self.__tab_widget.tabBar().hide()
        vbox.addWidget(self.__tab_widget)

    def NewTab(self, name: str, connection):
        tab = ServerTab(connection, self, name)
        self.__connections.append(tab)
        self.__tab_widget.addTab(tab, name)
        self.__tab_widget.setCurrentIndex(self.__tab_widget.count() - 1)
        if self.__tabbarhidden:
            self.__tab_widget.tabBar().show()
            self.__tabbarhidden = False
        return tab

    def hideTab(self, action=None):
        if action is None:
            return self.__tabbarhidden
        elif action:
            self.__tabbarhidden = False
            self.__tab_widget.tabBar().show()
        else:
            self.__tabbarhidden = True
            self.__tab_widget.tabBar().hide()

    def connections_remove(self, tab):
        self.__connections.remove(tab)

    def number_of_connections(self) -> int:
        return len(self.__connections)

    def renameTab(self, name: str):
        self.__tab_widget.setTabText(self.__tab_widget.currentIndex(), name)

    def alert(self, ip, port, name):
        self.__alert = QMessageBox.critical(self, 'Connection error', 'Error while trying to connect to server!\nWould you like to try again?', buttons=QMessageBox.Retry | QMessageBox.No, defaultButton=QMessageBox.Retry)
        if self.__alert == QMessageBox.Retry:
            self.__main.connection_Qthread(ip, port, name)
        else:
            pass

    def error(self, msg):
        QMessageBox.critical(self, 'error', msg, buttons=QMessageBox.Ok)

    def closeEvent(self, event):
        for i in self.__connections:
            i.force_stop()
        event.accept()
