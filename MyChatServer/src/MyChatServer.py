'''
Created on 03 nov 2016

@author: Daniele Bisignano
'''
import threading
from threading import * 
#from threading import Condition 
import socket




class ClientHandler(Thread):

    
    
    
    def __init__(self, sock, Dizionario, lock):
        Thread.__init__(self)
        self.lock = lock
        self.Dizionario = Dizionario
        self.sock = sock
        self.login = 0
        self.loginAttempt = 0
        self.userAttempt = ""
        self.userName = ""
        self.command = {
            "USER": self.user,
            "PASS": self.password,
            "NEW": self.topic,
            "TOPICS": self.topic_list,
            "MESSAGE": self.message,
            "LIST": self.msgList,
            "REPLY": self.msgReply,
            "CONV": self.conv,
            "GET": self.getMsg,
            "REGISTER": self.register,
            "UNREGISTER": self.unregister,
            "SUBSCRIBE": self.subscribe,
            "UNSUBSCRIBE": self.unsubscribe
        }
        self.autobreak = 0
        self.login = 0
        pass
    
    
    def __getMessage(self):
        data = ""
        i = -2
        try:
            while True:
                data = data + self.sock.recv(1)
                # print data
                if(data[len(data) - 2] == '\r' and data[len(data) - 1] == '\n'):
                    break
        except:
            self.sock.close()
            print "Close connection by remote host..."
            self.autobreak = 1
        if not data:
            # if not self.sock.is_alive():    
            self.sock.close()
            self.autobreak = 1 
        return data 
    
    def __sendMessage(self, str):
        try:
            self.sock.send(str)
        except:                
            # if not self.sock.is_alive():    
            self.sock.close()
            self.autobreak = 1 
    def subscribe(self,param):
        if self.login:
            try:
                registered = MyChatServer.registerHost[self.userAttempt]
                print len(param)
                for k in range(len(param)):
                    found = MyChatServer.topicList[int(param[k])][0]
            except:
                self.__sendMessage("KO" + '\r' + '\n')
                exit()
            with self.lock:
                for k in range(len(param)):
                    try:
                        userList = MyChatServer.subscribed[param[k]]
                        if not self.userAttempt in userList:
                            userList.append(self.userAttempt)
                            #print "printo userlist \r\n"
                            #print userList
                            MyChatServer.subscribed[param[k]] = userList
                   
    #                     userList = MyChatServer.subscribed[param[k]]
    #                     if not param[k] in userList:
    #                         userList.append(self.userAttempt)
                    except:
                        userList = []
                        userList.append(self.userAttempt)
                        MyChatServer.subscribed[param[k]] = userList
                    #print userList
                    #print "\r\n"
                    #print MyChatServer.subscribed       
            self.__sendMessage("OK" + '\r' + '\n')   
        else:
            self.__sendMessage("KO" + '\r' + '\n')     
        pass
    def unsubscribe(self,param):
        if self.login:
            failure = False
            try:
                registered = MyChatServer.registerHost[self.userAttempt]
                for k in range(len(param)):
                    found = MyChatServer.topicList[int(param[k])][0]
            except:
                self.__sendMessage("KO" + '\r' + '\n')
                exit()
            with self.lock:
                for k in range(len(param)):
                    try:
                        userList = MyChatServer.subscribed[param[k]]
                        for i in range(len(userList)):
                            if userList[i] == self.userAttempt:
                                del userList[i]
                        MyChatServer.subscribed[param[k]] = userList
                        if len(userList) == 0:
                            del MyChatServer.subscribed[param[k]]
                    except:
                        failure = True
                        #print"fail remove subscrive..."
    #                 print userList
    #                 print "\r\n"
    #                 print MyChatServer.subscribed       
            self.__sendMessage("OK" + '\r' + '\n') 
        else:
            self.__sendMessage("KO" + '\r' + '\n')       
        pass
        
    def run(self):
        i = 0
        while(not self.autobreak):
            i = i + 1
            data = self.__getMessage()
            if self.autobreak:
                exit()
            data = data.split()
            param = data[1:]
            
            try: 
                with self.lock:
                    self.command[data[0]](param)
            except Exception as e:
                print e
                self.__sendMessage("KO" + '\r' + '\n')
            
    def user(self, param):
            self.loginAttempt = 1
            self.userAttempt = param[0]
            self.__sendMessage("OK" + '\r' + '\n')
            
    def password(self, param):
        if self.loginAttempt:
            try:
                user = str(self.userAttempt)
                if self.Dizionario[user] == param[0]:
                    self.__sendMessage("OK" + '\r' + '\n')
                    self.login = 1
                    del self.command['USER']
                    del self.command['PASS']
                    # self.command = self.command[1:] #login non e piu un comando possibile quindi lo rimuovo dall'elenco.  #cosi facendo ho automatico anche la gestione dell'errore nel caso l'utente provasse a reinviare il comando login 
                else:
                    self.loginAttempt = 0
                    self.userAttempt = ""
                    self.__sendMessage("KO" + '\r' + '\n')
            except Exception as e:
                print e
                self.__sendMessage("KO" + '\r' + '\n')
        else:
            self.__sendMessage("KO" + '\r' + '\n')       
    def topic(self, param):
        # print param
        if self.login:
            with self.lock:
                topicIndex = MyChatServer.MyChatServerAddTopic(param[0])
                self.__sendMessage("OK " + str(topicIndex) + '\r' + '\n')
                self.lock.notify_all()
        else:
            self.__sendMessage("KO" + '\r' + '\n')    
    def topic_list(self, param):
        if self.login:
            if not len(param)>0:
                str1 = "TOPIC_LIST\r\n"
                if self.login:
                    with self.lock:
                        for i in range(len(MyChatServer.topicList)):
                            checked = ""
                            
                            try:
                                if self.userAttempt in (MyChatServer.subscribed[str(i)]):
                                    checked = "*"
                            except:
                                print""
                            str1 = str1 +checked + str(i) + " " + MyChatServer.topicList[i] + "\r\n"
                    str1 = str1 + "\r\n"
                    #print str1
                    
                    self.__sendMessage(str1)
                else:
                    self.__sendMessage("KO" + '\r' + '\n')
            else:
                self.__sendMessage("KO" + '\r' + '\n')
        else:
                self.__sendMessage("KO" + '\r' + '\n')        
            # self.lock.notify_all()
     
    def register(self,param):
        if self.login:
            occupato = False
            coppia = (param[0],int(param[1]))
            with self.lock:
                for key, value in MyChatServer.registerHost.iteritems():
                #for i in range(len(MyChatServer.registerHost)):
                    coppiaLocal = value
                    if coppiaLocal==coppia:
                        try:
                            MyChatServer.registerHost[self.userAttempt]
                        except:
                            occupato = True
                            
                        break  
            if occupato:
                self.__sendMessage("KO" + '\r' + '\n')
            else:          
                MyChatServer.registerHost[self.userAttempt]=(param[0],int(param[1]))
                self.__sendMessage("OK" + '\r' + '\n')
        else:
            self.__sendMessage("KO" + '\r' + '\n')
    def unregister(self,param):
        if self.login:
            if not len(param)>0:
                try:
                    with self.lock:
                        registerHostProvv = MyChatServer.registerHost[self.userAttempt]
                        del MyChatServer.registerHost[self.userAttempt]
                except:
                    self.__sendMessage("KO" + '\r' + '\n')
                    exit()
                #################### INIZIO UNSUBSCRIBE ######################
                failure = False
                try:
                    #registered = registerHostProvv
                    with self.lock:
                        #param = [i for i in range(len(MyChatServer.topicList))]
                        for k in range(len(MyChatServer.topicList)):
                            try:
                                userList = MyChatServer.subscribed[str(k)]
                                for i in range(len(userList)):
                                    if userList[i] == self.userAttempt:
                                        #print "cancello..." + userList[i]
                                        del userList[i]
                                MyChatServer.subscribed[str(k)] = userList
                                if len(userList) == 0:
                                    del MyChatServer.subscribed[str(k)]
                            except:
                                failure = True
                                #print"fail remove subscrive..."
                except:
                    print ""                
                ######################FINE UNSUBSCRIBE ##########################
                
                self.__sendMessage("OK" + '\r' + '\n')
            else:
                self.__sendMessage("KO" + '\r' + '\n')
        else:
            self.__sendMessage("KO" + '\r' + '\n')        
        
    def getMsg(self, param):
        if self.login:
            if len(param) > 1:
                self.__sendMessage("KO" + '\r' + '\n')
                exit()
            IDmsg = param[0]
            with self.lock:
                try:
                    listOfTopic = MyChatServer.message[int(IDmsg)][1]
                    text = MyChatServer.message[int(IDmsg)][0]
                except:
                    self.__sendMessage("KO" + '\r' + '\n')
                    exit()
            listOfTopic = " ".join(listOfTopic)
            response = "MESSAGE " + IDmsg + "\r\n" + "TOPICS " + listOfTopic + "\r\n" + text + "\r\n" + ".\r\n\r\n"
            self.__sendMessage(response)
        else:
            self.__sendMessage("KO" + '\r' + '\n')      
    def message(self, param):
        data = ""
        escape_sequence = '\r' + '\n' + "." + '\r' + '\n' + '\r' + '\n'
        while True:
            data = data + self.__getMessage()
            data2 = data[-5:]
            if(self.autobreak or data[-7:] == escape_sequence):
                break
        if self.login:
            msgId =""        
            with self.lock:
                topicExists = True
                for i in range(len(param)):
                    try:
                        #print "provo param di i:"
                        #print param[i]
                        MyChatServer.topicList[int(param[int(i)])]
                    except:
                        topicExists = False
                        break
                if topicExists:
                    if(not self.autobreak):
                        data = data[:-7]
                        with self.lock:
                            msgId = MyChatServer.MyChatServerAddMessage(data, param)
                        self.__sendMessage("OK " + str(msgId) + '\r' + '\n')
                else:
                    self.__sendMessage("KO" + '\r' + '\n')
            with self.lock:
                #per ogni topic ricevuto nel messaggio
                msg = "MESSAGE "+str(msgId)+"\r\n"+"TOPICS "+" ".join(param)+"\r\n"+data+"\r\n.\r\n\r\n"
                #print msg
                for i in range(len(param)):
                    try:
                        userSubscribedList = MyChatServer.subscribed[param[i]]
                        for k in range(len(userSubscribedList)):
                            userSubscribed = userSubscribedList[k]
                            host = MyChatServer.registerHost[userSubscribed][0]
                            Port = MyChatServer.registerHost[userSubscribed][1]
                            #print(userSubscribed)
                            clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                            clientSocket.connect((host,Port))
                            clientSocket.send(msg)
                            clientSocket.close()
                    except:
                        print""
        else:
            self.__sendMessage("KO" + '\r' + '\n')
    def msgList(self, param):
        if self.login:
            msgID = param[0]
            param = param[1:]
            Response = "MESSAGES\r\n"
            if self.login:
                with self.lock:
                    topicExists = True
                    for i in range(len(param)):
                        try:
                            #print "provo param di i:"
                            print param[i]
                            MyChatServer.topicList[int(param[int(i)])]
                        except:
                            topicExists = False
                            break
                    if topicExists:
                        for i in range(int(msgID), len(MyChatServer.message)):
                            find = False
                            listOfTopic = MyChatServer.message[i][1]
                            if len(param) > 0:
                                for k in range(len(param)):
                                    if param[k] in listOfTopic:
                                        find = True
                                        break
                                if find == True:
                                    Response = Response + str(i) + " " + " ".join(listOfTopic) + "\r\n"
                            else:
                                Response = Response + str(i) + " " + " ".join(listOfTopic) + "\r\n"
                        Response = Response + "\r\n"
                        #print Response
                        self.__sendMessage(Response)
                    else:
                        self.__sendMessage("KO" + '\r' + '\n')
            else:
                self.__sendMessage("KO" + '\r' + '\n')
        else:
                self.__sendMessage("KO" + '\r' + '\n')        
    def msgReply(self, param):
        
        msgID = param[0]
        data = ""
        escape_sequence = '\r' + '\n' + "." + '\r' + '\n' + '\r' + '\n'
        while True:
            data = data + self.__getMessage()
            data2 = data[-5:]
            if(self.autobreak or data[-7:] == escape_sequence):
                break
        if self.login and len(param) == 1:
            msgExists = True
            with self.lock:
                try:
                    #print "provo message di i:"
                    #print param[0]
                    topicListFather = MyChatServer.message[int(param[0])][1]
                except:
                    msgExists = False
                if msgExists:
                    if(not self.autobreak):
                        data = data[:-7]
                        with self.lock:
                            replyId = MyChatServer.MyChatServerAddMessage(data, topicListFather)
                            msgId = MyChatServer.MyChatServerAddReply(replyId, msgID)
                        self.__sendMessage("OK " + str(replyId) + '\r' + '\n')
                else:
                    self.__sendMessage("KO" + '\r' + '\n')
                    
        else:
            self.__sendMessage("KO" + '\r' + '\n')
            
    def conv(self, param):
        if self.login:
            msgID = param[0]
            listRep = []
            hasReply = True
            with self.lock:
                try:
                    # se fallisce questo try non e un messaggio valido quindi termino
                    topicFatherList = MyChatServer.message[int(msgID)][1]
                    #print topicFatherList
                except:
                    self.__sendMessage("KO" + '\r' + '\n')
                    exit()
                try:
                    listRep = MyChatServer.reply[msgID]
                except:
                    hasReply = False
                response = "MESSAGES\r\n"
                # response = + msgID +" " + " ".join(MyChatServer.message[int(msgID)][1])+"\r\n"
                listaT = []
                if hasReply:
                    listaT = self.__Dig(msgID)
                listaC = self.__DigUp(msgID)
                ListaCompleta = list(set().union(listaC, listaT, [msgID]))
                ListaCompleta = sorted(ListaCompleta)
                for k in range(len(ListaCompleta)):
                    messageIndex = int(ListaCompleta[k])
                    response = response + str(messageIndex) + " " + " ".join(MyChatServer.message[messageIndex][1]) + "\r\n"
                # print response
                response = response + "\r\n"
            self.__sendMessage(response)
        else:
            self.__sendMessage("KO" + '\r' + '\n')
    def __Dig(self, base):
        #print base
        lista = []
        try:
            lista = MyChatServer.reply[base]
        except:
            return ""
        #print MyChatServer.reply
        #print lista
        for i in range(len(lista)):
            listaT = self.__Dig(str(lista[i]))
            for k in range(len(listaT)):
                lista.append(listaT[k])
        return lista
    def __DigUp(self, base):
        #print base
        lista = []
        try:
            lista.append(MyChatServer.replyFather[base])
        except:
            return ""
        #print MyChatServer.reply
        #print lista
        listaT = self.__DigUp(lista[0])
        for k in range(len(listaT)):
            lista.append(listaT[k])
        return lista
    
