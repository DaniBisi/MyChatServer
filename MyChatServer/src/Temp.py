# clientSocket.send('MESSAGE 0 1\r\n')
# clientSocket.send('Ciao mamma come stai?\r\n')
# clientSocket.send('.\r\n')
# clientSocket.send('\r\n')

# [['MESSAGE', '0', '1'], ['Ciao', 'mamma', 'come', 'stai?'], ['.'], []]

# list = [['MESSAGE'], ['Ciao', 'mamma', 'come', 'stai?'], ['USER'], ['PASS', 'sbagliata'], ['.'],[], ['Ciao', 'mamma', 'come', 'stai?'], ['USER'], ['PASS', 'sbagliata.'], []]
#
# k = -1
# for i in range(len(list) - 1):
#     if len(list[i]) > 0 and list[i][0] == '.' and len(list[i + 1]) == 0:
#         k = i+1
#
#
# messageText = ' '.join([' '.join(list[i]) for i in range(1,k-1)])
#
# print messageText
#
# cmd = [['LIST', '0', '2']]
# messageList = [(['0', '1', '2', '3'], 'Ciao!'), (['0', '1', '3'], 'Bau!'), (['2', '3'], 'Miao!')]
# print ' '.join(messageList[2][0])
#
# tlist = set(cmd[0][2:])  # se la tlist non c'e', questa e' una lista vuota: []
# msgtlist = set(messageList[1][0])
# print tlist
# print msgtlist
#
# print tlist.isdisjoint(msgtlist)
#
#
# res = 'MESSAGES\r\n'

# for i in range(mid, len(messageList)):
#     if tlist <= set(messageList[i][0]):
#         res += str(i)+' '+ ' '.join(messageList[i][0])+'\r\n'
#
# print res

# c = [['LIST', '0', '2', '3']]
#
# a = [0,1,2,3,4,5,6,7]
# l = len(a)
# intList = [0,1,2,3,4,5,6,7,8,9]
# print set(''.join(map(str, range(l))))

#
# cmdList = [['MESSAGE', '0', '1', '2', '3'], ['Ciao!', 'Come', 'stai?'], ['.'], []]
#
# k = -1
# for i in range(len(cmdList) - 1):
#     print "list[{}]: {}".format(i, cmdList[i])
#     print "list[{}][0]: {}".format(i, cmdList[i][0])
#     print '\n'
#     if len(cmdList[i]) > 0 and cmdList[i][0] == '.' and len(cmdList[i + 1]) == 0:
#         k = i + 1
#         break
# messageText = ' '.join([' '.join(cmdList[i]) for i in range(1, k - 1)])
#
# print messageText

#
# [[0],[1],[2]] UNITO [[1],[3]]
# deve dare
# [[0],[1],[2],[3]]

#
# a = [[0], [1], [2]]
# b = [[1], [3]]
# print list(set().union(a, b))
# DIO CANE BISI NON FUNZIONAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA



# def __Dig(self, base):
#     print base
#     lista = []
#     try:
#         lista = MyChatServer.reply[base]
#     except:
#         return ""
#     print MyChatServer.reply
#     print lista
#     for i in range(len(lista)):
#         listaT = self.__Dig(str(lista[i]))
#         for k in range(len(listaT)):
#             lista.append(listaT[k])
#     return lista
#
#
# def __DigUp(self, base):
#     print base
#     lista = []
#     try:
#         lista.append(MyChatServer.replyFather[base])
#     except:
#         return ""
#     print MyChatServer.reply
#     print lista
#     listaT = self.__DigUp(lista[0])
#     for k in range(len(listaT)):
#         lista.append(listaT[k])
#     return lista
#
# DIC = {'user1': 'pass1',
#        'user2': 'pass2',
#        'user3': 'pass3'
#        }
#
# regUsers = {'user1': ('localhost', 1),
#             'user2': ('localhost', 2),
#             'user3': ('localhost', 3)
#             }
#
# # regUsers = {}
# userName = 'user3'
# host = 'localhost'
# port = 1
# logged = True
# cond = False
#
#
#
# if userName not in regUsers or not logged:
#     print 'KO'
#     cond = True
#
# if not cond:
#     regUsers.pop(userName, None)
#
# print regUsers


# cmdList = [['COMANDO','1','2','4',]]
# #              0      1       2       3     4
# topicList = ['fea','fdafa','43214','432f','fafa']
#
# tlist = set(cmdList[0][1:])
# topicNumber = set(''.join(map(str, range(len(topicList)))))

# print "tlist:",tlist
# print "topicNumber:",topicNumber
#
#
# print not set(cmdList[0][1:]) <= set(''.join(map(str, range(len(topicList)))))
#
#
# print not tlist <= topicNumber
#
# print tlist in topicNumber
# userName = 'user0'
# tlist0 = set(range(1))
# tlist1 = set(range(2))
# tlist2 = set(range(3))
# userTopics = []
# userTopics.append(('user0', tlist0))
# userTopics.append(('user1', tlist1))
# userTopics.append(('user2', tlist2))
# print tlist0
# print tlist1
# print tlist2
#
# print userTopics
#
# for i in range(len(userTopics)):
#     if userTopics[i][0] == userName:
#         userTopics[i][1].update(tlist1)
#         break
#
#
# print userTopics
#
# class User:
#     def __init__(self, name, host, port):
#         self.name = name
#         self.host = host
#         self.port = port
#
#     def __repr__(self):
#         return "("+self.name+", "+self.host+", "+str(self.port)+")"
#
# userName = 'user1'
# host = 'localhost'
# port = 20
#
# a = User('user1', 'casa mia', 20)
# b = User('user2', 'localhost', 10)
#
# userList = []
# userList.append(a)
# userList.append(b)
# print userList
#
#
# for user in userList:
#     if user.name != userName and (host, port) == (user.host, user.port):
#         print 'KO'
#         break
#     elif user.name == userName:
#         user.host, user.port = host, port
#         print 'OK'
#         break
#
# print userList
from socket import *
import time
import threading



class MyUserServer:
    def __init__(self, serverAddress, serverPort):
        self.sa = serverAddress
        self.sp = serverPort

    def start(self):
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind((self.sa, self.sp))
        serverSocket.listen(10)
        print "Avvio Server..."
        while 1:
            connectionSocket, clientAddress = serverSocket.accept()
            UThread(connectionSocket, clientAddress).start()

class UThread(threading.Thread):
    def __init__(self, clientSocket, clientAddress):
        threading.Thread.__init__(self)
        self.cs = clientSocket
        self.ca = clientAddress
    def run(self):
        msg = ''
        while True:
            try:
                recvChunk = self.cs.recv(8192)
                if len(recvChunk) == 0:
                    break
                msg += recvChunk
                print msg
            except BaseException as e:
                print e

        # print "Chiudo la connessione anch'io"
        self.cs.close()

#####################
#   M   A   I   N   #
#####################
print "[Main] Sto per avviare il server"
MyUserServer('localhost', 1984).start()
