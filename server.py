import sys
import os
import socket
from cmd import cmd_run
import threading
from datetime import datetime



def write_to_logs(info:str) -> None:
    with open('logs.txt', 'a') as file:
        text = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' : ' + info + '\n'
        file.write(text)
        return


def disconnect():
    global force_stop
    force_stop = True
    write_to_logs('Closed server')
    print('Closed server')


def connect():
    try:
        server_socket = socket.socket()
        server_socket.bind(('0.0.0.0',port))
        server_socket.listen(5)
        server_socket.setblocking(0)
        print('Started server')
        write_to_logs('Started server')
        return server_socket
    except:
        print('There was an error starting the server. PORT already in use!')
        return sys.exit()


def listen(connection,auth):
    global force_stop
    global reset
    while True:
        if not force_stop:
            try:
                data = connection.recv(1024)
                if data is not None:
                    cleaned = data.decode()
                    if cleaned == '<testing_connection>':
                        pass
                    elif not auth:
                        if cleaned == password:
                            auth = True
                            msg = 'OK'
                            connection.send(msg.encode())
                        else:
                            if cleaned == 'disconnect' or cleaned == 'exit' or cleaned == 'leave' or cleaned == 'exit':
                                msg = 'closing socket'
                                connection.send(msg.encode())
                                connection.close()
                                break
                            else:
                                msg = 'incorrect password'
                                connection.send(msg.encode())
                    else:
                        if len(cleaned) > 0:
                            if cleaned[0] == '$':
                                command_thread = threading.Thread(target=cmd_run,args=[connection,cleaned.split('$',1)[1]])
                                command_thread.start()
                                if cleaned == '$kill':
                                    disconnect()
                                elif cleaned == '$reset':
                                    reset = True
                                    disconnect()
                                    if authentication:
                                        os.system('python ' + sys.argv[0] + ' ' + str(port) + ' -p ' + password)
                                    else:
                                        os.system('python ' + sys.argv[0] + ' ' + str(port))
                            write_to_logs(cleaned)
            except:
                pass
        else:
            if not reset:
                connection.send('closing socket'.encode())
            else:
                connection.send('resetting'.encode())
            connection.close()
            break


def accept(server_socket):
    while True:
        if not force_stop:
            try:
                conn, addr = server_socket.accept()
                if authentication:
                    isAuthenticated = False
                    conn.send('enter password'.encode())
                else:
                    isAuthenticated = True
                    conn.send('OK'.encode())
                write_to_logs('New connection from IP : ' + str(addr[0]))
                t = threading.Thread(target=listen,args=[conn,isAuthenticated])
                t.start()
            except:
                pass
        else:
            server_socket.close()
            sys.exit()


def main():
    server_socket = connect()
    t1 = threading.Thread(target=accept,args=[server_socket])
    t1.start()
    t1.join()
    sys.exit()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except:
            print('Invalid port! (must be a numeric value)')
            sys.exit()
        if len(sys.argv) == 4:
            if sys.argv[2] == '-p':
                authentication = True
                password = sys.argv[3]
        else:
            authentication = False
            password = None
    else:
        print('Usage: python ' + sys.argv[0] + ' <port number>\nFor authenticated connection use: -p <password>')
        sys.exit()
    force_stop = False
    reset = False
    main()
