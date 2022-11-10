import time
from SimpleOSC import SimpleOSCParser

class PBSOSC:
    def __init__(self, esp, socket, parser):
        self.HOST = "172.19.13.33"
        self.PORT = 1213
        self.TIMEOUT = 5
        self.INTERVAL = 5
        self.MAXBUF = 256
        self.parser = parser
        self.esp = esp
        self.socket = socket
        print("Create UDP Client Socket")
        self.s = socket.socket(type=socket.SOCK_DGRAM)
        self.s.settimeout(self.TIMEOUT)

        print("Connecting")
        self.socketaddr = socket.getaddrinfo(self.HOST, self.PORT)[0][4]
        self.s.connect(self.socketaddr, conntype=esp.UDP_MODE)

    def loop(self, cb):
        if self.s.available:
            buf = self.s.recv(self.MAXBUF)
            topic, types, output = self.parser.parseOSC(buf)
            if topic:
                cb(topic, types, output)

    def sendMessage(self, message):
        self.s.close()
        self.s.connect(self.socketaddr, conntype=self.esp.UDP_MODE)
        print("sending: ", message)
        self.s.send(message)
