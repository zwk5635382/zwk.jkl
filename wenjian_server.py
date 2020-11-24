from socket import *
from threading import Thread
import sys
import os
from time import sleep
HOST="0.0.0.0"
PDRT=9958
ADDR=(HOST,PDRT)
FTP="/home/tarena/zwk/123/"
class Handle(Thread):
    def __init__(self,connfd):
        self.connfd=connfd
        super().__init__(daemon=True)
    def xiazai(self,name):
        list01 = os.listdir(FTP)
        if name in list01:
            self.connfd.send("OK".encode())
            fr = open(FTP + name, 'rb')
            sleep(0.1)
            while True:
                data = fr.read(1024)
                if not data:
                    break
                self.connfd.send(data)
            fr.close()
            sleep(0.1)
            self.connfd.send("##".encode())
        else:
            self.connfd.send("FAIA".encode())
    def chakan(self):
        list01 = os.listdir(FTP)
        if list01:
            self.connfd.send("OK".encode())
            sleep(0.1)
            list02="  ".join(list01)
            self.connfd.send(list02.encode())
            sleep(0.1)
            self.connfd.send(b"##")
        else:
            data="FAIL"
            self.connfd.send(data.encode())
    def shangchuan(self,lujin):
        list01 = os.listdir(FTP)
        name=lujin.split("/")[-1]
        if name in list01:
            self.connfd.send(b"FAIA")
        else:
            self.connfd.send(b"OK")
            fw=open(FTP+name,"wb")
            sleep(0.1)
            while True:
                fw01 = self.connfd.recv(1024)
                if fw01 == b"##":
                    break
                fw.write(fw01)
            fw.close()
    def run(self):
        while True:
            data = self.connfd.recv(1024).decode()
            tmp = data.split(" ")
            if not data or tmp[0]=="exit":
                break
            elif tmp[0]=="list":
                self.chakan()
            elif tmp[0]=="get":
                self.xiazai(tmp[1])
            elif tmp[0]=="put":
                self.shangchuan(tmp[1])
        self.connfd.close()

def main ():
    sock=socket()
    sock.bind(ADDR)
    sock.listen(5)
    print("Listen the port %d..." % PDRT)
    while True:
        try:
            connfd,addr=sock.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            sock.close()
            sys.exit("服务退出")
        t=Handle(connfd)
        t.start()
if __name__ == '__main__':
    main()