class MyChatServer(Thread):
    topicList = []
    message = []
    reply = {}
    replyFather = {}
    registerHost = {}
    subscribed = {}
    def __init__(self, Dizionario, Host, Port):
        Thread.__init__(self)    #implementato per i test con pyUnit
        
        self.Dizionario = Dizionario
        self.Host = Host
        self.Port = Port
        self.serverSocket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.serverSocket.bind((self.Host, self.Port))
        self.serverSocket.listen(10)
        self.lock = threading.Condition()
        pass
    @classmethod
    def MyChatServerAddTopic(self, name):
        MyChatServer.topicList.append(name)
        topicIndex = len(MyChatServer.topicList) - 1
        #print MyChatServer.topicList
        return topicIndex
    @classmethod
    def MyChatServerAddMessage(self, msg, param):
        MyChatServer.message.append([msg])
        msgIndex = len(MyChatServer.message) - 1
        MyChatServer.message[msgIndex].append(param)
        #print MyChatServer.message
        return msgIndex
    @classmethod
    def MyChatServerAddReply(self, repId, msgId):
        listApp = []
        try:
            listApp = MyChatServer.reply[msgId]
        except:
            print""
        listApp.append(str(repId))
        #print listApp
        #print"ecco invece il msgid {}".format(msgId)
        MyChatServer.reply[msgId] = listApp
        MyChatServer.replyFather[str(repId)] = str(msgId)
        nReply = len(MyChatServer.reply[msgId]) - 1
#         msgIndex = len(MyChatServer.message)-1
#         MyChatServer.message[msgIndex].append(param)
        #print MyChatServer.reply
        
        return nReply
    @classmethod
    def beforeTest(self):
        self.topicList = []
        self.message = []
        self.reply = {}
        self.replyFather = {}
        self.registerHost = {}
        self.subscribed = {}
    
    def run(self):        #implementato per i test con pyunit
        self.start1()  
    def start1(self):
        gestore = []
        while(1):
            try:
                connectionSocket, addr = self.serverSocket.accept()
                print "nuova connessione"
                gestore.append(ClientHandler(connectionSocket, self.Dizionario, self.lock))
                gestore[len(gestore)-1].start()
            except Exception as e:
                print e
#             MyChatServer.topicList = []
#             MyChatServer.message = []
#             MyChatServer.reply = {}
#             MyChatServer.replyFather = {}
        #for i in range(len(gestore)):
            #gestore[i].join()  
            #connectionSocket.close()
# Dizionario = {
#     "Dani": "ciao",
#     "user1": "pass1",
#     "user2": "pass2",
#     "user3": "pass3"}
# MyChatServer(Dizionario, "127.0.0.1", 102).start()
