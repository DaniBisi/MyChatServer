import socket
import threading
from threading import Thread
from test.test_pydoc import expected_data_docstrings

class MyChatServer(threading.Thread):
    listaMessaggi = []
    listaTopic = []
    indiceTopic = 0
    countMessaggi = -1

    def __init__(self, dict, indirizzo, porta):
        threading.Thread.__init__(self)
        self.dict = dict
        self.indirizzo = indirizzo
        self.porta = porta
        self.codaSend = ""
    def beforeTest(self):
        print"testStarted.."
    def run(self):
        self.start1()
        
    def start1(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((self.indirizzo, self.porta))
        serverSocket.listen(10)
        print "Server started..."
        print "Using this dictionary: {}".format(self.dict)
        #while 1:
        print "Waiting for connections.."
        connectionScoket, addr = serverSocket.accept()
        print "New connection from {}".format(addr)
        #connectionScoket.send("Grazie per esserti connesso\r\n")
        t = threading.Thread(target=self.client_handler, args=(connectionScoket,))
        t.start()

    def client_handler(self, connectionScoket):
        stringa_ricevuta = ""
        userMandato = 0
        nomeUtente = ""
        AUTENTICATO = 1
        UTENTE = 0
        while 1:
            try:
                stringa_ricevuta += connectionScoket.recv(2048)
            except:
                return
            if not stringa_ricevuta: break  # TODO mettere il chiudi_socketserver()
            stringa_comandi, resto = self.parse_batch(stringa_ricevuta)
            stringa_ricevuta = resto
            for comando in stringa_comandi:
                funzione = comando.split()[0]
                if not userMandato and UTENTE != AUTENTICATO and funzione != "USER":
                    connectionScoket.send("KO\r\n")
                elif UTENTE != AUTENTICATO and funzione == "USER" and nomeUtente=="":
                    connectionScoket.send("OK\r\n")
                    userMandato = 1
                    nomeUtente = " ".join(comando.split()[1:])
                elif UTENTE != AUTENTICATO and funzione == "PASS" and userMandato:
                    password = " ".join(comando.split()[1:])
                    try:
                        if nomeUtente in self.dict and self.dict.get(nomeUtente) == password:
                            connectionScoket.send("OK\r\n")
                            UTENTE = AUTENTICATO
                        else:
                            connectionScoket.send("KO\r\n")
                            userMandato = 0
                            nomeUtente = ""
                    except Exception as e:
                        print e
                elif UTENTE == AUTENTICATO:
                    if funzione == "USER" or funzione == "PASS":
                        connectionScoket.send("KO\r\n")
                    else:
                        funzione = comando.split()[0]
                        if funzione in self.comandi:
                            #TODO inser lock here
                            ret = self.comandi[funzione](self, comando)
                            connectionScoket.send(ret)
                else:
                    connectionScoket.send("KO\r\n")

    def new_topic(self, stringaComando):
        nomeTopic = " ".join(stringaComando.split()[1:])
        if not nomeTopic:
            return "KO\r\n"
        topic = Topic(nomeTopic)
        self.listaTopic.append(topic)
        return "OK {}\r\n".format(len(self.listaTopic)-1)

    def topic_list(self, stringaComando):
        if stringaComando != "TOPICS\r\n":
            return "KO\r\n"
        del stringaComando
        testa = "TOPIC_LIST\r\n"
        if len(self.listaTopic) > 0:
            for topic in self.listaTopic:
                testa += "{} {}\r\n".format(self.listaTopic.index(topic), topic.nome_topic())
        testa += "\r\n"
        return testa

    def messaggio(self, stringaComando):
        if len(stringaComando.split()) <= 3:
            return "KO\r\n"
        try:
            lista_topic = map(int, stringaComando.split("\r\n")[0].split()[1:])
        except:
            return "KO\r\n"
        testo_messaggio = " ".join(("".join(stringaComando.split("\r\n.\r\n\r\n"))).split()[1+(len(lista_topic)):])
        for topic in lista_topic:
            try:
                self.listaTopic[topic].append(testo_messaggio, self.countMessaggi)
            except Exception:
                return "KO\r\n"
        self.countMessaggi += 1
        self.listaMessaggi.append((self.countMessaggi, testo_messaggio, lista_topic))
        return "OK {}\r\n".format(self.countMessaggi)

    def lista_messaggi(self, stringaComando):
        try:
            mid = stringaComando.split()[1]
        except:
            return "KO\r\n"
        tlist = []
        if len(stringaComando.split()) >2:
            try:
                tlist = map(int, stringaComando.split()[2:])
            except:
                return "KO\r\n"
        if len(tlist)!=0:
            for topic in tlist:
                if topic < 0:
                    return "KO\r\n"
                if topic >= len(self.listaTopic):
                    return "KO\r\n"
                    # TODO fix
        testa = "MESSAGES\r\n"
        for message in self.listaMessaggi:
            if message[0] >= int(mid):
                if len(tlist) == 0:
                    y = " ".join(map(str, message[2]))
                    testa += "{} {}\r\n".format(message[0], y)
                else:
                    for topic in tlist:
                        if topic in message[2]:
                            y = " ".join(map(str, message[2]))
                            #print "analizzo topic {}, messaggio: {}\r\naggiunto: {} {}\r\n".format(topic, message,message[0], y)
                            if testa.find("{} {}\r\n".format(message[0], y))==-1:
                                testa += "{} {}\r\n".format(message[0], y)
        return "{}\r\n".format(testa)

    def trova_messaggio(self, stringaComando):
        mid = int(stringaComando.split()[1])
        testa = "MESSAGE {}\r\n".format(mid)
        try:
            messaggioTrovato = self.listaMessaggi[mid]
        except Exception:
            return "KO\r\n"
        tids = " ".join(map(str,messaggioTrovato[2]))
        testa += "TOPICS {}\r\n".format(tids)
        testa += "{}\r\n.\r\n\r\n".format(messaggioTrovato[1])
        return testa

    def parse_command(self, connectionSocket, comandoMessage):
        messaggio = ""
        while messaggio.find("\r\n") == -1:
            stringa = connectionSocket.recv(2048)
            messaggio += stringa
        if comandoMessage and messaggio.find(
                ".\r\n\r\n") == -1:  # la seconda condizione e' per i messaggi su una riga sola
            while messaggio.find(".\r\n") == -1:
                stringa = connectionSocket.recv(2048)
                messaggio += stringa
            stringa = connectionSocket.recv(2048)
            while messaggio.find("\r\n") == -1:
                messaggio += stringa
        return messaggio

    def parse_batch(self, stringa):
        lista_comandi = []
        while stringa.find("\r\n") != -1:
            indexM = stringa.find("\r\n.\r\n\r\n")
            if stringa.startswith("MESSAGE ") and stringa.find("\r\n.\r\n\r\n") == -1:
                break
            index = stringa.find("\r\n")
            if indexM == index:
                lista_comandi[-1] += stringa[:indexM + 7]
                stringa = stringa[index + 7:]
            else:
                lista_comandi.append(stringa[:index + 2])
                stringa = stringa[index + 2:]
        return lista_comandi, stringa


    comandi = {'NEW': new_topic, 'TOPICS': topic_list, 'MESSAGE': messaggio, 'LIST': lista_messaggi,
               'GET': trova_messaggio}


class Topic:
    messageList = []
    nome = ""

    def __init__(self, nome):
        self.nome = nome

    def append(self, msg, id):
        self.messageList.append((msg, id))

    def nome_topic(self):
        return self.nome

    def lista_messaggi(self):
        return self.messageList


#dict = {'pippo': 'abcd'}

#t = MyChatServer(dict, "localhost", 12000)
#t.start()