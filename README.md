# SAE3.02 Self-monitoring Application

**WHAT IS A SUPERSHELL SERVER?  ─────────────────────────────**

A supershell server is a script that will be running on the machine you wish to monitor.
There is no user interface.
Once it is running, it will be waiting for client connections.
The server will do nothing until a client has connected to it.
The server can accept multiple clients simultaneously.
This server can run on any operating system (Tested on: Linux Debian, MacOs, Windows 10).

**WHAT IS A SUPERSHELL CLIENT?  ─────────────────────────────**

A supershell client is a python application with a graphical interface (PyQT).
It will allow you to connect to a supershell server.
The application holds a database of servers filled by the user for quick connection.
The client can perform basic commands to receive information on the system running the server, for example, a client can view the CPU usage, the RAM usage, and more.
A client will also be able to execute all system commands.

**────────────────────────────────────────────────────────**

### To get started,
You must download and extract all the files available on this GITHUB.
Get the required packages:

**Requirements (for Client):**
Python version: 3.10 or newer
PIP PACKAGES:
  PyQt5==5.15.7
  PyQt5-Qt5==5.15.2
  PyQt5-sip==12.11.0
  pyqtgraph==0.13.1

**Requirements (for Server):**
Python version: 3.10 or newer
PIP PACKAGES:
  psutil==5.9.4

