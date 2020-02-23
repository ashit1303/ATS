import RPi.GPIO as GPIO
import time
import socket 
host = ""
port = 8089
buf = 1024
addr = (host, port)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.bind(addr)

laser_pin=38
GPIO.setmode(GPIO.BOARD)
GPIO.setup(laser_pin, GPIO.OUT, initial=GPIO.LOW)
#def laser():
     #laser
#    try:
while True:
    (data, addr) = UDPSock.recvfrom(buf)
    data=data.decode()
    #data="laserTrue"
    if (data=="laserTrue"):
        GPIO.output(laser_pin, GPIO.HIGH)
        #print("In range")
        time.sleep(2)
        data="laserFalse"
        #GPIO.output(laser_pin, GPIO.LOW)
    else:
        GPIO.output(laser_pin, GPIO.LOW)
#    except:
#        GPIO.cleanup()
#        print("gpio.cleaned")

#if __name__ == '__main__':
#    laser()
