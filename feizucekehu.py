from socket import *
sock=socket()
sock.connect(("176.233.35.3",7798))
while True:
    a=input(">>")
    sock.send(a.encode())
    data=sock.recv(1024)
    print(data.decode())