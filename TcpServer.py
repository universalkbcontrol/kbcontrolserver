import socket
import select
from keyInput import keyOperation
from lua import luaGenerator
import msvcrt
import time
import os

class TcpServer():
    

    def __init__(self, ip, port):
        
        # Need to automatic detects the IP address
        self.connectionExist = False
        self.ip = ip
        self.port = port
        self.host = socket.gethostname()
        self.headerSize = 10
        self.clients = {}
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket = server_socket
        self.sockets_list = [server_socket]
        self.runButton = True
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def openSocket(self):
        
        if ~self.connectionExist:
            try:
                self.server_socket.bind((self.ip, self.port))
                self.server_socket.listen()
                self.connectionExist = True
                print (f"Server Established, {self.ip}: {str(self.port)}")
            
            except ValueError:
                print (f"Connection Failure! Please Check {self.ip}: {str(self.port)}")
    

    def closeSocket(self):
        
        if self.connectionExist:
            for clientSocket in self.sockets_list:
                if clientSocket != self.server_socket:
                    user = self.clients[clientSocket]
                    disconnection_message = f'Disconnection from: {user["data"].decode("utf-8")}.'
                    print (disconnection_message)
                    disconnection_message_send = f'Disconnection with {self.host}'
                    disconnection_message_send = f'{len(disconnection_message_send):<{self.headerSize}}' + disconnection_message_send
                    clientSocket.send(bytes(disconnection_message_send, "utf-8"))
                    #clientSocket.shutdown(how=socket.SHUT_RDWR)
                    clientSocket.close()
            self.connectionExist = False
            #os._exit(0)
            socket.socket(socket.AF_INET, 
                  socket.SOCK_STREAM).connect((self.ip, self.port))
            self.server_socket.close()
            print (f"Server Disconnected, {self.ip}: {str(self.port)}")                  

    
    def receive_message(self, client_socket):

        try:
            message_header = client_socket.recv(self.headerSize)
            if not len(message_header):
                return False
            message_length = int(message_header.decode('utf-8').strip())
            data = b''  # recv() does return bytes
            while len(data) < message_length:
                chunk = client_socket.recv(message_length)  # some 2^n number
                data += chunk

            return {'header': message_header, 'data': data}

        except:
            return False
    

    def keyCommand(self, message):

        keySeparator = '$and$'

        if keySeparator in message:
            command = message.split(keySeparator)
        else:
            command = message

        keyOperation(command)

    
    def createLua(self, message):

        keyLua = "luafile"

        splitlua = message.split(keyLua)

        luaGenerator(splitlua[0], splitlua[1])

    
    def tcpServer(self):

        if self.connectionExist:
            
            while self.runButton:

                read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list, 0.5)
                
                if not (read_sockets or exception_sockets):
                    if self.runButton:
                        continue 
                    else:
                        return

                # Iterate over notified sockets
                for notified_socket in read_sockets:

                    # If notified socket is a server socket - new connection, accept it
                    if notified_socket == self.server_socket:

                        # Accept new connection
                        client_socket, client_address = self.server_socket.accept()
                        
                        # Client should send his name right away, receive it
                        user = self.receive_message(client_socket)

                        # If False - client disconnected before he sent his name
                        if user is False:
                            continue

                        # Add accepted socket to select.select() list
                        self.sockets_list.append(client_socket)

                        # Also save username and username header
                        self.clients[client_socket] = user

                        connection_message = f'Open connection from: {user["data"].decode("utf-8")}.'
                        print (connection_message)
                        connection_message_send = f'Connection Established with {self.host}'
                        connection_message_send = f'{len(connection_message_send):<{self.headerSize}}' + connection_message_send
                        client_socket.send(bytes(connection_message_send, "utf-8"))

                    # Else existing socket is sending a message
                    else:

                        # Receive message
                        message = self.receive_message(notified_socket)

                        # If False, client disconnected, cleanup
                        if message is False:
                            print('Closed connection from: {}'.format(self.clients[notified_socket]['data'].decode('utf-8')))

                            # Remove from list for socket.socket()
                            self.sockets_list.remove(notified_socket)

                            # Remove from our list of users
                            del self.clients[notified_socket]

                            continue

                        # Get user by notified socket, so we will know who sent the message
                        user = self.clients[notified_socket]

                        print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
                        receivedCommand = message["data"].decode("utf-8")
                        if "luafile" in receivedCommand:
                            self.createLua(receivedCommand)
                        else:
                            self.keyCommand(receivedCommand)


                # It's not really necessary to have this, but will handle some socket exceptions just in case
                for notified_socket in exception_sockets:

                    # Remove from list for socket.socket()
                    self.sockets_list.remove(notified_socket)

                    # Remove from our list of users
                    del self.clients[notified_socket]
            
        else:
            print (f"Connection is not Open!")

