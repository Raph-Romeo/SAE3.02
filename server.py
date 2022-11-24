import sys
import socket
from cmd import cmd_run
import threading
from datetime import datetime



def write_to_logs(info:str) -> None:
    with open('logs.txt', 'a') as file:
        text = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' : ' + info + '\n'
        file.write(text)
        return


def disconnect(server_socket):
    global force_stop
    force_stop = True
    server_socket.close()
    write_to_logs('Closed server')
    print('Closed server')


def connect():
    try:
        server_socket = socket.socket()
        server_socket.bind(('127.0.0.1',port))
        server_socket.listen(5)
        server_socket.setblocking(0)
        print('Started server')
        write_to_logs('Started server')
        return server_socket
    except:
        print('There was an error starting the server. PORT already in use!')
        return sys.exit()


def listen(connection):
    global force_stop
    while True:
        if not force_stop:
            try:
                data = connection.recv(1024)
                if data is not None:
                    cleaned = data.decode()
                    if len(cleaned) > 0:
                        if cleaned[0] == '$':
                            command_thread = threading.Thread(target=cmd_run,args=[connection,cleaned.split('$',1)[1]])
                            command_thread.start()
                            if cleaned == '$kill':
                                force_stop = True
                        write_to_logs(cleaned)
            except:
                #print('connection with client was lost')
                #connection.close()
                #sys.exit()
                pass
        else:
            break


def accept(server_socket):
    global connections
    while True:
        if not force_stop:
            try:
                conn, addr = server_socket.accept()
                write_to_logs('New connection from IP : ' + str(addr))
                t = threading.Thread(target=listen,args=[conn])
                t.start()
            except:
                pass
        else:
            print('closed')
            server_socket.close()
            sys.exit()


def main():
    server_socket = connect()
    t1 = threading.Thread(target=accept,args=[server_socket])
    t1.start()
    t1.join()
    sys.exit()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            port = int(sys.argv[1])
        except:
            print('Invalid port!')
            sys.exit()
    else:
        print('Usage: python ' + sys.argv[0] + ' <port number>')
        sys.exit()
    force_stop = False
    main()
