# Server Tkinter and Create EXE files
from tkinter import *
import socket
from tkinter import messagebox
from TcpServer import TcpServer
from threading import Thread, Event

# Create Window
root = Tk()
root.title("Socket Connector")
root.geometry("300x100") 
root.resizable(width=False, height=False)
'''
Add Icon
root.iconbitmap('')
'''

ipInputLabel = Label(root, text = 'IP:', padx = 5)
ipInputLabel.grid(row = 0, column = 0, sticky = W)
ipInputEntry = Entry(root, width = 15)
ipInputEntry.insert(END, socket.gethostbyname(socket.gethostname()))
ipInputEntry.grid(row = 0, column = 1)
portInputLabel = Label(root, text = 'Port:', padx = 5)
portInputLabel.grid(row = 1, column = 0 , sticky = W)
portInputEntry = Entry(root, width = 15)
portInputEntry.grid(row = 1, column = 1)

connectionStatus = 'Disconnected'
statusLabel = Label(root, text = connectionStatus, bd = 1, relief = SUNKEN, anchor = W)
statusLabel.grid(row = 3, column = 0, columnspan = 4, sticky=W+E)

severThread = None
stopseverThread = Event()

def socketOpenFunc():
    
    global connectionStatus
    ipInput = ipInputEntry.get()
    portInput = portInputEntry.get()
    if (ipInput == '') or (portInput == ''):
        # Need to have a Pop-Up if the Input is not valid
        messagebox.showwarning("Warning", 'Please Enter IP and Port')
        return
    else:
        try:
            portInput = int(portInput)
        except ValueError:
            messagebox.showwarning("Warning", 'Invalid Port Entry')
            return

    if connectionStatus == 'Disconnected':
        
        global tcp
        tcp = TcpServer(ip = ipInput, port = portInput)
        tcp.openSocket()
        connectionStatus = 'Connected'
        statusLabel = Label(root, text = connectionStatus, bd = 1, relief = SUNKEN, anchor = W)
        statusLabel.grid(row = 3, column = 0, columnspan = 4, sticky=W+E)
        ipInputEntry.config(state='disabled')
        portInputEntry.config(state='disabled')

        # Runtime Error, need to test tcpserver object
        tcp.tcpServer()
    else:
        messagebox.showwarning("Warning", 'Already Connected')
        return

def disconnectClick():
    
    global connectionStatus
    global tcp
    global socketCommThread
    if connectionStatus == 'Connected':
        tcp.runButton = False
        tcp.closeSocket()
        connectionStatus = 'Disconnected'
        statusLabel = Label(root, text = connectionStatus, bd = 1, relief = SUNKEN, anchor = W)
        statusLabel.grid(row = 3, column = 0, columnspan = 4, sticky=W+E)
        ipInputEntry.config(state='normal')
        portInputEntry.config(state='normal')
    else:
        return


def clearButtonClick():

    ipInputEntry.delete(0, END)
    portInputEntry.delete(0, END)

def defaultIpClick():

    ipInputEntry.delete(0, END)
    ipInputEntry.insert(END, socket.gethostbyname(socket.gethostname()))

def socketCommThreadClick():

    global socketCommThread
    socketCommThread = Thread(target=socketOpenFunc)
    socketCommThread.daemon = True
    socketCommThread.start()

socketSetupButton = Button(root, text = 'Connect', command = socketCommThreadClick)
socketSetupButton.grid(row = 2, column = 2)

clearButton = Button(root, text = 'Clear', padx = 20, command = clearButtonClick)
clearButton.grid(row = 2, column = 1)

defaultIpButton = Button(root, text = 'Default',  command = defaultIpClick)
defaultIpButton.grid(row = 0, column = 2)

quitButton = Button(root, text = 'Disconnect', command = disconnectClick)
quitButton.grid(row = 2, column = 3)


# Event Loop
root.mainloop()