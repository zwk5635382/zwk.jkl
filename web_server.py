from socket import *
from  select import select
import re
class WebServer:
    def __init__(self,*,host="0.0.0.0",port=80,html=None):
        self.host=host
        self.port=port
        self.html=html
        self.rlist=[]
        self.wlist=[]
        self.xlist=[]
        self.create_socket()
        self.bind()
    def create_socket(self):
        self.sock=socket()
        self.sock.setblocking(False)
    def bind(self):
        self.address=(self.host,self.port)
        self.sock.bind(self.address)
    def connect(self,sockfd):
        connfd,addr=sockfd.accept()
        print("Connect from ",addr)
        connfd.setblocking(False)
        self.rlist.append(connfd)
    def start(self):
        self.sock.listen(5)
        self.rlist.append(self.sock)
        while True:
            rs,ws,xs=select(self.rlist,self.wlist,self.xlist)
            for r in rs:
                if r is self.sock:
                    self.connect(r)

                else:
                    try:
                        self.handle(r)
                    except:
                        pass
                    finally:
                        r.close()
                        self.rlist.remove(r)

    def handle(self,connfd):
        request=connfd.recv(1024*10).decode()
        parrern=r"[A-Z]+\s+(?P<info>/\S*)"
        result=re.match(parrern,request)
        if result:
            info=result.group("info")
            self.send_html(connfd,info)
        else:
            return
    def send_html(self,connfd,info):
        if  info=="/":
            filename=self.html+"/index.html"
        else:
            filename=self.html+info
        try:
            file=open(filename,"rb")
        except:
            a="wangyebucunzai...."
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += a
            response=response.encode()
        else:
            data=file.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response = response.encode()+data
            file.close()
        finally:
            connfd.send(response)




if __name__ == '__main__':
    httpd=WebServer(host="0.0.0.0",port=8000,html="./static")
    httpd.start()