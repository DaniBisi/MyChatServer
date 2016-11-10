'''
Created on 07 nov 2016

@author: Daniele
'''


# ricordare che la class MyChatServer deve estendere Thread
# ricordare che si deve implementare and 
#  def run(self):
#         self.start1()  
#     def start1(self):
         
import unittest
from DanieleBisignano import *
#from UbaldoPuocci import *
from _socket import AF_INET, SOCK_STREAM
class Test(unittest.TestCase):
    address = "127.0.0.1"
    port = 1294
    Dizionario = {
    "Dani": "ciao",
    "user1": "pass1",
    "user2": "pass2",
    "user3": "pass3"}
#     def __init__(self):
#         unittest.TestCase.__init__(self)
#         print"inizio test"
    
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        #self.i = -1
    def setUp(self):
        unittest.TestCase.setUp(self)
        
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
    def TestUser(self):
        
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port)
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port))
        msg = "USER Dani"+'\r'+'\n'
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(4)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\n", "TestUser Non Funzionante")
        pass
    
    def TestUserPassOk(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+1)
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+1))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(4)
        data = data + self.clientSocket.recv(4)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\n", data)
        pass
    def testBatch(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+56)
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+56))
        msg = "USER Dani"+'\r'+'\n'+"PAS"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(4)
        msg = "S ciao"+'\r'+'\n'
        self.clientSocket.send(msg)
        data = data + self.clientSocket.recv(4)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\n", data)
        pass
    
    def TestUserPassNotOk(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+2)
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+2))
        msg = "USER Dani"+'\r'+'\n'+"PASS lol"+'\r'+'\n'
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(4)
        data = data + self.clientSocket.recv(4)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nKO\r\n", data)
        pass
    def TestUserPassNotOkMessage(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+3)
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+3))
        msg = "USER Dani"+'\r'+'\n'+"PASS lol"+'\r'+'\n'+"MESSAGE 1 4 lol"+'\r'+'\n'+"ASDGAKHSDFG"+'\r'+'\n'+'.'+'\r'+'\n'+'\r'+'\n'
        print msg
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(4)
        data = data + self.clientSocket.recv(4)
        data = data + self.clientSocket.recv(4)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nKO\r\nKO\r\n", data)
        pass
    def testLegalCommandNotLogin(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+4)
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+4))
        msg = "NEW CIAO"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(4)
        data = data + self.clientSocket.recv(4)
        self.clientSocket.close()
        self.assertEqual(data,"KO\r\nKO\r\n", data)
        pass
    def testNewTopic(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+5)
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+5))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(4)
        data = data + self.clientSocket.recv(4)
        data = data + self.clientSocket.recv(6)
        data = data + self.clientSocket.recv(6)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\n", data)
        pass
    def testTopicList(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+11)
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+11))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"TOPIC_LIST\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(4)
        data = data + self.clientSocket.recv(4)
        data = data + self.clientSocket.recv(6)
        data = data + self.clientSocket.recv(6)
        data = data + self.clientSocket.recv(32)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nTOPIC LIST\r\n0 CIAO\r\n1 ciao11\r\n\r\n", data)
        pass
    
    def testTopicListWrongSyntax(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+26)
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+26))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"TOPIC_LIST 1 3\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(4)
        data = data + self.clientSocket.recv(4)
        data = data + self.clientSocket.recv(6)
        data = data + self.clientSocket.recv(6)
        data = data + self.clientSocket.recv(4)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nKO\r\n", data)
        pass
    def testMessageNoTopic(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+6)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+6))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 2 1"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nKO\r\n", data)
        pass
    def testMessage(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+7)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+7))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"hello first msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nOK 0\r\n", data)
        pass
    def testPiuInserimenti(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+8)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+8))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"hello first msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nOK 0\r\nOK 1\r\n", data)
        pass
    def testListTopicValidPresent(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+14)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+14))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"hello first msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"LIST 0 1"+'\r'+'\n'
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nOK 0\r\nOK 1\r\nMESSAGES\r\n0 0 1\r\n\r\n", data)
        pass
    def testListTopicValidPresentMore(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+9)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+9))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"hello first msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"LIST 0 1 0"+'\r'+'\n'
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nOK 0\r\nOK 1\r\nMESSAGES\r\n0 0 1\r\n1 0\r\n\r\n", data)
        pass
    
    def testListTopicNotValidPresentMore(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+10)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+10))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"hello first msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"LIST 0 1 4"+'\r'+'\n'
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nOK 0\r\nOK 1\r\nKO\r\n", data)
        pass
    def testValidReply(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+13)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+13))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"hello first msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"LIST 0 1 6"+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hell first responce msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nOK 0\r\nOK 1\r\nKO\r\nOK 2\r\n", data)
        pass
    def testInValidReply(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+12)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+12))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"hello first msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"LIST 0 1 6"+'\r'+'\n'+"REPLY 6"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nOK 0\r\nOK 1\r\nKO\r\nKO\r\n", data)
        pass
    
    def testConv(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+15)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+15))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"hello first msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"LIST 0 1 6"+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 2"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"CONV 2\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nOK 0\r\nOK 1\r\nKO\r\nOK 2\r\nOK 3\r\nMESSAGES\r\n0 0 1\r\n2 0 1\r\n3 0 1\r\n\r\n", data)
        pass
    
    def testConvBase(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+16)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+16))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"hello first msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"LIST 0 1 6"+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 2"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"CONV 0\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nOK 0\r\nOK 1\r\nKO\r\nOK 2\r\nOK 3\r\nMESSAGES\r\n0 0 1\r\n2 0 1\r\n3 0 1\r\n\r\n", data)
        pass
    def testConvUltimo(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+17)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+17))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"MESSAGGIO 1"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"LIST 0 1 6"+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 2"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"CONV 3\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nOK 0\r\nOK 1\r\nKO\r\nOK 2\r\nOK 3\r\nMESSAGES\r\n0 0 1\r\n2 0 1\r\n3 0 1\r\n\r\n", data)
        pass
    def testConvMoreReplySameLevel(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+18)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+18))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"hello first msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"LIST 0 1 6"+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"CONV 0\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nOK 0\r\nOK 1\r\nKO\r\nOK 2\r\nOK 3\r\nMESSAGES\r\n0 0 1\r\n2 0 1\r\n3 0 1\r\n\r\n", data)
        pass
    
    
    def testGeneric(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+19)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+19))
        msg = "USER user1\r\nPASS pass1\r\nNEW Titolo0\r\nNEW Titolo1\r\nNEW Titolo2\r\nNEW Titolo3\r\nMESSAGE 0 1 2 3\r\nCiao! Come stai?\r\n.\r\n\r\nMESSAGE 0 1 3\r\nBau!\r\n.\r\n\r\nMESSAGE 0 2 3\r\nMiao!\r\n.\r\n\r\nLIST 0 2\r\nGET 2\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nOK 2\r\nOK 3\r\nOK 0\r\nOK 1\r\nOK 2\r\nMESSAGES\r\n0 0 1 2 3\r\n2 0 2 3\r\n\r\nMESSAGE 2\r\nTOPICS 0 2 3\r\nMiao!\r\n.\r\n\r\n", data)
        pass
    def testRegisterBase(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+20)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+20))
        msg = "USER user1\r\nPASS pass1\r\nREGISTER 127.0.0.1 89\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK\r\n", data)
    def testRegisterBusy(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+21)
        self.MyServer.beforeTest()
        self.MyServer.start()
        MyChatServer.registerHost["Dani"] = ("127.0.0.1" , 89)
        self.clientSocket.connect((self.address , self.port+21))
        msg = "USER user1\r\nPASS pass1\r\nREGISTER 127.0.0.1 89\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nKO\r\n", data)
    #msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"MESSAGGIO 1"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"MESSAGGIO 2"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"LIST 0 1 6"+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 3"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 2"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"CONV 3\r\n"
    
    def testRegisterBusyAndReplace(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+22)
        self.MyServer.beforeTest()
        self.MyServer.start()
        MyChatServer.registerHost["user1"] = ("127.0.0.1" , 89)
        self.clientSocket.connect((self.address , self.port+22))
        msg = "USER user1\r\nPASS pass1\r\nREGISTER 127.0.0.1 89\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK\r\n", data)
    #msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"MESSAGGIO 1"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"MESSAGGIO 2"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"LIST 0 1 6"+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 3"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 2"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"CONV 3\r\n"
    
    def testUnRegisterBase(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+23)
        self.MyServer.beforeTest()
        self.MyServer.start()
        MyChatServer.registerHost["user1"] = ("127.0.0.1" , 89)
        self.clientSocket.connect((self.address , self.port+23))
        msg = "USER user1\r\nPASS pass1\r\nUNREGISTER\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK\r\n", data)
    #msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"MESSAGGIO 1"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"MESSAGGIO 2"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"LIST 0 1 6"+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 3"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 2"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"CONV 3\r\n"
     
    def testUnRegisterNotRegistered(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+24)
        self.MyServer.beforeTest()
        self.MyServer.start()
        MyChatServer.registerHost["dani"] = ("127.0.0.1" , 89)
        self.clientSocket.connect((self.address , self.port+24))
        msg = "USER user1\r\nPASS pass1\r\nUNREGISTER\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nKO\r\n", data)
    #msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"MESSAGGIO 1"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"MESSAGGIO 2"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"LIST 0 1 6"+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 3"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 2"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"CONV 3\r\n"
    
    def testUnRegisterWrongSyntaxLegalDelete(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+25)
        self.MyServer.beforeTest()
        self.MyServer.start()
        MyChatServer.registerHost["user1"] = ("127.0.0.1" , 89)
        self.clientSocket.connect((self.address , self.port+25))
        msg = "USER user1\r\nPASS pass1\r\nUNREGISTER 3 4\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nKO\r\n", data)
    #msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"MESSAGGIO 1"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"MESSAGGIO 2"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"LIST 0 1 6"+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 3"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 2"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"CONV 3\r\n"
    
    def testConvMoreThanEnought(self):
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+41)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket.connect((self.address , self.port+41))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"MESSAGGIO 1"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"MESSAGGIO 2"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"LIST 0 1 6"+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 3"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 2"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"CONV 0\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        data = data + self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nOK 0\r\nOK 1\r\nKO\r\nOK 2\r\nOK 3\r\nMESSAGES\r\n0 0 1\r\n2 0 1\r\n3 0 1\r\n", data)
        pass
    def testMultiUser(self):
        self.clientSocket = []
        self.clientSocket.append(socket.socket(AF_INET,SOCK_STREAM))
        self.clientSocket.append(socket.socket(AF_INET,SOCK_STREAM))
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+131)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket[0].connect((self.address , self.port+131))
        self.clientSocket[1].connect((self.address , self.port+131))
        msg0 = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"MESSAGGIO 1"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"MESSAGGIO 2"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"LIST 0 1 6"+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 3"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 2"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"CONV 0\r\n"
        self.clientSocket[0].send(msg0)
        data0 = self.clientSocket[0].recv(1024)
        msg1 = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"MESSAGE 0 1"+'\r'+'\n'+"MESSAGGIO 1"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"MESSAGE 0"+'\r'+'\n'+"MESSAGGIO 2"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"LIST 0 1 6"+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 0"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 3"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"REPLY 2"+'\r'+'\n'+"hello second msg"+'\r'+'\n'+"."+'\r'+'\n'+'\r'+'\n'+"CONV 0\r\n"
        self.clientSocket[1].send(msg1)
        data1 = self.clientSocket[1].recv(1024)
        self.clientSocket[0].close()
        self.clientSocket[1].close()
        self.assertEqual(data0,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nOK 0\r\n", data0)
        
    def testSubscribeRegister(self):
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+38)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.clientSocket.connect((self.address , self.port+38))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"REGISTER 127.0.0.1 89\r\n"+"SUBSCRIBE 0 1 0\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nOK\r\nOK\r\n", data)
      
    def testSubscribeRegisterTaken(self):
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+40)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.clientSocket.connect((self.address , self.port+40))
        MyChatServer.registerHost['user1'] = ("127.0.0.1", 89)
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"REGISTER 127.0.0.1 89\r\n"+"SUBSCRIBE 0 1 0\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nKO\r\nKO\r\n", data) 
    def testSubscribeNoRegister(self):
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+37)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.clientSocket.connect((self.address , self.port+37))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"SUBSCRIBE 0 1\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nKO\r\n", data)
        
    def testUnSubscribeRegister(self):
        self.MyServer = MyChatServer(self.Dizionario,self.address , self.port+39)
        self.MyServer.beforeTest()
        self.MyServer.start()
        self.clientSocket = socket.socket(AF_INET,SOCK_STREAM)
        self.clientSocket.connect((self.address , self.port+39))
        msg = "USER Dani"+'\r'+'\n'+"PASS ciao"+'\r'+'\n'+"NEW CIAO"+'\r'+'\n'+"NEW ciao11"+'\r'+'\n'+"REGISTER 127.0.0.1 95\r\n"+"SUBSCRIBE 0 1 0\r\nUNSUBSCRIBE 0 1\r\n"
        self.clientSocket.send(msg)
        data = self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        data =data +  self.clientSocket.recv(1024)
        self.clientSocket.close()
        self.assertEqual(data,"OK\r\nOK\r\nOK 0\r\nOK 1\r\nOK\r\nOK\r\nOK\r\n", data)
        