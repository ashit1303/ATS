import RPi.GPIO as GPIO
import time
import socket
rcwl_pin=36

host = "192.168.43.6" # set to IP address of target computer
port = 8086
addr = (host, port)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

GPIO.setmode(GPIO.BOARD)
# rcwl sensor code
def get_RCWL():
    GPIO.setup(rcwl_pin, GPIO.IN) #RCWL
    try:
        time.sleep(2) # to stabilize sensor
        while True:
            if GPIO.input(rcwl_pin):
                print("Motion Detected...klglkjegljdgjlkjglkerge")
                #send rcwl signals to computer
                #alarm in raspberry pi
                data="rcwlTrue"
                UDPSock.sendto(data.encode(), addr)
                time.sleep(1) #to avoid multiple detection
            else :
                print("Regular rotation")
                data=("rcwlFalse")
                UDPSock.sendto(data.encode(), addr)
            time.sleep(0.5) #loop delay, should be less than detection delay
    
    except:
        GPIO.cleanup()
        print("gpio.cleaned")

if __name__ == '__main__':
    get_RCWL()
