from socket import *
from time import sleep
import sys
ADDR=("176.233.35.3",9958)
class FTP:
    def __init__(self,sock):
        self.sock=sock
    def do_list(self):
        data01="list "
        self.sock.send(data01.encode())
        data=self.sock.recv(1024).decode()
        if data=="OK":
            while True:
                n=self.sock.recv(1024).decode()
                if n=="##":
                    break
                print(n,end="")
        else:
            print("文件为空")
    def do_get(self):
        a=input("请输入需要下载的文件：")
        b="get "+a
        self.sock.send(b.encode())
        data=self.sock.recv(1024).decode()
        if data=="OK":
            print("正在下载中")
            fw=open("/home/tarena/zwk/789/"+a,'wb')
            while True:
                fw01=self.sock.recv(1024)
                if fw01==b"##":
                    print("下载成功")
                    break
                fw.write(fw01)
            fw.close()
        else:
            print("文件不存在")
    def do_put(self):
        a=input("请输入需要上传的文件:")
        self.sock.send(("put "+a).encode())
        b=self.sock.recv(1024).decode()
        if b=="OK":
            print("正在上传中.....")
            fr=open(a,"rb")
            while True:
                data = fr.read(1024)
                if not data:
                    print("上传成功")
                    break
                self.sock.send(data)
            fr.close()
            sleep(0.1)
            self.sock.send("##".encode())
        else:
            print("文件已存在,上传失败")
    def exit(self):
        self.sock.send(b"exit")
        self.sock.close()
        sys.exit("谢谢使用")

def main():
    sock=socket()
    sock.connect(ADDR)
    ftp=FTP(sock)
    while True:
        print("========================")
        print("******  1,list    ******")
        print("****** 2,get file ******")
        print("****** 3,put file ******")
        print("******   4,exit   ******")
        print("========================")
        data=input("请输入编号：")
        if data=="1":
            ftp.do_list()
        elif data=="2":
            ftp.do_get()
        elif data=="3":
            ftp.do_put()
        elif data=="4":
            ftp.exit()
        else:
            print("请输入正确指令")

if __name__ == '__main__':
    main()
