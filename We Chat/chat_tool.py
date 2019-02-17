# coding:utf8

from threading import Thread
from socket import *

def send(sendAddr):
	while True:
		sendInfo = input("<<")
		udpSocket.sendto(sendInfo.encode("utf-8"),sendAddr)

def receive():
	while True:
		recvData = udpSocket.recvfrom(1024)
		content = recvData[0].decode("utf-8")
		addr = recvData[1]
		print("\n>>[%s]: %s"%(addr,content))

udpSocket = None

def main():
	global udpSocket
	udpSocket = socket(AF_INET,SOCK_DGRAM)
	post = int(input("Enter your post please..."))
	post2 = int(input("Enter post of the other party..."))
	addr = input("Enter IP of the other party...")
	udpSocket.bind(("",post))
	sendAddr = (addr,post2)

	ts = Thread(target=send,args=(sendAddr,))
	tr = Thread(target=receive)
	ts.start()
	tr.start()
	ts.join()
	tr.join()

if __name__ == "__main__":
	main()
