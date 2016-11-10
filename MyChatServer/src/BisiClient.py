import socket
import time

# QUESTO PRIMA SI FA LO USER1 INVIANDOGLI ROBA SUL SERVER TEMP, POI FA LA STAMPA CON GLI ASTERISCHI PER LO USER2

serverName = 'localhost'
serverPort = 9182

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
#          user  pass   new     new     new     new     msg0    msg1
# expected = 'OK\r\n'
#                                                                                                               OK 0\r\n                                   OK 1\r\n                                               OK 2\r\n                     OK 3\r\n                      OK 4\r\n                      OK 5\r\n                       OK 6\r\n                     MESSAGES\r\n0 0 1 2 3\r\n2 0 1 2 3\r\n4 0 1 2 3\r\n5 0 1 2 3\r\n6 0 1 2 3\r\n\r\n
clientSocket.send("USER user1\r\nPASS pass1\r\nNEW Topic0\r\nNEW Topic1\r\nNEW Topic2\r\nNEW Topic3\r\nNEW Topic4\r\nREGISTER localhost 1984\r\nSUBSCRIBE 0 1 2 3 4\r\nDIGEST 2\r\nMESSAGE 0 1\r\nBau!\r\n.\r\n\r\nMESSAGE 2 3\r\nMiao!\r\n.\r\n\r\nMESSAGE 4 0\r\nCiao!\r\n.\r\n\r\nDIGEST 4\r\nMESSAGE 0 1 2 3 4\r\nSonno!\r\n.\r\n\r\nREPLY 0\r\nreply!\r\n.\r\n\r\nDIGEST 0\r\nREPLY 2\r\nBene!\r\n.\r\n\r\n")
# time.sleep(0.1)
# actual = clientSocket.recv(2048)
# print actual == expected
# print "Atteso:\n",expected
# print "Ottenuto:\n",actual
# print len(actual), len(expected)
# print "Connessione col Server chiusa."
clientSocket.close()
# ###################################################################################################
# #
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

clientSocket.send("USER user2\r\nPASS pass2\r\nNEW Topic5\r\nNEW Topic6\r\nNEW Topic7\r\nNEW Topic8\r\nNEW Topic9\r\nREGISTER localhost 1985\r\nSUBSCRIBE 0 2 4 6 8\r\nTOPICS\r\n")
time.sleep(0.1)
result = clientSocket.recv(1024)
print result
clientSocket.close()
# print clientSocket.recv(4)
# print clientSocket.recv(4)
# print clientSocket.recv(7)
# print clientSocket.recv(7)
# print clientSocket.recv(7)
# print clientSocket.recv(7)
# print clientSocket.recv(7)
# print clientSocket.recv(4)
# print clientSocket.recv(4)
# print clientSocket.recv(1024)
clientSocket.close()
