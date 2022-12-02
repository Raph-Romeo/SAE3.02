import sys
import subprocess
from socket import gethostname, gethostbyname
import psutil
import platform
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
            return subprocess.check_output('wmic os get Caption,CSDVersion /value | findstr /B /C:"Caption="', shell=True).decode().split('=')[1]
        elif cmd == 'ip':
            if args is None:
                return 'Local IP : ' + gethostbyname(gethostname())
            elif args == '-a':
                return subprocess.check_output('ipconfig /all', shell=True).decode()
            elif args == '-e':
                return subprocess.check_output("""powershell -C "Resolve-DNSName -Name "'myip.opendns.com'" -server "'resolver1.opendns.com'" | select IPAdress" ^| findstr "\."'' """, shell=True).decode()
            else:
                return str('unrecognized argument : ' + cmd_in.split(' ', 1)[1])
        elif cmd == 'name':
            return gethostname()
        elif cmd == 'ram':
            memory = psutil.virtual_memory()
            if len(str(memory[0])) >= 9:
                memory_total = str(round(memory[0]/1000000000,2)) + 'GB'
            elif len(memory) >= 6:
                memory_total = str(round(memory[0]/1000000,2)) + 'MB'
            else:
                memory_total = str(round(memory[0]/1000,2)) + 'KB'
            output = 'Total Memory: ' + memory_total + '\r\n'
            if len(str(memory[3])) >= 9:
                memory_used = str(round(memory[3]/1000000000,2)) + 'GB'
            elif len(memory) >= 6:
                memory_used = str(round(memory[3]/1000000,2)) + 'MB'
            else:
                memory_used = str(round(memory[3]/1000,2)) + 'KB'
            output += 'Used Memory: ' + memory_used + '\r\n'
            if len(str(memory[1])) >= 9:
                memory_available = str(round(memory[1]/1000000000,2)) + 'GB'
            elif len(memory) >= 6:
                memory_available = str(round(memory[1]/1000000,2)) + 'MB'
            else:
                memory_available = str(round(memory[1]/1000,2)) + 'KB'
            output += 'Available Memory: ' + memory_available
            return output
        elif cmd == 'cpu':
            stdout = 'CPU: ' + str(platform.processor()) + '\r\nUSAGE: ' + str(psutil.cpu_percent()) + '%'
            return stdout
        elif cmd == 'disconnect' or cmd == 'exit' or cmd == 'quit' or cmd == 'leave':
            return 'closing socket'
        elif cmd == 'kill':
            if args is None:
                return 'closing socket'
            else:
                return subprocess.check_output('taskkill /F /IM ' + args +  ' /T', shell=True).decode()
        elif cmd == 'reset':
            return 'resetting'
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
                    string = f'Showing all logs:\r\n'
                else:
                    string = f'Showing {i} of the last logs:\r\n'
                for line in lines[len(lines)-i:len(lines)]:
                    string += line
            return string
        elif cmd == 'help':
            commands = """Available commands:
DISCONNECT,LEAVE,QUIT,EXIT - close client connection
RESET - reset server
KILL - closes server OR task. KILL [taskname]
OS - displays operating system name
NAME - displays machine name
RAM - displays total and available memory
CPU - displays CPU percentage
LOGS [number] or [clear] - displays server logs
IP [-a] - Displays machine IP information
PING <destination> - ping a destination address
CLEAR - clears terminal
RENAME <name> - renames client
DOS:<msdos command> - Execute DOS commands
POWERSHELL:<powershell command> - Execute Powershell command"""
            return commands
        elif cmd == 'ping':
            ip = args
            return subprocess.check_output('ping ' + ip, shell=True).decode()
        elif cmd[0:4] == 'dos:':
            command = cmd_in.split(':',1)[1]
            output = subprocess.check_output(command, shell=True).decode()
            if len(output) == 0:
                output = 'success'
            return output
        elif cmd[0:11] == 'powershell:':
            command = cmd_in.split(':',1)[1]
            output = subprocess.check_output('powershell -command "' + command + '"', shell=True).decode()
            if len(output) == 0:
                output = 'success'
            return output
        elif cmd[0:6] == 'linux:':
            return 'This is a windows machine, try using "dos:" instead'
        else:
            return 'Command not found. Type help for a list of available commands'
    except:
        return 'Error when executing command: ' + cmd_in



def linux_command(cmd_in:str) -> str:
    try:
        cmd = cmd_in.lower()
        if len(cmd.split(' ')) > 1:
            cmd = cmd.split(' ')[0]
            args = cmd_in.split(' ', 1)[1].lower()
        else:
            args = None
        if cmd == 'os':
            return subprocess.check_output('cat /etc/os-release', shell=True).decode()
        elif cmd == 'ip':
            if args is None:
                return subprocess.check_output('ip', shell=True).decode()
            elif args == '-a':
                return subprocess.check_output('ip a', shell=True).decode()
            else:
                return 'Unknown argument ' + args
        elif cmd == 'ping':
            if args is None:
                return 'Failed to ping. Must specify address'
            else:
                return subprocess.check_output('ping -c 4' + args, shell=True).decode()
        elif cmd[0:6] == 'linux:':
            command = cmd_in.split(':',1)[1]
            return subprocess.check_output(command, shell=True).decode()
    except:
        return 'Failed to execute command: ' + cmd_in


def cmd_run(connection, cmd:str) -> None:
    if sys.platform == "linux" or sys.platform == "linux2":
        data = linux_command(cmd).encode()
    elif sys.platform == "darwin":
        print("NOT DONE YET") #MACOS
    elif sys.platform == "win32":
        data = windows_command(cmd).encode()
    connection.send(data)
    if cmd == 'disconnect' or cmd == 'kill' or cmd == 'exit' or cmd == 'quit' or cmd == 'leave' or cmd == 'reset':
        connection.close()
    sys.exit()
