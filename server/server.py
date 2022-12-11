import threading
import socket
import sys
from datetime import datetime
from cmd import execute, cpu_percent, ram_percent
import time


class Client:
    def __init__(self, auth: bool, connection):
        self.__auth = auth
        self.__connection = connection
        self.__open = True
        self.__cpu_graph_sub = False
        self.__ram_graph_sub = False

    def is_cpu_subbed(self) -> bool:
        return self.__cpu_graph_sub

    def is_ram_subbed(self) -> bool:
        return self.__ram_graph_sub

    def sub_cpu(self, state):
        if state:
            self.__cpu_graph_sub = True
        else:
            self.__cpu_graph_sub = False

    def sub_ram(self, state):
        if state:
            self.__ram_graph_sub = True
        else:
            self.__ram_graph_sub = False

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

    def send(self, msg) -> bool:
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
        self.__resetting = False

    def log(self, info: str) -> None:
        try:
            with open('logs.txt', 'a') as file:
                text = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' : ' + info + '\n'
                file.write(text)
        except:
            print("Couldn't write to logs")

    def start(self, option: int = 0):
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
            print('Server started')
            threading.Thread(target=self.__accept).start()
            if option == 0:
                threading.Thread(target=self.__graph).start()

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

    def __graph(self):
        while not self.__forcestop and not self.__resetting:
            time.sleep(1)
            for client in self.__clients:
                if client.is_cpu_subbed():
                    client.send('<CPU|' + str(cpu_percent()) + '|>')
                if client.is_ram_subbed():
                    client.send('<RAM|' + str(ram_percent()) + '|>')

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
                    elif cmd == '<sub_cpu_true>':
                        c.sub_cpu(True)
                        c.send('Subscribed to CPU topic')
                    elif cmd == '<sub_ram_true>':
                        c.sub_ram(True)
                        c.send('Subscribed to RAM topic')
                    elif cmd == '<sub_cpu_false>':
                        c.sub_cpu(False)
                        c.send('Unsubscribed from CPU topic')
                    elif cmd == '<sub_ram_false>':
                        c.sub_ram(False)
                        c.send('Unsubscribed from RAM topic')
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
        self.__resetting = True
        self.__close('resetting')
        self.__clients = []
        self.__forcestop = False
        self.start(1)
        self.__resetting = False


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
