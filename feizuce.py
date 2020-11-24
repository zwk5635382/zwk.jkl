from socket import *
from time import sleep

sock=socket()
sock.bind(("0.0.0.0",9967))
sock.listen(5)
sock.setblocking(False)
while True:
    try:
        print("等待客户连接....")
        connfd,addr=sock.accept()
        print("连接",addr)
    except BlockingIOError as e:
        print("沉睡中....")
        sleep(10)
    else:
        data=connfd.recv(1024)
        print(data.decode())
        connfd.send("你好".encode())