from socket import *
import socket
import threading
from threading import *


class MyChatServer(Thread):
    lock = threading.Lock()
    topicList = []
    messageList = []
    userList = []

    def beforeTest(self):
        print"test start"
        self.topicList = []
        self.messageList = []
        selfuserList = []
    def __init__(self, dictionary, serverAddress, serverPort):
        Thread.__init__(self)
        self.dic = dictionary
        self.sa = serverAddress
        self.sp = serverPort
    def run(self):
        self.start1()
    def start1(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.bind((self.sa, self.sp))
        serverSocket.listen(10)
        # print "Avvio Server..."
        while 1:
            connectionSocket, clientAddress = serverSocket.accept()
            CThread(connectionSocket, clientAddress, self.dic, self.lock).start()


class Message:
    def __init__(self, topicList, messageText):
        self.tlist = topicList
        self.msg = messageText
        self.parent = []
        self.child = []

    def __repr__(self):
        return '[' + str(self.tlist) + ', [' + self.msg + '], ' + str(self.parent) + ', ' + str(self.child) + ']\n'

    def getTList(self):
        return self.tlist

    def getMessageText(self):
        return self.msg

    def appendToParent(self, item):
        self.parent.append(int(item))

    def appendToChild(self, item):
        self.child.append(int(item))

    def getParent(self):
        if self.parent:
            return self.parent[0]
        return -1

    def getChild(self):
        return self.child


class User:
    def __init__(self, userName, host, port):
        self.name = userName
        self.host = host
        self.port = port
        self.tlist = set()
        self.digest = 1
        self.msgToSend = []

    def __repr__(self):
        l = len(str(self.tlist)) - 1
        return "(" + self.name + ", " + self.host + ", " + str(self.port) + ", " + str(self.tlist)[4:l] + ", " + str(
            self.digest) + ", " + str(self.msgToSend) + ")"

    def notifyUser(self, msg):  # va fatta in mutua esclusione
        self.msgToSend.append(msg)
        if len(self.msgToSend) > 1:
            previousMsg = self.msgToSend[len(self.msgToSend) - 2]
            self.msgToSend[len(self.msgToSend) - 2] = previousMsg[:len(previousMsg) - 5]
        sent = False
        if len(self.msgToSend) == self.digest:
            for msg in self.msgToSend:
                try:
                    userSocket = socket(AF_INET, SOCK_STREAM)
                    userSocket.connect((self.host, self.port))
                    userSocket.send(msg)
                    userSocket.close()
                    sent = True
                except:
                    pass
            if sent:
                self.msgToSend = []

    def setDigest(self, k):
        if int(k) == 0:
            self.digest = 1
        else:
            self.digest = int(k)
        if self.digest <= len(self.msgToSend):
            sent = False
            for msg in self.msgToSend:
                try:
                    userSocket = socket(AF_INET, SOCK_STREAM)
                    userSocket.connect((self.host, self.port))
                    userSocket.send(msg)
                    userSocket.close()
                    sent = True
                except:
                    pass
            if sent:
                self.msgToSend = []


class CThread(threading.Thread):
    def __init__(self, clientSocket, clientAddress, dictionary, lock):
        threading.Thread.__init__(self)
        self.cs = clientSocket
        self.ca = clientAddress
        self.dic = dictionary
        self.lock = lock
        self.cmdList = []
        self.userName = ''
        self.isLogged = False
        self.isOffLine = False

    def doLogin(self):
        if len(self.cmdList[0]) == 1:
            del self.cmdList[0]
            try:
                self.cs.send('KO\r\n')
            except:
                self.isOffLine = True
            return
        command = self.cmdList[0][0]
        data = ' '.join(self.cmdList[0][1:])
        del self.cmdList[0]
        if self.isLogged:  # USER o PASS non importa
            try:
                self.cs.send('KO\r\n')
            except:
                self.isOffLine = True
        elif command == 'PASS':
            try:
                if self.dic[
                    self.userName] == data:  # sto assumendo che self.userName sia significativo (potrebbe non stare nel dizionario)
                    self.isLogged = True
                    try:
                        self.cs.send('OK\r\n')
                    except:
                        self.isOffLine = True
                else:
                    self.userName = ''
                    try:
                        self.cs.send('KO\r\n')  # self.userName da qui in poi non e' piu' significativo
                    except:
                        self.isOffLine = True
            except KeyError:  # qui significa che self.userName non sta nel dizionario
                self.userName = ''
                try:
                    self.cs.send('KO\r\n')
                except:
                    self.isOffLine = True
        else:  # command == 'USER'
            if self.userName == '':  # non ho assegnato self.userName, questo significa che e' la prima USER
                self.userName = data
                try:
                    self.cs.send("OK\r\n")
                except:
                    self.isOffLine = True
            else:  # questo significa che non e' la prima USER
                try:
                    self.cs.send("KO\r\n")
                except:
                    self.isOffLine = True

    def doNewTopic(self):
        if len(self.cmdList[0]) == 1 or not self.isLogged:
            del self.cmdList[0]
            try:
                self.cs.send('KO\r\n')
            except:
                self.isOffLine = True
            return
        data = ' '.join(self.cmdList[0][1:])
        del self.cmdList[0]
        self.lock.acquire()
        MyChatServer.topicList.append(data)
        tid = str(len(MyChatServer.topicList) - 1)
        self.lock.release()
        try:
            self.cs.send('OK ' + tid + '\r\n')
        except:
            self.isOffLine = True

    def doTopicList(self):
        del self.cmdList[0]
        if self.isOffLine:
            return
        if not self.isLogged:
            try:
                self.cs.send('KO\r\n')
            except:
                self.isOffLine = True
            return
        res = 'TOPIC_LIST\r\n'
        self.lock.acquire()
        for i in range(len(MyChatServer.topicList)):
            res += self.s(i) + str(i) + ' ' + MyChatServer.topicList[i] + '\r\n'
        self.lock.release()
        try:
            self.cs.send(res + '\r\n')
        except:
            self.isOffLine = True

    def doMessage(self):
        k = -1
        for i in range(len(self.cmdList) - 1):
            if len(self.cmdList[i]) > 0 and self.cmdList[i][0] == '.' and len(self.cmdList[i + 1]) == 0:
                k = i + 1
                break
        messageText = ' '.join([' '.join(self.cmdList[i]) for i in range(1, k - 1)])
        self.lock.acquire()
        lenTopicList = len(MyChatServer.topicList)
        self.lock.release()
        cond = not set(self.cmdList[0][1:]) <= set([str(i) for i in range(lenTopicList)])
        if len(self.cmdList[0]) == 1 or not messageText or not self.isLogged or cond or k == -1:
            if k == -1:
                self.cmdList = []
            else:
                del self.cmdList[0:k + 1]
            try:
                self.cs.send('KO\r\n')
            except:
                self.isOffLine = True
            return
        topicList = self.cmdList[0][1:]
        del self.cmdList[0:k + 1]
        self.lock.acquire()
        MyChatServer.messageList.append(Message(topicList, messageText))
        mid = str(len(MyChatServer.messageList) - 1)
        self.notify(int(mid))
        self.lock.release()
        try:
            self.cs.send('OK ' + mid + '\r\n')
        except:
            self.isOffLine = True

    def doMessageList(self):
        if self.isOffLine:
            del self.cmdList[0]
            return
        self.lock.acquire()
        lenMessageList = len(MyChatServer.messageList)
        lenTopicList = len(MyChatServer.topicList)
        tlist = set(self.cmdList[0][2:])  # se la tlist non c'e', questo e' un insieme vuoto: {[]}
        if not self.isLogged or len(self.cmdList[0]) == 1 or int(self.cmdList[0][1]) < 0 or int(self.cmdList[0][
                                                                                                    1]) >= lenMessageList or not tlist <= set(
            ''.join(map(str, range(lenTopicList)))):
            self.lock.release()
            del self.cmdList[0]
            try:
                self.cs.send('KO\r\n')
            except:
                self.isOffLine = True
            return
        mid = int(self.cmdList[0][1])
        del self.cmdList[0]
        res = 'MESSAGES\r\n'
        for i in range(mid, lenMessageList):
            msgTList = MyChatServer.messageList[i].getTList()
            if len(tlist) == 0 or not tlist.isdisjoint(set(msgTList)):
                res += str(i) + ' ' + ' '.join(msgTList) + '\r\n'
        self.lock.release()
        try:
            self.cs.send(res + '\r\n')
        except:
            pass

    def doGetMessage(self):
        if self.isOffLine:
            del self.cmdList[0]
            return
        self.lock.acquire()
        if not self.isLogged or len(self.cmdList[0]) == 1 or not self.cmdList[0][1].isdigit() or int(
                self.cmdList[0][1]) >= len(MyChatServer.messageList):
            self.lock.release()
            del self.cmdList[0]
            try:
                self.cs.send('KO\r\n')
            except:
                self.isOffLine = True
            return
        mid = int(self.cmdList[0][1])
        tlist = MyChatServer.messageList[mid].getTList()
        text = MyChatServer.messageList[mid].getMessageText()
        self.lock.release()
        del self.cmdList[0]
        try:
            self.cs.send('MESSAGE ' + str(mid) + '\r\nTOPICS ' + ' '.join(tlist) + '\r\n' + text + '\r\n.\r\n\r\n')
        except:
            self.isOffLine = True

    def doReplyMessage(self):
        k = -1
        for i in range(len(self.cmdList) - 1):
            if len(self.cmdList[i]) > 0 and self.cmdList[i][0] == '.' and len(self.cmdList[i + 1]) == 0:
                k = i + 1
                break
        replyText = ' '.join([' '.join(self.cmdList[i]) for i in range(1, k - 1)])
        self.lock.acquire()
        if not self.isLogged or len(self.cmdList[0]) == 1 or not self.cmdList[0][1].isdigit() or int(
                self.cmdList[0][1]) >= len(MyChatServer.messageList) or k == -1:
            if k == 1:
                self.cmdList = []
            else:
                del self.cmdList[0:k + 1]
            self.lock.release()
            try:
                self.cs.send('KO\r\n')
            except:
                self.isOffLine = True
            return
        parentMid = int(self.cmdList[0][1])
        del self.cmdList[0:k + 1]
        inerithedTlist = MyChatServer.messageList[parentMid].getTList()
        message = Message(inerithedTlist, replyText)
        message.appendToParent(parentMid)
        MyChatServer.messageList.append(message)
        mid = str(len(MyChatServer.messageList) - 1)
        MyChatServer.messageList[parentMid].appendToChild(mid)
        self.notify(int(mid))
        self.lock.release()
        try:
            self.cs.send('OK ' + mid + '\r\n')
        except:
            self.isOffLine = True

    def doConv(self):
        if self.isOffLine:
            del self.cmdList[0]
            return
        self.lock.acquire()
        if not self.isLogged or len(self.cmdList[0]) == 1 or not self.cmdList[0][1].isdigit() or int(
                self.cmdList[0][1]) >= len(MyChatServer.messageList):
            self.lock.release()
            del self.cmdList[0]
            try:
                self.cs.send('KO\r\n')
            except:
                self.isOffLine = True
            return
        mid = int(self.cmdList[0][1])
        del self.cmdList[0]
        childList = self.getChildList(mid)
        parentList = self.getParentMid(mid)
        traversal = (childList + parentList + [mid])
        traversal.sort()
        res = 'MESSAGES\r\n'
        tlist = ' '.join(MyChatServer.messageList[mid].getTList())
        self.lock.release()
        for i in traversal:
            res += str(i) + ' ' + tlist + '\r\n'
        try:
            self.cs.send(res + '\r\n')
        except:
            self.isOffLine = True

    def getChildList(self, mid):
        res = MyChatServer.messageList[mid].getChild()
        if not res:
            return []
        for i in range(len(res)):
            aux = self.getChildList(int(res[i]))
            for k in range(len(aux)):
                res.append(aux[k])
        return res

    def getParentMid(self, mid):
        parent = MyChatServer.messageList[mid].getParent()
        if parent < 0:
            return []
        return [parent] + self.getParentMid(parent)

    def doRegister(self):
        if not self.isLogged or len(self.cmdList[0]) < 2 or not self.cmdList[0][2].isdigit():
            del self.cmdList[0]
            try:
                self.cs.send('KO\r\n')
            except:
                self.isOffLine = True
            return
        host = self.cmdList[0][1]
        port = int(self.cmdList[0][2])
        del self.cmdList[0]
        self.lock.acquire()
        for user in MyChatServer.userList:
            if user.name != self.userName and (host, port) == (user.host, user.port):
                self.lock.release()
                try:
                    self.cs.send('KO\r\n')
                except:
                    self.isOffLine = True
                return
            elif user.name == self.userName:
                user.host, user.port = host, port
                self.lock.release()
                try:
                    self.cs.send('OK\r\n')
                except:
                    self.isOffLine = True
                return
        MyChatServer.userList.append(User(self.userName, host, port))
        self.lock.release()
        try:
            self.cs.send('OK\r\n')
        except:
            self.isOffLine = True

    def doUnregister(self):
        del self.cmdList[0]
        self.lock.acquire()
        if not self.isLogged or not self.isRegistered():
            self.lock.release()
            try:
                self.cs.send('KO\r\n')
            except:
                self.isOffLine = True
            return
        for i in range(len(MyChatServer.userList)):
            if MyChatServer.userList[i].name == self.userName:
                del MyChatServer.userList[i]
                self.lock.release()
                try:
                    self.cs.send('OK\r\n')
                except:
                    self.isOffLine = True
                return

    def doScribe(self):
        cmd = self.cmdList[0][0]
        self.lock.acquire()
        if not self.isLogged or len(self.cmdList[0]) == 1 or not self.isRegistered() or not ''.join(
                self.cmdList[0][1:]).isdigit() or not set(self.cmdList[0][1:]) <= set(
            ''.join(map(str, range(len(MyChatServer.topicList))))):
            self.lock.release()
            del self.cmdList[0]
            try:
                self.cs.send('KO\r\n')
            except:
                self.isOffLine = True
            return
        tlist = set(self.cmdList[0][1:])
        del self.cmdList[0]
        for user in MyChatServer.userList:
            if user.name == self.userName:
                if cmd == 'SUBSCRIBE':
                    user.tlist.update(tlist)
                else:
                    user.tlist -= tlist
                self.lock.release()
                try:
                    self.cs.send('OK\r\n')
                except:
                    self.isOffLine = True
                return

    def doDigest(self):
        self.lock.acquire()
        if not self.isLogged or not self.isRegistered() or len(self.cmdList[0]) == 1 or not self.cmdList[0][
            1].isdigit():
            self.lock.release()
            del self.cmdList[0]
            try:
                self.cs.send('KO\r\n')
            except:
                self.isOffLine = True
            return
        for user in MyChatServer.userList:
            if user.name == self.userName:
                user.setDigest(self.cmdList[0][1])
                self.lock.release()
                del self.cmdList[0]
                try:
                    self.cs.send('OK\r\n')
                except:
                    self.isOffLine = True
                return

    def notify(self, mid):
        tlist = MyChatServer.messageList[mid].getTList()
        text = MyChatServer.messageList[mid].getMessageText()
        for user in MyChatServer.userList:
            tids = set(tlist) & user.tlist
            if len(tids) > 0:
                user.notifyUser(
                    'MESSAGE ' + str(mid) + '\r\nTOPICS ' + ' '.join(tlist) + '\r\n' + text + '\r\n.\r\n\r\n')

    def isRegistered(self):
        # si deve fare in mutua esclusione
        for user in MyChatServer.userList:
            if user.name == self.userName:
                return True
        return False

    def mySplit(self, msg):
        temp = ''
        if msg[len(msg) - 5:] == '\r\n.\r\n':
            k = len(msg) - 6
            while msg[k] != '\n':
                k -= 1
            while msg[k] != 'M' and msg[k - 1] != 'R':
                k -= 1
            temp = msg[k:]
        i = len(msg) - 3
        if msg[i] != '.':
            while i >= 0 and msg[i] != '\n':
                i -= 1
            if msg[i + 1:i + 6] == 'REPLY' or msg[i + 1:i + 8] == 'MESSAGE':
                temp = msg[i + 1:]
            elif i > 0:
                i -= 1
                while i >= 0 and msg[i] != '\n':
                    i -= 1
                if msg[i + 1:i + 6] == 'REPLY' or msg[i + 1:i + 8] == 'MESSAGE':
                    temp = msg[i + 1:]
        if temp:
            msg = msg[0:len(msg) - len(temp)]
        i = 0
        for j in range(len(msg) - 1):
            if msg[j] + msg[j + 1] == '\r\n':
                self.cmdList.append(msg[i:j])
                i = j + 2
        if i < len(msg):
            msg = msg[i:]
        elif temp:
            msg = temp
        else:
            msg = ''
        return msg

    def s(self, i):
        if not self.isRegistered():
            return ''
        for user in MyChatServer.userList:
            if self.userName == user.name and set(str(i)) <= user.tlist:
                return '*'
        return ''

    CMD = {'USER': doLogin,
           'PASS': doLogin,
           'NEW': doNewTopic,
           'TOPICS': doTopicList,
           'MESSAGE': doMessage,
           'LIST': doMessageList,
           'GET': doGetMessage,
           'REPLY': doReplyMessage,
           'CONV': doConv,
           'REGISTER': doRegister,
           'UNREGISTER': doUnregister,
           'SUBSCRIBE': doScribe,
           'UNSUBSCRIBE': doScribe,
           'DIGEST': doDigest,
           }

    def handleCmdList(self):
        x, y = 0, 0
        while self.cmdList and x == y:
            x += 1
            if len(self.cmdList[0]) == 0 or (len(self.cmdList[0]) > 0 and self.cmdList[0][0] not in self.CMD):
                y += 1
                del self.cmdList[0]
                try:
                    self.cs.send('KO\r\n')
                except:
                    self.isOffLine = True
        if self.cmdList:
            self.CMD[self.cmdList[0][0]](self)

    def run(self):
        msg = ''
        while not self.isOffLine:
            while self.cmdList:
                self.handleCmdList()
            try:
                recvChunk = self.cs.recv(8192)
                if len(recvChunk) == 0:
                    self.isOffLine = True
                    break
                msg += recvChunk
                if '\r\n' in msg:
                    msg = self.mySplit(msg)
                    self.cmdList = [self.cmdList[i].split() for i in range(len(self.cmdList))]
            except BaseException as e:
                # print e
                if self.lock.locked():
                    # print "rilascio il lock"
                    self.lock.release()
                break
        self.cs.close()

