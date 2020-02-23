import RPi.GPIO as GPIO                                ## Import GPIO Library.
#import time                                 ## Import ‘time’ library for a delay.
import socket 

host = ""
port = 8088
buf = 1024
addr = (host, port)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.bind(addr)

s180_port=31
GPIO.setmode(GPIO.BOARD)                    ## Use BOARD pin numbering.
GPIO.setup(s180_port, GPIO.OUT)                    ## set output.
GPIO.setwarnings(False)
pwm=GPIO.PWM(s180_port,50)                        ## PWM Frequency
pwm.start(5)
lobound=6
upbound=8
duty=7
pwm.ChangeDutyCycle(duty)


while True:
    (data, addr) = UDPSock.recvfrom(buf)
    data=data.decode()
    if (data=="move_top"):        
        print("movetop")
        if(duty<=upbound and duty>=lobound):
            duty= duty+0.2    ## Angle To Duty cycle  Conversion
            pwm.ChangeDutyCycle(duty)
    elif (data=="move_bottom"):
        print("movebottom")
        if(duty<=upbound and duty>=lobound):
            duty=duty-0.1
            pwm.ChangeDutyCycle(duty)
    #pwm.ChangeDutyCycle(duty)    

GPIO.cleanup()
