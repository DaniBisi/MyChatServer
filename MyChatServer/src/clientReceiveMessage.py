import socket

serverSocket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(("127.0.0.1", 4127))
serverSocket.listen(10)
connectionSocket, addr = serverSocket.accept()
data = connectionSocket.recv(2048)
print data
connectionSocket.close()
