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
            return 'Operating System: Windows 10'
        elif cmd == 'ip':
            if args is None:
                return str(subprocess.check_output('ipconfig', shell=True)).replace('\\r\\n','\n').split("'",1)[1].split("'",1)[0]
            elif args == '-a':
                return str(subprocess.check_output('ipconfig /all', shell=True)).replace('\\r\\n','\n').split("'",1)[1].split("'",1)[0]
            else:
                return str('unrecognized argument : ' + cmd_in.split(' ', 1)[1])
        elif cmd == 'name':
            return 'Machine name: ' + gethostname()
        elif cmd == 'ram':
            stdout = str(subprocess.check_output("wmic computersystem get totalphysicalmemory", shell=True)).replace('\\r\\n','').replace('\\r','')
            memory = stdout.split(' ')[2]
            if len(memory) >= 9:
                memory = str(round(int(memory)/1000000000,2)) + 'GB'
            elif len(memory) >= 6:
                memory = str(round(int(memory)/1000000,2)) + 'MB'
            else:
                memory = str(round(int(memory)/1000,2)) + 'KB'
            available = str(subprocess.check_output('systeminfo |find "Available Physical Memory"', shell=True)).replace(',',' ')
            return 'Total memory: ' + memory + '\n' + available.replace("b'", "").replace("\\r\\n'", "")
        elif cmd == 'cpu':
            powershell = "Powershell \"Get-Counter '\Processor(*)\% Processor Time' | Select -Expand Countersamples | Select InstanceName, CookedValue\""
            stdout = str(subprocess.check_output(powershell, shell=True)).replace('\\r\\n','').replace("'"," ")
            percent = str(round(float(stdout.split(' ')[len(stdout.split(' ')) - 2]),2))
            stdout = f"CPU USAGE: {percent}%"
            return stdout
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
            commands = ['disconnect,leave,quit,exit','reset','kill','os','cpu','ip (-a for more details)','name','RAM','CPU','IP','ping <destination>','DOS:<system command>','powershell:<powershell command>']
            string = ''
            for i in commands:
                string += i + '\n'
            return 'List of commands:\n' + string
        elif cmd == 'ping':
            ip = args
            return str(subprocess.check_output('ping ' + ip, shell=True)).replace('\\r\\n','\n').split("'",1)[1].split("'",1)[0]
        elif cmd[0:4] == 'dos:':
            command = cmd_in.split(':',1)[1]
            return str(subprocess.check_output(command, shell=True)).replace('\\r\\n','\n').split("'",1)[1].split("'",1)[0]
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
