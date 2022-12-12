import sys
import psutil
from socket import gethostname, gethostbyname
import subprocess
from commands.linux import linux
from commands.other import other
from commands.windows import windows
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
            windows(client, cmd, cmd_split, data, args)
        elif sys.platform == 'linux' or sys.platform == 'linux2':
            linux(client, cmd, cmd_split, data, args)
        else:
            other(client, cmd, cmd_split, data, args)
    sys.exit()


def cpu_percent():
    return psutil.cpu_percent()


def ram_percent():
    return psutil.virtual_memory()[2]
