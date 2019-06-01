from socket import *

udpSocket = socket(AF_INET,SOCK_DGRAM)

udpSocket.sendto(b"陈永建真帅",("192.168.43.15",8080))