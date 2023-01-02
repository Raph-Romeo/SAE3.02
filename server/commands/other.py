import subprocess


def other(client, cmd, cmd_split, data, args):
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
    elif cmd[0:5] == 'exec:':
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
    ## NEW COMMAND:
    #elif cmd == 'NEW COMMAND':
    #   do_something()
    else:
        client.send('Command not found. Type help for a list of available commands')
