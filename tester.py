from TcpServer import TcpServer

tcp = TcpServer('192.168.0.20', 5005)
tcp.openSocket()
tcp.tcpServer()