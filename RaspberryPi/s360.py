import RPi.GPIO as GPIO                                ## Import GPIO Library.
#import time                                 ## Import ‘time’ library for a delay.
import socket 

host = ""
port = 8087
buf = 1024
addr = (host, port)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.bind(addr)

s360_port=32
GPIO.setmode(GPIO.BOARD)                    ## Use BOARD pin numbering.
GPIO.setup(s360_port, GPIO.OUT)                    ## set output.

pwm=GPIO.PWM(s360_port,50)                        ## PWM Frequency
pwm.start(5)
lobound=0
upbound= 180
angle=lobound


while True:
    (data, addr) = UDPSock.recvfrom(buf)
    data=data.decode()
    if (data=="move_right"):        
        print("moveright")
        angle=angle-0.5%upbound
        duty= float(angle)/10 + 2.5    ## Angle To Duty cycle  Conversion
        if(duty>0 and duty<100):                
            pwm.ChangeDutyCycle(duty)
            data=None
    elif (data=="move_left"):
        print("moveLeft")
        angle=angle+0.5%upbound
        duty= float(angle)/10 + 2.5
        if(duty>0 and duty<100):
            pwm.ChangeDutyCycle(duty)
            data=None
    #pwm.ChangeDutyCycle(duty)    
    #elif(data==None):
        #regular rotation

GPIO.cleanup()
