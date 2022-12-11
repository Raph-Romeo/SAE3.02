import sys
import psutil
from socket import gethostname, gethostbyname
import subprocess
import platform


def execute(client, data):
    cmd_split = data.lower().split(' ')
    cmd = cmd_split[0]
    if len(cmd_split) > 1:
        args = True
    else:
        args = False
    if cmd == 'cpu':
        client.send('CPU: ' + str(platform.processor()) + '\r\nUSAGE: ' + str(psutil.cpu_percent()) + '%')
    elif cmd == 'ram':
        memory = psutil.virtual_memory()
        if len(str(memory[0])) >= 9:
            memory_total = str(round(memory[0] / 1000000000, 2)) + 'GB'
        elif len(memory) >= 6:
            memory_total = str(round(memory[0] / 1000000, 2)) + 'MB'
        else:
            memory_total = str(round(memory[0] / 1000, 2)) + 'KB'
        output = 'Total Memory: ' + memory_total + '\r\n'
        if len(str(memory[3])) >= 9:
            memory_used = str(round(memory[3] / 1000000000, 2)) + 'GB'
        elif len(memory) >= 6:
            memory_used = str(round(memory[3] / 1000000, 2)) + 'MB'
        else:
            memory_used = str(round(memory[3] / 1000, 2)) + 'KB'
        output += 'Used Memory: ' + memory_used + '\r\n'
        if len(str(memory[1])) >= 9:
            memory_available = str(round(memory[1] / 1000000000, 2)) + 'GB'
        elif len(memory) >= 6:
            memory_available = str(round(memory[1] / 1000000, 2)) + 'MB'
        else:
            memory_available = str(round(memory[1] / 1000, 2)) + 'KB'
        output += 'Available Memory: ' + memory_available
        client.send(output)
    elif cmd == 'ip':
        client.send(gethostbyname(gethostname()))
    elif cmd == 'name':
        client.send(gethostname())
    elif cmd == 'os':
        if not args:
            client.send(platform.system() + ' ' + platform.release())
        else:
            if data == 'os -a':
                client.send(platform.platform())
            else:
                client.send('os - unrecognized argument')
    elif cmd == 'logs':
        if not args:
            num = 25
        elif cmd_split[1].isdigit():
            num = int(cmd_split[1])
            if num < 1:
                client.send('logs - value must be over 0')
                return
        elif cmd_split[1] == 'clear':
            with open('logs.txt', 'w') as file:
                file.write('')
            client.send('server logs are cleared')
            return
        else:
            client.send('logs - unrecognized argument')
            return
        with open('logs.txt', 'r') as file:
            lines = file.readlines()
            if num > len(lines):
                num = len(lines)
                string = f'Showing all logs:\r\n'
            else:
                string = f'Showing {num} of the last logs:\r\n'
            for line in lines[len(lines) - num:len(lines)]:
                string += line
            if len(string) > 0:
                string = string[0:len(string)-1]
        client.send(string)
    else:
        if sys.platform == 'win32':
            if cmd == 'help':
                commands = """AVAILABLE COMMANDS:
    DISCONNECT,LEAVE,QUIT,EXIT - disconnect
    RESET - reset server
    KILL - closes server OR task. KILL [taskname]
    OS - displays info on operating system (use -a for more details)
    NAME - displays machine name
    RAM - displays total,used and available memory
    CPU - displays CPU percentage
    LOGS [number] or [clear] - displays server logs
    IP - Displays machine local IP
    PING <destination> - ping a destination address
    CLEAR - clears terminal
    RENAME <name> - renames client
    DOS:<msdos command> - Execute DOS commands
    POWERSHELL:<powershell command> - Execute Powershell command"""
                client.send(commands)
            elif cmd == 'ping':
                if args:
                    client.send('Trying to ping at ' + data.split(' ', 1)[1] + '...')
                    process = subprocess.Popen(data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', shell=True)
                    output = process.stdout.read()
                    if len(output) == 0:
                        output = process.stderr.read()
                else:
                    output = 'Usage : ping <DESTINATION>'
                client.send(output)
            elif cmd == 'kill':
                if args:
                    output = subprocess.check_output('taskkill /F /IM ' + cmd_split[1] + ' /T', shell=True).decode()
                    client.send(output)
            elif cmd[0:4] == 'dos:':
                command = data.split(':', 1)[1]
                if len(command) == 0:
                    client.send('Usage : dos:<COMMAND>')
                    return
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', shell=True)
                output = process.stdout.read()
                if len(output) == 0:
                    output = process.stderr.read()
                if len(output) == 0:
                    output = 'success'
                client.send(output)
            elif cmd[0:11] == 'powershell:':
                command = data.split(':', 1)[1]
                if len(command) == 0:
                    client.send('Usage : powershell:<COMMAND>')
                    return
                process = subprocess.Popen('powershell -command "' + command + '"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', shell=True)
                output = process.stdout.read()
                if len(output) == 0:
                    output = process.stderr.read()
                if len(output) == 0:
                    output = 'success'
                client.send(output)
            elif cmd[0:6] == 'linux:' or cmd[0:6] == 'macos:':
                client.send('This is a windows machine, try using "dos:" instead')
            else:
                client.send('Command not found. Type help for a list of available commands')
        elif sys.platform == 'linux' or sys.platform == 'linux2':
            if cmd == 'help':
                commands = """AVAILABLE COMMANDS:
    DISCONNECT,LEAVE,QUIT,EXIT - disconnect
    RESET - reset server
    KILL - closes server
    OS - displays info on operating system (use -a for more details)
    NAME - displays machine name
    RAM - displays total,used and available memory
    CPU - displays CPU percentage
    LOGS [number] or [clear] - displays server logs
    IP - Displays machine local IP
    PING <destination> - ping a destination address
    CLEAR - clears terminal
    RENAME <name> - renames client
    LINUX:<command> - Execute command on machine"""
                client.send(commands)
            elif cmd == 'ping':
                if args:
                    process = subprocess.Popen('ping -c 4 ' + cmd_split[1], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', shell=True)
                    output = process.stdout.read()
                    if len(output) == 0:
                        output = process.stderr.read()
                else:
                    output = 'Usage : ping <DESTINATION>'
                client.send(output)
            elif cmd[0:6] == 'linux:':
                command = data.split(':', 1)[1]
                if len(command) == 0:
                    client.send('Usage : linux:<COMMAND>')
                    return
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', shell=True)
                output = process.stdout.read()
                if len(output) == 0:
                    output = process.stderr.read()
                if len(output) == 0:
                    output = 'success'
                client.send(output)
            elif cmd[0:4] == 'dos:' or cmd[0:6] == 'macos:':
                client.send('This is a linux machine, try using "linux:" instead')
            else:
                client.send('Command not found. Type help for a list of available commands')
        else:
            if cmd == 'help':
                commands = """AVAILABLE COMMANDS:
    DISCONNECT,LEAVE,QUIT,EXIT - disconnect
    RESET - reset server
    KILL - closes server
    OS - displays info on operating system (use -a for more details)
    NAME - displays machine name
    RAM - displays total,used and available memory
    CPU - displays CPU percentage
    LOGS [number] or [clear] - displays server logs
    IP - Displays machine local IP
    CLEAR - clears terminal
    RENAME <name> - renames client
    EXEC:<command> - Execute command on this system"""
                client.send(commands)
            elif cmd == 'exec':
                command = data.split(':', 1)[1]
                if len(command) == 0:
                    client.send('Usage : exec:<COMMAND>')
                    return
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', shell=True)
                output = process.stdout.read()
                if len(output) == 0:
                    output = process.stderr.read()
                if len(output) == 0:
                    output = 'success'
                client.send(output)
            elif cmd[0:4] == 'dos:' or cmd[0:6] == 'macos:' or cmd[0:6] == 'linux:':
                client.send("try using 'exec:' instead")
            else:
                client.send('Command not found. Type help for a list of available commands')
    sys.exit()


def cpu_percent():
    return psutil.cpu_percent()


def ram_percent():
    return psutil.virtual_memory()[2]
