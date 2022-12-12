import sys
from PyQt5.QtWidgets import QApplication
from assets.main_window import MainWindow


def main():
    if len(sys.argv) == 2:
        file = sys.argv[1]
    else:
        file = 'iplist.csv'
    app = QApplication(sys.argv)
    window = MainWindow(file)
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
