import os
from socket import * 
import time
pir=("pirTrue")
rcwl=("rcwlTrue")
#host = "192.168.43.6" # set to IP address of target computer
host = "192.168.0.106"
port = 8085
port1 = 8086
addr = (host, port)
addr1 = (host, port1)
UDPSock = socket(AF_INET, SOCK_DGRAM)
while True:
    #data = input("Enter message to send or type 'exit': ")
    data = pir
    data1 = rcwl
    UDPSock.sendto(data.encode(), addr)
    UDPSock.sendto(data1.encode(), addr1)
    time.sleep(3)
    if data == "exit":
        break
UDPSock.close()
os._exit(0)
