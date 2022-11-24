import sys
import subprocess
from socket import gethostname
import os


def windows_command(cmd_in: str) -> str:
    try:
        cmd = cmd_in.lower()
        if len(cmd.split(' ')) > 1:
            cmd = cmd.split(' ')[0]
            args = cmd_in.split(' ', 1)[1].lower()
        else:
            args = None
        if cmd == 'os':
            return 'Operating System: Windows 10\nMachine name: ' + gethostname()
        elif cmd == 'ip':
            if args is None:
                return str(subprocess.check_output('ipconfig', shell=True)).replace('\\r\\n','\n').split("'",1)[1].split("'",1)[0]
            elif args == '-a':
                return str(subprocess.check_output('ipconfig /all', shell=True)).replace('\\r\\n','\n').split("'",1)[1].split("'",1)[0]
            else:
                return str('unrecognized argument : ' + cmd_in.split(' ', 1)[1])
        elif cmd == 'ram':
            return os.system('')
        elif cmd == 'disconnect' or cmd == 'exit' or cmd == 'quit' or cmd == 'leave':
            return 'closing socket'
        elif cmd == 'kill':
            return 'closing socket'
        elif cmd == 'reset':
            return 'closing socket'
        elif cmd == 'logs':
            if args != None:
                if args == 'clear':
                    with open('logs.txt','w') as file:
                        file.write('')
                    return 'Server logs were cleared!'
                else:
                    i = int(args)
                    if i < 1:
                        return 'logs : value must be superior to 0!'
            else:
                i = 25
            with open('logs.txt','r') as file:
                lines = file.readlines()
                if i > len(lines):
                    i = len(lines)
                    string = f'Showing all logs:\n'
                else:
                    string = f'Showing {i} of the last logs:\n'
                for line in lines[len(lines)-i:len(lines)]:
                    string += line
            return string
        elif cmd == 'help':
            return 'List of commands:\nOS - displays operating system details\nIP - displays all ip information of the machine\nRAM - displays total memory available on the machine\nDISCONNECT -closes client connection\nKILL -closes server socket'
        elif cmd == 'ping':
            ip = args
            return str(subprocess.check_output('ping ' + ip, shell=True)).replace('\\r\\n','\n').split("'",1)[1].split("'",1)[0]
        elif cmd == 'echo':
            return cmd_in.split(' ',1)[1]
        else:
            return 'Command not found. Type help for a list of available commands'
    except:
        return 'Error when executing command: ' + cmd_in


def cmd_run(connection, cmd:str) -> None:
    if sys.platform == "linux" or sys.platform == "linux2":
        print("NOT DONE YET") #LINUX
    elif sys.platform == "darwin":
        print("NOT DONE YET") #MACOS
    elif sys.platform == "win32":
        data = windows_command(cmd).encode()
    connection.send(data)
    if cmd == 'disconnect' or cmd == 'kill' or cmd == 'exit' or cmd == 'quit' or cmd == 'leave':
        connection.close()
    sys.exit()
