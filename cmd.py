import sys
import subprocess
from socket import gethostname
import os


def windows_command(cmd_in: str) -> str:
    try:
        cmd = cmd_in.lower()
        if cmd == 'os':
            return 'Operating System: Windows 10\nMachine name: ' + gethostname()
        elif cmd == 'ip':
            return str(subprocess.check_output('ipconfig', shell=True)).replace('\\r\\n','\n').split("'",1)[1].split("'",1)[0]
        elif cmd == 'ip -a':
            return str(subprocess.check_output('ipconfig /all', shell=True)).replace('\\r\\n','\n').split("'",1)[1].split("'",1)[0]
        elif cmd == 'ram':
            return os.system('')
        elif cmd == 'disconnect' or cmd == 'exit' or cmd == 'quit':
            return 'closing socket'
        elif cmd == 'kill':
            return 'closing socket'
        elif cmd == 'reset':
            return 'closing socket'
        elif cmd == 'help':
            return 'List of commands:\nOS - displays operating system details\nIP - displays all ip information of the machine\nRAM - displays total memory available on the machine\nDISCONNECT -closes client connection\nKILL -closes server socket'
        elif len(cmd.split(' ')[0]) > 1:
            if cmd.split(' ')[0] == 'ping':
                ip = cmd.split(' ')[1]
                return str(subprocess.check_output('ping ' + ip, shell=True)).replace('\\r\\n','\n').split("'",1)[1].split("'",1)[0]
            elif cmd.split(' ')[0] == 'echo':
                return cmd_in.split(' ',1)[1]
            else:
                return 'Unknown command. Type help for a list of commands'
        else:
            return 'Unknown command. Type help for a list of commands'
    except:
        return 'Error'


def cmd_run(connection, cmd:str) -> None:
    if sys.platform == "linux" or sys.platform == "linux2":
        print("NOT DONE YET") #LINUX
    elif sys.platform == "darwin":
        print("NOT DONE YET") #MACOS
    elif sys.platform == "win32":
        data = windows_command(cmd).encode()
    connection.send(data)
    if cmd == 'disconnect' or cmd == 'kill' or cmd == 'exit' or cmd == 'quit':
        connection.close()
    sys.exit()

