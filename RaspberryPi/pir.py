
import RPi.GPIO as GPIO
import time
import socket
pir_pin=35

host = "192.168.43.6" # set to IP address of target computer
port = 8085
addr = (host, port)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

GPIO.setmode(GPIO.BOARD)
# pir sensor code

def get_PIR():
    GPIO.setup(pir_pin, GPIO.IN) #PIR
    try:
        time.sleep(1) # to stabilize sensor
        while True:
            data="pirFalse"
            if GPIO.input(pir_pin):
                print("Motion Detected...fjldgjwkwlkwekwk;er;lwekr;lwekr;lwer")
                data="pirTrue"
                UDPSock.sendto(data.encode(), addr)
                #send pir signals to computer
                #alarm in raspberry pis
                #send signals to computer to start detection from camera
                #time.sleep(2) #to avoid multiple detection
            else :
                print("Regular rotation")
                data=("pirFalse")
                UDPSock.sendto(data.encode(), addr)
            time.sleep(0.5) #loop delay, should be less than detection delay=
    except:
        GPIO.cleanup()
        print("gpio.cleaned at pir")


if __name__ == '__main__':
    get_PIR()
