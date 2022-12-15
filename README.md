# SAE3.02 Self-monitoring Application
I chose to name my application SUPERSHELL

## WHAT IS A SUPERSHELL SERVER?

A supershell server is a script that will be running on the machine you wish to monitor.  
There is no user interface.  
Once it is running, it will be waiting for client connections.  
The server will do nothing until a client has connected to it.  
The server can accept multiple clients simultaneously.  
This server can run on any operating system (Tested on: Linux Debian, MacOs, Windows 10).

## WHAT IS A SUPERSHELL CLIENT?

A supershell client is a python application with a graphical interface (PyQT).  
It will allow you to connect to a supershell server.  
The application holds a database of servers filled by the user for quick connection.  
The client can perform basic commands to receive information on the system running the server, for example, a client can view the CPU usage, the RAM usage, and more.  
A client will also be able to execute all system commands.  

##

### To get started,
You must download and extract all the files available on this GITHUB.  
Get the required packages:

**Requirements (for Client):**
> Python version: 3.10 or newer
```
  pip install PyQt5==5.15.7
  pip install PyQt5-Qt5==5.15.2
  pip install PyQt5-sip==12.11.0
  pip install pyqtgraph==0.13.1
```
**Requirements (for Server):**
> Python version: 3.10 or newer
```
  pip install psutil==5.9.4
```

## SETTING UP A SUPERSHELL SERVER

To set up a server, you will need the following files/folders in the same directory:
```
server.py
commands <DIR>
```

Open a terminal on your machine, and run the **server.py** file with the following argument:
```
python server.py <PORT NUMBER>
```
Specify the port on which you want the server to run.  
For example, if you want your server to run on the port 3000, run the following command:
```
python server.py 3000
```
If the command line shows: **Started server**, then server was successfully started.  
  
The server will automatically create a logs.txt file containing all of the commands sent from the client connection as well as the IP address of every connection.
#### If an error occurs,
- Make sure that the port you chose is not already in use by some other application.
- Make sure that the python process has enough permission to write files (Necessary when writing server logs).

### Authenticated server :

You can set up an authenticated connection by running the script with option ‘-p’:
```
python server.py <PORT NUMBER> -p <PASSWORD>
```
That's all!

## SETTING UP A SUPERSHELL CLIENT

To run the client application, you will need the following files/folders in the same directory:
```
client.py
assets <DIR>
```
Open a terminal on your machine and run the **client.py** script with python:
```
python client.py
```

A CSV file will automatically be created on startup (if inexistant) : _ip-list.csv_  
If you wish to change the name of this file on startup you may execute the **client.py** file with the following argument:
```
python client.py <FILE PATH>
```
or you may select a different file later from within the application.  
### What is the CSV File for?
This csv file will allow the user to store a list of his server IPs and PORTs so he can easily connect to them without having to type them in manually every time.
#### Here's how you format the CSV file:
```
name,ip:port
name,ip:port
```
Please note:
- The IP can also be a domain name.
- The name of the server is only a reference for the client, you may put which ever name you want. It can include any UTF-8 character except for commas '**,**' .

Your client has been successfully set up!

## SUPERSHELL CLIENT GUIDE
Please view documents/user guide.pdf
## FOR MORE TECHNICAL DETAILS
Please view documents/technical document.pdf
