import threading
import socket
import sys
import time
from datetime import datetime
from cmd import execute


class Client:
    def __init__(self, auth:bool, connection):
        self.__auth = auth
        self.__connection = connection
        self.__open = True

    def is_authenticated(self) -> bool:
        return self.__auth

    def authenticate(self) -> None:
        self.__auth = True

    def close(self, param='closing socket') -> None:
        try:
            self.__connection.send(param.encode())
        except:
            pass
        self.__connection.close()
        self.__open = False

    def is_open(self) -> bool:
        return self.__open

    def send(self, msg):
        try:
            self.__connection.send(msg.encode())
            return True
        except:
            return False

    def data(self, payload=1024):
        try:
            if self.is_open():
                data = self.__connection.recv(payload)
                if len(data) > 0:
                    return data.decode()
                else:
                    return None
            else:
                return None
        except:
            return None


class Server:
    def __init__(self, port, host='0.0.0.0', password=None):
        self.__server = None
        self.__host = host
        self.__port = port
        self.__password = password
        self.__forcestop = False
        self.__clients = []

    def log(self, info: str) -> None:
        with open('logs.txt', 'a') as file:
            text = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' : ' + info + '\n'
            file.write(text)
            return

    def start(self):
        self.__server = socket.socket()
        try:
            self.__server.bind((self.__host, self.__port))
            self.__server.listen(5)
            self.__server.setblocking(False)
        except:
            print('EXIT: Failed to start server')
            sys.exit()
        else:
            self.log('Sarted server')
            threading.Thread(target=self.__accept).start()

    def __accept(self):
        while not self.__forcestop:
            try:
                conn, addr = self.__server.accept()
                if self.__password is not None:
                    c = Client(False, conn)
                else:
                    c = Client(True, conn)
                self.__clients.append(c)
                self.log('connection from: ' + addr[0])
                threading.Thread(target=self.__listen, args=[c]).start()
            except:
                pass

    def __disconnect(self, c):
        c.close()
        self.__clients.remove(c)

    def __listen(self, c):
        if c.is_authenticated():
            c.send('OK')
        else:
            c.send('enter password')
        while not self.__forcestop and c.is_open():
            data = c.data()
            if data is not None:
                cmd = data.lower()
                self.log(cmd)
                if cmd == '<testing_connection>':
                    if self.__forcestop:
                        self.__disconnect(c)
                elif cmd == 'disconnect' or cmd == 'exit' or cmd == 'leave' or cmd == 'quit':
                    self.__disconnect(c)
                elif not c.is_authenticated():
                    if data != self.__password:
                        c.send('incorrect password')
                    else:
                        c.authenticate()
                        c.send('OK')
                else:
                    if cmd == 'kill':
                        self.__close()
                    elif cmd == 'reset':
                        self.__reset()
                    else:
                        threading.Thread(target=execute, args=[c, data]).start()

    def __close(self, param=None):
        for c in self.__clients:
            if param is None:
                c.close()
            else:
                c.close(param)
        self.__forcestop = True
        self.log('Closed server')
        self.__server.close()

    def __reset(self):
        self.__close('resetting')
        self.__clients = []
        self.__forcestop = False
        self.start()


def main():
    if len(sys.argv) >= 2:
        if sys.argv[1].isdigit():
            port = int(sys.argv[1])
        else:
            print("EXIT: Port must be an integer!")
            sys.exit()
        if '-p' in sys.argv:
            server = Server(port, password=sys.argv[sys.argv.index('-p') + 1])
        else:
            server = Server(port)
        server.start()
    else:
        print('Usage: python3 ' + sys.argv[0] + ' <port number>\nFor authenticated connection use option: -p <password>\n\nExample: python3 ' + sys.argv[0] + ' 8800 -p my_password')
        sys.exit()


if __name__ == '__main__':
    main()
