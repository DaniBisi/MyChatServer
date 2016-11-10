import socket
import time

serverName = 'localhost'
serverPort = 102

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
#          user  pass   new     new     new     new     msg0    msg1
expected = 'OK\r\nOK\r\nOK 0\r\nOK 1\r\nOK 2\r\nOK 3\r\nOK 0\r\nOK 1\r\nMESSAGES\r\n0 0 1 2 3\r\n\r\nMESSAGE 1\r\nTOPICS 0 1 3\r\nBau!\r\n.\r\n\r\nOK 2\r\nOK 3\r\nOK 4\r\nOK 5\r\nOK 6\r\nMESSAGES\r\n0 0 1 2 3\r\n2 0 1 2 3\r\n4 0 1 2 3\r\n5 0 1 2 3\r\n6 0 1 2 3\r\n\r\nOK\r\n'
#                                                                                                               OK 0\r\n                                   OK 1\r\n                                               OK 2\r\n                     OK 3\r\n                      OK 4\r\n                      OK 5\r\n                       OK 6\r\n                     MESSAGES\r\n0 0 1 2 3\r\n2 0 1 2 3\r\n4 0 1 2 3\r\n5 0 1 2 3\r\n6 0 1 2 3\r\n\r\n
clientSocket.send("USER user1\r\nPASS pass1\r\nNEW Titolo0\r\nNEW Titolo1\r\nNEW Titolo2\r\nNEW Titolo3\r\nMESSAGE 0 1 2 3\r\nCiao! Come stai?\r\n.\r\n\r\nMESSAGE 0 1 3\r\nBau!\r\n.\r\n\r\nLIST 0 2\r\nGET 1\r\nREPLY 0\r\nMiao!\r\n.\r\n\r\nREPLY 0\r\nBene!\r\n.\r\n\r\nREPLY 2\r\nBenone!\r\n.\r\n\r\nREPLY 2\r\nBenone!\r\n.\r\n\r\nREPLY 5\r\nBenone!\r\n.\r\n\r\nCONV 2\r\nREGISTER localhost 1982\r\n")
time.sleep(0.9)
actual = clientSocket.recv(2048)
print actual == expected
print "Atteso:\n",expected
print "Ottenuto:\n",actual
print len(actual), len(expected)
print "Connessione col Server chiusa."
clientSocket.close()
###################################################################################################
print '\n'
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
expected = 'OK\r\nOK\r\nKO\r\nOK\r\n'
clientSocket.send("USER user2\r\nPASS pass2\r\nREGISTER localhost 1982\r\nREGISTER localhost 1983\r\n")
time.sleep(0.1)
actual = clientSocket.recv(2048)
print actual == expected
# print "Atteso:\n",expected
# print "Ottenuto:\n",actual
print len(actual), len(expected)
print "Connessione col Server chiusa."
clientSocket.close()

print '\n'
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
expected = 'OK\r\nOK\r\nKO\r\nKO\r\nOK\r\n'
clientSocket.send("USER user3\r\nPASS pass3\r\nREGISTER localhost 1982\r\nREGISTER localhost 1983\r\nREGISTER localhost 1984\r\n")
time.sleep(0.1)
actual = clientSocket.recv(2048)
print actual == expected
# print "Atteso:\n",expected
# print "Ottenuto:\n",actual
print len(actual), len(expected)
print "Connessione col Server chiusa."
clientSocket.close()

print '\n'
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
expected = 'OK\r\nOK\r\nOK\r\n'
clientSocket.send("USER user2\r\nPASS pass2\r\nUNREGISTER\r\n")
time.sleep(0.1)
actual = clientSocket.recv(2048)
print actual == expected
# print "Atteso:\n",expected
# print "Ottenuto:\n",actual
print len(actual), len(expected)
print "Connessione col Server chiusa."
clientSocket.close()

print '\n'
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
expected = 'KO\r\nKO\r\nOK\r\nKO\r\nKO\r\nKO\r\nKO\r\nOK\r\nOK\r\nOK\r\n'
clientSocket.send("PASS pass1\r\nPASS pass2\r\nUSER user1\r\nUNREGISTER\r\nPASS pass2\r\nUNREGISTER\r\nNIENTE 1 2 3 4\r\nUSER user1\r\nPASS pass1\r\nUNREGISTER\r\n")
#                      KO\r\n        KO\r\n      OK\r\n          KO\r\n       KO\r\n         KO\r\n         KO\r\n           OK\r\n     OK\r\n       OK\r\n
time.sleep(0.1)
actual = clientSocket.recv(2048)
print actual == expected
# print "Atteso:\n",expected
# print "Ottenuto:\n",actual
print len(actual), len(expected)
print "Connessione col Server chiusa."
clientSocket.close()


# time.sleep(5)

print '\n'
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
expected = 'OK\r\nOK\r\nTOPIC_LIST\r\n0 Titolo0\r\n1 Titolo1\r\n2 Titolo2\r\n3 Titolo3\r\n\r\nOK\r\nKO\r\nOK\r\nOK 7\r\nOK 8\r\nKO\r\nOK\r\nOK\r\n'
clientSocket.send("USER user3\r\nPASS pass3\r\nTOPICS\r\nSUBSCRIBE 0 1 2 3\r\nUNSUBSCRIBE 0 3 5\r\nUNSUBSCRIBE 0 3\r\nMESSAGE 0 1 3\r\nArriva la notifica?\r\n.\r\n\r\nREPLY 0\r\nSperiamo!\r\n.\r\n\r\nDIGEST -1\r\nDIGEST 2\r\nDIGEST 0\r\n")
#                      OK\r\n        OK\r\n      OK\r\n          KO\r\n       KO\r\n         KO\r\n         KO\r\n           OK\r\n     OK\r\n       OK\r\n

time.sleep(21)
actual = clientSocket.recv(2048)
print actual == expected
print "Atteso:\n",expected
print "Ottenuto:\n",actual
print len(actual), len(expected)
print "Connessione col Server chiusa."
clientSocket.close()


