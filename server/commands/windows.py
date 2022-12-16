import subprocess


def windows(client, cmd, cmd_split, data, args):
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
            process = subprocess.Popen(data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output = process.stdout.read()
            if len(output) == 0:
                output = process.stderr.read()
            try:
                output.decode('utf-8')
            except:
                output.decode('cp850')
        else:
            output = 'Usage : ping <DESTINATION>'
        client.send(output)
    elif cmd == 'kill':
        if args:
            output = subprocess.check_output('taskkill /F /IM ' + cmd_split[1] + ' /T', shell=True)
            try:
                output.decode('utf-8')
            except:
                output.decode('cp850')
            client.send(output)
    elif cmd[0:4] == 'dos:':
        command = data.split(':', 1)[1]
        if len(command) == 0:
            client.send('Usage : dos:<COMMAND>')
            return
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output = process.stdout.read()
        if len(output) == 0:
            output = process.stderr.read()
        try:
            output = output.decode('utf-8')
        except:
            output = output.decode('cp850')
        if len(output) == 0:
            output = 'success'
        client.send(output)
    elif cmd[0:11] == 'powershell:':
        command = data.split(':', 1)[1]
        if len(command) == 0:
            client.send('Usage : powershell:<COMMAND>')
            return
        process = subprocess.Popen('powershell -command "' + command + '"', stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   encoding='utf-8', shell=True)
        output = process.stdout.read()
        if len(output) == 0:
            output = process.stderr.read()
        try:
            output = output.decode('utf-8')
        except:
            output = output.decode('cp850')
        if len(output) == 0:
            output = 'success'
        client.send(output)
    elif cmd[0:6] == 'linux:' or cmd[0:6] == 'macos:':
        client.send('This is a windows machine, try using "dos:" instead')
    ## NEW COMMAND:
    #elif cmd == 'NEW COMMAND':
    #   do_something()
    else:
        client.send('Command not found. Type help for a list of available commands')